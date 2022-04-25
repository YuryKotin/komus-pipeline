#!/usr/bash

html_catalog_folder=$(grep html_catalog_folder schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
html_pages_folder=$(grep   html_pages_folder   schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")

if [ $# -eq 0 ]
  then
    date=$(date +%F)
  else
    date=$1
fi

catalog_folder="$html_catalog_folder/$date"
pages_folder="$html_pages_folder/$date"

if ! [ -e "$catalog_folder" ]; then
    mkdir "$catalog_folder"
fi

if ! [ -e "$pages_folder" ]; then
    mkdir "$pages_folder"
fi

python3 extract_catalog.py --date $date

python3 extract_data.py --date $date

