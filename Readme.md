This is a quick set of scripts to allow you to automatically cut between two camera angles, based on which person is speaking more loudly.

Run `python3 generate_cuts.py  video_1.mp4 audio_1.wav video_2.mp4 audio_2.wav` to create a `cuts.json` file. This contains only the information telling you which video clip to cut to. It is created using only the audio information. Whoever is speaking louder will be cut to next.

Create a directory called "subclips" then run `./generate_clips.sh`. You will need to have a `cuts.json` file, and you will need to make sure the filenames in that file point to valid locations (typically `data/awais.mp4` or something similar).

Next create a folder called `formatted` and run `./format_clips.sh` to encode all the video files in the same format. This is necessary if the videos ahave different frame rates etc. 

Run `python3 generate_subclips_txt.py` to add padded zeros to the formatted subclip file names so they will be alphabetical. This will also generate a `subclips.txt` file.

Finally run `export_file.sh`. This will produce an `output.mp4`, then a `mute.mp4` file (which has no audio), and finally a `combined.mp4` file, which contains the full video with the combined audio file (you will need to prepare that file separately).

