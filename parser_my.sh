#!/usr/bin/env bash
#Petit script pour parser toutes les pages de Jahia à la recherche de documents 'my'
#zf180806.1618

#echo -e " 
#
#Cela va prendre un certain temps, il serait bien de le faire tourner dans un 'screen' avec:
#screen -S my        pour entrer dans screen
#./parser_my.sh       pour lancer le serveur WEB dans screen
#CTRL+a,d                pour sortir de screen en laissant tourner le serveur
#screen -r my        pour revenir dans screen
#CTRL+d                  pour terminer screen
#screen -list            pour lister tous les screen en fonctionement
#"
#read -p "appuyer une touche pour démarrer parser_my.sh"

zcsv=`cat liste_pages.csv`

for i in $zcsv ; do 
#    echo -e $i
    while read zline; do 
#        echo $zline

        if [[ $zline == *"documents.epfl.ch"* ]]; then
#echo "yyy"
            echo $zline | sed 's/"/\n/g' | grep "documents.epfl.ch" | egrep -i ".jpg|.png|.gif|.pdf" > temp.csv
#            cat temp.csv

            ztemp=`cat temp.csv`
            for j in $ztemp ; do
                echo -e $i", "$j
            done

        fi

    done < $i
done


