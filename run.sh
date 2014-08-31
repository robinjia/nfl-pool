#!/bin/bash
USAGE=$(cat <<EOF
Use available data to make NFL Suicide Pool picks.

Usage: $0 year week
EOF
)
if [ -z "$2" ]
then
  echo "$USAGE"
  exit 1
fi
year=$1
week=$2
filename=output/predictions_${year}_${week}.txt
mkdir -p output
echo "Computing game outcome probabilities..." 1>&2
python src/py/schedule.py $year $week > $filename
echo "Determining optimal pick sequence..." 1>&2
build/make-picks $filename
