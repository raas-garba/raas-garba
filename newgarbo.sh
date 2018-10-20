#! /bin/sh

for G; do
    GARBO="$G.rst"
    if [ -f "$GARBO" ]; then
        echo "$GARBO exists, skipped!" 1>&2
    else
        echo "$G" > "$GARBO"
        echo "$G" | sed 's/./-/g' >> "$GARBO"
    fi
done
