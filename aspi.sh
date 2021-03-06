#!/usr/bin/env bash
#Petit script pour juste aspirer que les .html d'un site web pour faire des tests en local
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf180808.0846

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

mkdir html
cd html
wget --user-agent="Mozilla/5.0" -E -m -e robots=off –w 10 --no-parent -X "/files,/templates,/cms/engineName" "$site"
