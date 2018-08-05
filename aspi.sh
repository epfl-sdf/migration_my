#!/usr/bin/env bash
#Petit script pour juste aspirer que les .html d'un site web pour faire des tests en local
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf180805.1538

#source: https://stackoverflow.com/questions/22614331/authenticate-on-wordpress-with-wget


#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./aspi.sh site_name user passwd \n\n"
    exit
fi

echo ---------- start aspi.sh

site=$1
agent="Mozilla/5.0"

#source ../aspi.credentials.sh

echo $1
echo $site

#exit

#rm -R $cookies $server$url $server$url".html"

mkdir html
cd html

wget \
    --user-agent="$agent" \
    -E -m -e robots=off –w 10 --no-parent -R "*.jpg,*.mp3,*.png,*.pdf,*.mpg,*.zip,*.JPG" "$site"


#    -E -m -e robots=off –w 10 --no-parent -A "*.html" "$site"

#    -p -k -E -m -e robots=off –w 2 --no-parent "$site"


#echo -e "
#il y a comme nombre de pages HTML:
#"

#find $site |grep '\.html' |wc


#wget http://portesouvertes.epfl.ch/templates/epfl/static_epfl_menus/header_en.jsp -P ./portesouvertes.epfl.ch/templates/epfl/static_epfl_menus/
#wget http://portesouvertes.epfl.ch/templates/epfl/static_epfl_menus/header_fr.jsp -P ./portesouvertes.epfl.ch/templates/epfl/static_epfl_menus/

