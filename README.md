# Application de Liste des CVE

Cette application web Flask affiche une liste de CVE (Common Vulnerabilities and Exposures) et leur exploit pour un CPE (Common Platform Enumeration) donné. Elle s'intègre avec `exploitdb` et nécessite la base de données `cve-ingest-pgsql` installée et alimentée.

## Prérequis

Avant d'exécuter l'application, assurez-vous d'avoir installé et configuré les éléments suivants :

1. **l'image docker** : Accès à l'image docker de l'application disponible ou accès à internet via le proxy
2. **exploitdb** : Une base de données d'exploits publics et des logiciels vulnérables associés.
3. **cve-ingest-pgsql** : Un outil d'ingestion CVE basé sur PostgreSQL. Suivez les instructions [ici sur github](https://github.com/cgarosai/cve-ingest-pgsql) pour installer et alimenter la base de données.


## Installation

1) Avoir accès à une base de donnée nourrie de cve-ingest-pgsql
2) Récupérer la dernière image Docker de l'application (fichier .tar)
3) Charger l'image Docker en local : `docker load --input <fichier tar>` (noter le nom de l'image)
4) Modifier le fichier example.env avec les informations de la bdd cve-ingest-pgsql et le renommer en .env
5) Lancer la commande `docker compose up -d` pour lancer le docker en mode détaché ou `docker compose up` en mode attaché
6) Enjoy sur http://localhost:5000

# TODO
- [x] trier par sévérité 
- [x] Trier par date à partir d'une date
- [x] Trier s'il y a exploit 
- [x] Gestion lien CVE

