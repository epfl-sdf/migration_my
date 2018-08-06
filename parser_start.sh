#!/usr/bin/env bash
#Petit script pour lancer toute la moulinette pour parser les istes et calculer la taille golbale des documents 'my'
#zf180806.1630

echo -e " 

Cela va prendre un certain temps, il serait bien de le faire tourner dans un 'screen' avec:
screen -S parser        pour entrer dans screen
./parser_start.sh       pour lancer le serveur WEB dans screen
CTRL+a,d                pour sortir de screen en laissant tourner le serveur
screen -r parser        pour revenir dans screen
CTRL+d                  pour terminer screen
screen -list            pour lister tous les screen en fonctionement
"

read -p "appuyer une touche pour démarrer parser_start.sh"

# aspire tous les sites JAHIA, cela prend 20mn !
#rm -Rf html
#./batch_aspi.sh

# crée la liste de toutes les pages html de JAHIA
find ./html |grep '\.html' |sort > liste_pages.csv

# parse toutes les pages de JAHIA à la recherche de documents 'my'
./parser_my.sh > liste_url_documents_brute.csv

# compte le nombre de documents dans la liste brute 'my'
wc liste_url_documents_brute.csv

# élimine les doublons dans les documents 'my'
cat liste_url_documents_brute.csv |sort | uniq > liste_url_documents_uniq.csv

# compte le nombre de documents 'my'
wc liste_url_documents_uniq.csv

