#!/usr/bin/env bash
#Petit script pour parser toutes les pages de Jahia à la recherche de documents 'my'
#zf180805.2354

echo -e " 

Cela va prendre un certain temps, il serait bien de le faire tourner dans un 'screen' avec:
screen -S my        pour entrer dans screen
./parser_my.sh       pour lancer le serveur WEB dans screen
CTRL+a,d                pour sortir de screen en laissant tourner le serveur
screen -r my        pour revenir dans screen
CTRL+d                  pour terminer screen
screen -list            pour lister tous les screen en fonctionement
"

#read -p "appuyer une touche pour démarrer parser_my.sh"

zcsv=`cat liste_pages.csv`
for i in $zcsv ; do 
#    echo -e $i
#    echo Start
    while read zline; do 
#        echo $zline

        if [[ $zline == *"documents.epfl.ch"* ]]; then
#echo "yyy"
#            echo -e "\n"$i
            echo $zline | sed 's/"/\n/g' | grep "documents.epfl.ch" | grep -i -E ".jpg|.png|.gif|.pdf|.doc|.docx"
#            echo $zline | sed 's/"/\n/g' | grep "documents.epfl.ch" | grep -i -e ".jpg" -e ".png" -e ".gif" -e ".pdf" -e ".doc" -e ".docx"

        fi

    done < $i






#    for line in $filelines ; do 

#        if [ `echo -e $line |grep documents`!="" ]
#        then
#            echo $i".epfl.ch,"$line
#        fi

#        echo $i".epfl.ch,"$line
#    done
done



exit


for i in *
	do echo -e $i
	filelines=`cat $i`
	for line in $filelines
		do echo $i".epfl.ch,"$line
	done
done > ../list_documents.csv



