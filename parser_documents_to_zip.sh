#!/usr/bin/env bash
#petit script pour aspirer tous les documents 'my' qui se trouvent dans les boîtes myEpflGallery selon une liste .csv et en faire un zip avec notation préfixée
#zf180813.1021
#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

echo ---------- start

echo -e "site, url" > tempzip.csv
head -n 100000 liste_url_documents_uniq.csv >> tempzip.csv
#cat liste_url_documents_uniq.csv >> tempzip.csv

cd /mnt/data
rm -Rf zip
mkdir zip
cd zip
mkdir tmp
cd tmp

INPUT=/home/ubuntu/migration_my/tempzip.csv
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
        wget -O `echo $url | awk -F "/" '{ for(i=5 ; i <= NF ; i++) { printf "_%s",$i } printf "\n"}' | sed "s/\%20/_/g" | sed "s/\%2C//g"` $url
    fi
    ((nblines+=1))
    echo ""
done < $INPUT
IFS=$OLDIFS

echo -e "on zip le dossier: "$zsite
zip -r ../$zsite".zip" .




exit


echo -e "
il y a comme nombre de pages HTML:
"

find ./html |grep '\.html' |wc

