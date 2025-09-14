CUR_TIME=$(date +"%H:%M")
END=18

cur_hour=$(date +%H)
cur_min=$(date +%M)

echo "Current time: $CUR_TIME."

if [ "$cur_hour" -ge "$END" ]; then
	echo "The work dy has ended."
else
	min=$(( cur_hour * 60 + cur_min ))
	end_min=$(( END * 60 ))

	min_remaining=$(( end_min - min ))
	hour_remaining=$(( min_remaining / 60 ))
	min_remaining=$(( min_remaining % 60 ))

	echo " Work day ends after $hour_remaining hours and $min_remaining minutes."
fi
