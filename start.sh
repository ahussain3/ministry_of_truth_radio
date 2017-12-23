# Supply arguments to this command in the following format
# video_1.mp4 audio_1.wav video_2.mp4 audio_2.wav combined.wav

echo "Generating cuts.json..."
python3 ../generate_cuts.py "f_"$1 $2 "f_"$3 $4

echo "Formatting video files..."
../format_video.sh $1
../format_video.sh $3

echo "Generating subclips"
mkdir subclips
../generate_clips.sh

echo "Generating subclips.txt file..."
python3 ../generate_subclips_txt.py

echo "Exporting finished product..."
../export_file.sh $5
