#!/usr/bin/env bash
#Petit script pour parser toutes les pages de Jahia à la recherche de documents 'my'
#zf180807.0849

zcsv=`cat liste_pages.csv`



    for i in $zcsv ; do

if grep -lq myEpflGalleryBox $i ; then

echo "--------------------"$i


        while read zline; do
            if [[ $zline == *"documents.epfl.ch"* ]]; then
                echo $zline | sed 's/"/\n/g' | grep "documents.epfl.ch" | egrep -i ".jpg|.png|.gif|.pdf" > temp.csv
                ztemp=`cat temp.csv`
                for j in $ztemp ; do
                    echo -e $i", "$j
                done
            fi
        done < $i
fi
    done

