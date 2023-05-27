# fablab-scanner
A Library Card scanner for the Fablab, running on a Raspberry Pi

## Introduction
Our Fablab is situated in a library and the inscription works with the library account, thus everybody who comes to the fablab is obliged to put their library card in a small compartment. To update this method and be able to make stats we wanted to use a barcode scanner connected to the Raspberry Pi, where everybody scans their card once entering the lab and a second time leaving.

## Structure
The project is based on 3 main files that are called by .service files at boot. The main file is scan_scraper.py which has 3 objectives: Reading the data of the barcode scanner; Getting the correponding user information from the Library's database; Saving the scanned users in a JSON file per day. The second file is a python file that checks for new users in the json file and exports them on the Fablab's NAS as .xlsx, it could also be done as .csv. The third file is a bash file mounting the Fablab's NAS on the Raspberry Pi. There's also a file with different fonctions for the i2c display that is included in the main python file.

---

# fablab-scanner
Un scanner de cartes de bibliothèque pour le Fablab, fonctionnant sur un Raspberry Pi

## Introduction
Notre Fablab est situé dans une bibliothèque et l'inscription fonctionne avec le compte de la bibliothèque, ainsi chaque personne qui vient au fablab est obligée de mettre sa carte de bibliothèque dans un petit compartiment. Pour mettre à jour cette méthode et pouvoir faire des statistiques nous avons voulu utiliser un lecteur de code-barres connecté au Raspberry Pi, où tout le monde scanne sa carte une fois en entrant dans le laboratoire et une deuxième fois en le quittant.

## Structure
Le projet est basé sur 3 fichiers principaux qui sont appelés par des fichiers .service au démarrage. Le fichier principal est scan_scraper.py qui a 3 objectifs : Lire les données du scanner de codes-barres ; Obtenir les informations correspondantes sur les utilisateurs à partir de la base de données de la bibliothèque ; Sauvegarder les utilisateurs scannés dans un fichier JSON par jour. Le deuxième fichier est un fichier python qui vérifie la présence de nouveaux utilisateurs dans le fichier JSON et les exporte sur le NAS du Fablab au format .xlsx, mais aussi au format .csv. Le troisième fichier est un fichier bash qui monte le NAS du Fablab sur le Raspberry Pi. Il y a aussi un fichier avec différentes fonctions pour l'affichage i2c qui est inclus dans le fichier python principal.
