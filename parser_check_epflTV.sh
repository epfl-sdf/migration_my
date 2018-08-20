#!/usr/bin/env bash
#Petit script pour parser toutes les pages d'un site à la recherche de boîtes epflTV pour voir si un site a bien été migré
#zf180820.1429

#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./parser_check_epflTV.sh site_nam.epfl.ch \n\n"
    exit
fi
echo ---------- start parser_check_epfl_TV.sh

# aspire site JAHIA
rm -Rf html_check
mkdir html_check
cd html_check
wget --user-agent="Mozilla/5.0" -E -m -e robots=off –w 10 --no-parent -X "/files,/templates,/cms/engineName" "https://$1"
cd ..

# crée la liste de toutes les pages html de JAHIA
find ./html_check |grep '\.html' |sort > liste_pages_du_site.csv

echo -e "
Nombre de pages HTML aspirées sur le site: "
cat liste_pages_du_site.csv |wc

# parse toutes les pages du site à la recherche de la boîte
zcsv=`cat liste_pages_du_site.csv`
echo -e "\nPages qui ont encore epflTvVideoBox: " > liste_pages_site_epflTV.csv

for i in $zcsv ; do
#    echo $i
#    if grep -lq epflTvVideoBox $i ; then
    if grep -ilq epfltv $i ; then
#    if grep -lq epflTv $i ; then
        echo $i >> liste_pages_site_epflTV.csv
    fi
done

cat liste_pages_site_epflTV.csv
