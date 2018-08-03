#!/usr/bin/env bash
#petit script pour aspirer seulement le html d'une liste de sites web qui se trouvent dans un fichier .csv
#zf180803.0935
#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

echo ---------- start

#INPUT=./urls_test.csv
INPUT=./urls_myEpflGallery.csv

OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

#élimine la première ligne !
#read name Server parent site_url_jahia site_url_wp site_title username_viewer pwd_viewer < $INPUT

nblines=0
#while read name Server parent site_url_jahia site_url_wp site_title username_viewer pwd_viewer
while read sites

do
	echo $nblines
	if [ $nblines != "0" ]
	then
#		./aspi.sh $site_title $username_viewer $pwd_viewer
		./aspi.sh $sites
#		echo "."$sites"."
#$username_viewer $pwd_viewer
	fi
	((nblines+=1))
	echo ""
done < $INPUT

IFS=$OLDIFS

echo -e "
il y a comme nombre de pages HTML:
"

find ./html |grep '\.html' |wc

