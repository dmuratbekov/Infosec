#!/bin/bash
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: delete_empty_files.sh <directory>"
    exit 1
fi

DIR="$1"
find "$DIR" -type f -empty -print -delete
