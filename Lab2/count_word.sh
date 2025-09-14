#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: count_word.sh <filename> <word>"
    exit 1
fi

FILE="$1"
WORD="$2"

COUNT=$(grep -o -w "$WORD" "$FILE" | wc -l)
echo "The word '$WORD' appears $COUNT times in $FILE."
