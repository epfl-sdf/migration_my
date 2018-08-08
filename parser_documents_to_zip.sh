#!/usr/bin/env bash
#petit script pour aspirer tous les documents 'my' qui se trouvent dans les boîtes myEpflGallery selon une liste .csv
#zf180808.1623
#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

echo ---------- start

echo -e "site, url" > tempzip.csv
head -n 100000 liste_url_documents_uniq.csv >> tempzip.csv
#cat liste_url_documents_uniq.csv >> tempzip.csv

rm -Rf zip
mkdir zip
cd zip
mkdir tmp
cd tmp

INPUT=../../tempzip.csv
OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
zsite="tmp"
while read site url ; do
    echo $nblines
    if [ $nblines != "0" ] ; then
        site=`echo $site | awk -F "/" '{print $3}'`
        echo -e "le site est: "$site
        if [ "$zsite" != "$site" ] ; then
            echo -e "on zip le dossier: "$zsite
            zip -r ../$zsite".zip" .
            echo -e "on remonte d'un étage"
            cd ..
            echo -e "on crée le nouveau dossier "$site" et on se déplace"
            mkdir $site
            cd $site
            zsite=$site
            echo -e "on aspire le nouveau site:"$site
        fi
        echo -e "on aspire: "$url
        pwd
        wget -x $url
    fi
    ((nblines+=1))
    echo ""
done < $INPUT
IFS=$OLDIFS


exit


echo -e "
il y a comme nombre de pages HTML:
"

find ./html |grep '\.html' |wc

