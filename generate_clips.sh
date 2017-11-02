NUM_CUTS=$(jq 'length' cuts.json)
FUDGE_FACTOR=0.01
echo $NUM_CUTS

for i in `seq 0 $NUM_CUTS`; do
  line=$(jq -c ".["$i"]" cuts.json)
	TIME_IN=$(echo $line | jq '.time_in')
	TIME_OUT=$(echo $line | jq '.time_out')
	DURATION=$(bc<<<"$TIME_OUT"-"$TIME_IN"-"$FUDGE_FACTOR")
	FILE_IN=$(echo $line | jq -r '.cut_to')
	FILE_OUT="subclips/"$(echo $line | jq '.time_in')".mp4"

  echo "---------------\n"
	echo $TIME_IN
	echo $FILE_IN
	echo $DURATION
	echo $FILE_OUT

  ffmpeg -ss $TIME_IN -i $FILE_IN -t $DURATION $FILE_OUT
done

echo "DONE!"
