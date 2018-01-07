if [ -z "$2" ]; then
    ffmpeg -i $1 -acodec copy -vcodec libx264 -s 1280x720 -r 30 -strict experimental "f_"$1
else
    ffmpeg -i $1 -i $2 -acodec aac -vcodec libx264 -s 1280x720 -r 30 -strict experimental -map 0:v:0 -map 1:a:0 "f_"$1
fi
