#!/bin/bash

# Variables
NAS_IP="192.168.1.1" # Replace with the IP of your Synology NAS
MOUNT_POINT="/mnt/synology" # Replace with the desired mount point
SHARE_NAME="/share" # Replace with the name of the shared folder on the NAS
USERNAME="username" # Replace with your Synology username
PASSWORD="password" # Replace with your Synology password
TIMEOUT=5 # Waiting time in seconds between connection attempts

# Create mounting point if necessary
if [ ! -d "${MOUNT_POINT}" ]; then
    sudo mkdir -p "${MOUNT_POINT}"
fi

# Synology NAS connection loop test
while true; do
    ping -c 2 "${NAS_IP}" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        break
    else
        echo "Erreur: Impossible de se connecter au NAS Synology à l'adresse IP ${NAS_IP}. Nouvelle tentative dans ${TIMEOUT} secondes..."
        sleep "${TIMEOUT}"
    fi
done

# Partition editing
sudo mount.cifs "//${NAS_IP}${SHARE_NAME}" "${MOUNT_POINT}" -o user=${USERNAME},password=${PASSWORD},uid=1000,gid=1000


# Verification of successful installation
if [ $? -eq 0 ]; then
    echo "Montage de la partition ${SHARE_NAME} sur le NAS Synology réussi."
else
    echo "Erreur: Impossible de monter la partition ${SHARE_NAME} sur le NAS Synology."
fi
