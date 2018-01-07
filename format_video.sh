ffmpeg -i $1 -acodec copy -vcodec libx264 -s 1280x720 -r 30 -strict experimental "f_vid_"$1

ffmpeg -i "f_vid"$1 -i $2 -shortest -c:v copy -c:a aac -b:a 256k "f_"$1
