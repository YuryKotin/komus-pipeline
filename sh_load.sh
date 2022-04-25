#!/usr/bash


if [ $# -eq 0 ]
  then
    date=$(date +%F)
  else
    date=$1
    echo $date
fi

bak=$(grep bak schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
bak_folder="$bak/$date"
#echo $bak_folder

db_categories_file=$(   grep db_categories_file    schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
db_subcategories_file=$(grep db_subcategories_file schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
db_prices_file=$(       grep db_prices_file        schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
db_products_file=$(     grep db_products_file      schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
db_descriptions_file=$( grep db_descriptions_file  schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
db_dates_file=$(        grep db_dates_file         schema.py | tr '= ' '\n' | tail -n 1 | tr -d "'")
#echo $db_categories_file

if ! [ -e "$bak_folder" ]; then
    mkdir "$bak_folder"
fi

cp $db_categories_file    "$bak_folder"
cp $db_subcategories_file "$bak_folder"
cp $db_prices_file        "$bak_folder"
cp $db_products_file      "$bak_folder"
cp $db_descriptions_file  "$bak_folder"
cp $db_dates_file         "$bak_folder"

python3 load.py --date $date

