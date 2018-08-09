#!/usr/bin/env bash
#Petit script pour parser toutes les pages d'un site à la recherche de documents de boîtes myEpflGallery pour voir si un site a bien été migré
#zf180809.1026

#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./parser_check_myEpflGallery.sh site_nam \n\n"
    exit
fi
echo ---------- start parser_check_myEpflGallery.sh

# aspire site JAHIA
rm -Rf html_check
mkdir html_check
cd html_check
wget --user-agent="Mozilla/5.0" -E -m -e robots=off –w 10 --no-parent -X "/files,/templates,/cms/engineName" "https://$1"
cd ..

# crée la liste de toutes les pages html de JAHIA
find ./html_check |grep '\.html' |sort > liste_pages_du_site.csv

echo -e "
il y a comme nombre de pages HTML:
"

cat liste_pages_du_site.csv |wc




#exit


zcsv=`cat liste_pages_du_site.csv`
echo "pages" > liste_pages_site_myEpflGallery.csv

for i in $zcsv ; do
    echo $i
    if grep -lq myEpflGalleryBox $i ; then
        echo $i >> liste_pages_site_myEpflGallery.csv
#        while read zline; do
#            if [[ $zline == *"documents.epfl.ch"* ]]; then
#                echo $zline | sed 's/"/\n/g' | grep "documents.epfl.ch" > temp.csv
#                ztemp=`cat temp.csv`
#                for j in $ztemp ; do
#                    if [[ $j == *".jpg"* ]] || [[ $j == *".JPG"* ]] || [[ $j == *".png"* ]] || [[ $j == *".gif"* ]] || [[ $j == *".pdf"* ]]  || [[ $j == *".doc"* ]]; then
#                        echo -e $i","$j
#                    fi
#                done
#            fi
#        done < $i
    fi
done



cat liste_pages_site_myEpflGallery.csv

