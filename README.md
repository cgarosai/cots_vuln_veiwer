# Application de Liste des CVE

Cette application web Flask affiche une liste de CVE (Common Vulnerabilities and Exposures) et leur exploit pour un CPE (Common Platform Enumeration) donné. Elle s'intègre avec `exploitdb` et nécessite la base de données nourrie par `cve-ingest-pgsql` installée et alimentée.

## Prérequis

Avant d'exécuter l'application, assurez-vous d'avoir installé et configuré les éléments suivants :

1. **l'image docker** : Faire un ```docker build .``` pour créer l'image (ou sinon installer toutes les dépendances en local)
3. **cve-ingest-pgsql** : Un outil d'ingestion CVE basé sur PostgreSQL. Suivez les instructions [ici sur github](https://github.com/cgarosai/cve-ingest-pgsql) pour installer et alimenter la base de données.


## Installation

1) Avoir accès à une base de donnée nourrie de cve-ingest-pgsql
4) Modifier le fichier example.env avec les informations de la bdd cve-ingest-pgsql et le renommer en .env
5) Lancer la commande `docker compose up -d` pour lancer le docker en mode détaché ou `docker compose up` en mode attaché
6) Enjoy sur http://localhost:5000


