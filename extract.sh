#!/bin/bash

if [ $# -eq 0 ]; then
    echo "DBLP key missing"
    exit
fi

KEY=$1
FILE=tmp.xml

wget --quiet --output-document $FILE https://dblp.uni-trier.de/rec/xml/$KEY

case ${KEY:0:4} in
    "conf")
        CONTAINING_PUB=booktitle
        ;;
    "jour")
        CONTAINING_PUB=journal
        ;;
esac

AUTHORS=`xmlstarlet sel -t -v '/dblp//author' $FILE | perl -pe 's/\n/$1, /'`
TITLE=`xmlstarlet sel -t -v '/dblp//title' $FILE`
VENUE=`xmlstarlet sel -t -v "/dblp//$CONTAINING_PUB" $FILE`
YEAR=`xmlstarlet sel -t -v '/dblp//year' $FILE`
URL=`xmlstarlet sel -t -v '/dblp//ee' $FILE`

echo -e "$URL\thttps://dblp.uni-trier.de/rec/html/$KEY\t\t$AUTHORS\t$TITLE\t$VENUE\t$YEAR" | xsel -b
