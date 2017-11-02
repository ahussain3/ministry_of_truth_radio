import sys
import time
import math
from moviepy.editor import *
from scipy.io.wavfile import read
import numpy as np
import argparse

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
BIAS_HYSTERESIS = 10
MIN_LENGTH = 4
MULTIPLIER = 160

def setupArgsParser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('video_a', type=str,
                    help='path to video of person a')
    parser.add_argument('audio_a', type=str,
                    help='path to audio of person a')
    parser.add_argument('video_b', type=str,
                    help='path to video of person b')
    parser.add_argument('audio_b', type=str,
                    help='path to audio of person b')
    parser.add_argument('-o', '--output', type=str,
                    help='specify the output file')

    return parser.parse_args()

def update_progress(progress):
    progress_int = int(progress)
    sys.stdout.write('\r[{0}] {1}%'.format('#'*(math.floor(progress_int/10)), progress_int))

class AudioChannel(object):
    def __init__(self, video_file_name, audio_file_name):
        super(AudioChannel, self).__init__()
        self.video_file_name = video_file_name
        self.audio_file_name = audio_file_name
        self.audio = read(audio_file_name)[1]

def amplitude(arr):
    return np.sqrt(np.mean(np.square(np.array(arr, dtype="int32"))))

def chunked_amplitude(audio):
    output = []
    for i in range(0, len(audio) - CHUNK_SIZE, CHUNK_SIZE):
        output.append(amplitude(audio[i : i + CHUNK_SIZE]))

    return output

def long_amplitude(audio):
    return np.mean(chunked_amplitude(audio))

def generate_cuts(person_a, person_b):
    output = []
    currently_showing = person_a if long_amplitude(person_a.audio[0:(MULTIPLIER*CHUNK_SIZE)]) > long_amplitude(person_b.audio[0:(MULTIPLIER*CHUNK_SIZE)]) else person_b
    not_showing = person_b if currently_showing == person_a else person_a
    prev_time_out = 0.0

    for i in np.arange(0, len(person_a.audio) - (CHUNK_SIZE * MULTIPLIER), CHUNK_SIZE):
        if (i % 10000 == 0):
            update_progress(i / (len(person_a.audio) - (CHUNK_SIZE * MULTIPLIER)) * 100)

        time_out = i / SAMPLE_RATE

        other_person_is_speaking = amplitude(not_showing.audio[i:i+CHUNK_SIZE]) > amplitude(currently_showing.audio[i:i+CHUNK_SIZE])
        other_person_will_be_speaking = long_amplitude(not_showing.audio[i:i+(MULTIPLIER*CHUNK_SIZE)]) > long_amplitude(currently_showing.audio[i:i+(MULTIPLIER*CHUNK_SIZE)])
        should_switch = other_person_is_speaking and other_person_will_be_speaking and ((time_out - prev_time_out) > MIN_LENGTH)

        if should_switch:
            output.append({'cut_to': currently_showing.video_file_name, 'time_in': prev_time_out, 'time_out': time_out})
            prev_time_out = i / SAMPLE_RATE

            temp = currently_showing
            currently_showing = not_showing
            not_showing = temp

    output.append({'cut_to': currently_showing.video_file_name, 'time_in': prev_time_out, 'time_out': len(person_a.audio) / SAMPLE_RATE})

    return output

def build_clips(cuts):
    clips = []
    duration = int(cuts[-1]["time_out"])
    for i, cut in enumerate(cuts):
        update_progress(i/len(cuts))
        try:
            clips.append(VideoFileClip(cut["cut_to"]).subclip(cut["time_in"], min(cut["time_out"], duration)))
        except:
            print("Unable to add clip: {0} [{1} : {2}]".format(cut["cut_to"], cut["time_in"], min(cut["time_out"], duration)))
    return clips

def main():
    args = setupArgsParser()
    person_a = AudioChannel(args.video_a, args.audio_a)
    person_b = AudioChannel(args.video_b, args.audio_b)

    print("Generating cuts...")
    cuts = generate_cuts(person_a, person_b)
    print("\nCuts Generated")

    print("Building clips...")
    clips = build_clips(cuts)
    print("{0} clips in total".format(len(clips)))

    result = concatenate_videoclips(clips)
    output_file = args.output if args.output else "output.mp4"
    result.write_videofile(output_file, verbose=True, codec="libx264") # Many options...

main()