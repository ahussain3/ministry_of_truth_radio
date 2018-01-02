ffmpeg -f concat -safe 0 -i subclips.txt -c copy output.mp4

ffmpeg -i output.mp4 -codec copy -an mute.mp4

ffmpeg -i mute.mp4 -i $1 -shortest -c:v copy -c:a aac -b:a 256k combined.mp4
