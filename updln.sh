#! /bin/sh

find . -maxdepth 1 -type l -delete

grep rst index.rst | sed 's/^ *//' | while read F; do
	LOC=""

	for D in "શ્લોક" "ગરબા" "રાસ" "bollywood"; do
		if [ -f "../../$D/$F" ]; then
			LOC="../../$D/$F"
			break
		fi
	done

	if [ -f "$LOC" ]; then
		ln -s "$LOC"
	else
		echo "***$F*** does not exist"
	fi

done
