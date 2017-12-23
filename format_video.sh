ffmpeg -i $1 -acodec copy -vcodec libx264 -s 1280x720 -r 30 -strict experimental "f_"$1
