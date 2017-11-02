for file in ./subclips/*
do
    ffmpeg -i $file -acodec copy -vcodec libx264 -s 1280x720 -r 30 -strict experimental "./formatted/"$(basename "$file")
done
