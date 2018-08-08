#!/usr/bin/env bash
#Petit script pour parser toutes les pages de Jahia à la recherche de documents 'my' qui se trouvent dans une boîte myEpflGallery
#zf180808.1625

zcsv=`cat liste_pages.csv`
echo "pages" > liste_pages_myEpflGallery.csv

for i in $zcsv ; do
    if grep -lq myEpflGalleryBox $i ; then
        echo $i >> liste_pages_myEpflGallery.csv
        while read zline; do
            if [[ $zline == *"documents.epfl.ch"* ]]; then
                echo $zline | sed 's/"/\n/g' | grep "documents.epfl.ch" > temp.csv
                ztemp=`cat temp.csv`
                for j in $ztemp ; do
                    if [[ $j == *".jpg"* ]] || [[ $j == *".JPG"* ]] || [[ $j == *".png"* ]] || [[ $j == *".gif"* ]] || [[ $j == *".pdf"* ]]  || [[ $j == *".doc"* ]]; then
                        echo -e $i","$j
                    fi
                done
            fi
        done < $i
    fi
done

