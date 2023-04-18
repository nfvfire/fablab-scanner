# fablab-scanner
A Library Card scanner for the Fablab, running on a Raspberry Pi

## Introduction
Our Fablab is situated in a library and the inscription works with the library account, thus everybody who comes to the fablab is obliged to put their library card in a small compartment. To update this method and be able to make stats we wanted to use a barcode scanner connected to the Raspberry Pi, where everybody scans their card once entering the lab and a second time leaving.

## Structure
The project is based on 3 main files that are called by .service files at boot. The main file is scan_scraper.py which has 3 objectives: Reading the data of the barcode scanner; Getting the correponding user information from the Library's database; Saving the scanned users in a JSON file per day. 
