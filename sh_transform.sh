#!/usr/bash

products_path=$(  grep products_folder   schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
categories_path=$(grep categories_folder schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")

if [ $# -eq 0 ]
  then
    date=$(date +%F)
  else
    date=$1
    echo $date
fi

catalog_folder="$products_path/$date"
products_folder="$categories_path/$date"

if ! [ -e "$catalog_folder" ]; then
    mkdir "$catalog_folder"
fi

if ! [ -e "$products_folder" ]; then
    mkdir "$products_folder"
fi


python3 transform_catalog.py --date $date

python3 transform_data.py --date $date

