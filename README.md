# migration_my
Tous les scripts pour la migration des boîtes Jahia myEpflGallery


## Buts:
Parser une liste de sites Jahia supposés contenir des boîtes Jahia myEpflGallery afin de trouver les pages qui les contiennent et enfin les documents 'my' à migrer.


## Installation
Il faut installer ceci:

```
sudo apt-get update
sudo apt-get install zip
```

## Description des scripts utilisés

**batch_aspi.sh**, script qui parse la liste des sites à parser

**aspi.sh**, script qui parse un seul site

**parser_start.sh**, script qui lance le tout

**parser_my.sh**, script qui parse la liste des pages des sites à la recherche des boîtes myEpflGallery et les documents 'my'


## Description des fichiers .csv

**liste_sites.csv**, liste des sites Jahia à parser

**liste_pages.csv**, liste des pages Jahia à parser

**liste_pages_myEpflGallery.csv**, liste des pages contenant les boîtes myEpflGallery

**liste_url_documents_brute.csv**, liste brute (avec doublons) des pages qui contiennent les boîtes myEpflGallery et les documents 'my' qui se trouvent
**liste_url_documents_uniq.csv**, liste finale (sans doublons) des pages qui contiennent les boîtes myEpflGallery et les documents 'my' qui se trouvent

**temp.csv**, fichier intermédiaire


## Utilisation
Simplement lancer le script:

`parser_start.sh`



zf180808.1652












.
