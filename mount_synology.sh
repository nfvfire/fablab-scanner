#!/bin/bash

# Variables
NAS_IP="192.168.1.4" # Remplacez par l'IP de votre NAS Synology
MOUNT_POINT="/mnt/synology" # Remplacez par le point de montage souhaité
SHARE_NAME="/Data" # Remplacez par le nom du dossier partagé sur le NAS
USERNAME="fablab" # Remplacez par votre nom d'utilisateur Synology
PASSWORD="fablab" # Remplacez par votre mot de passe Synology
TIMEOUT=5 # Temps d'attente en secondes entre les tentatives de connexion

# Création du point de montage si nécessaire
if [ ! -d "${MOUNT_POINT}" ]; then
    sudo mkdir -p "${MOUNT_POINT}"
fi

# Test de la connexion au NAS Synology en boucle
while true; do
    ping -c 2 "${NAS_IP}" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        break
    else
        echo "Erreur: Impossible de se connecter au NAS Synology à l'adresse IP ${NAS_IP}. Nouvelle tentative dans ${TIMEOUT} secondes..."
        sleep "${TIMEOUT}"
    fi
done

# Montage de la partition
sudo mount.cifs "//${NAS_IP}${SHARE_NAME}" "${MOUNT_POINT}" -o user=${USERNAME},password=${PASSWORD},uid=1000,gid=1000


# Vérification du succès du montage
if [ $? -eq 0 ]; then
    echo "Montage de la partition ${SHARE_NAME} sur le NAS Synology réussi."
else
    echo "Erreur: Impossible de monter la partition ${SHARE_NAME} sur le NAS Synology."
fi
