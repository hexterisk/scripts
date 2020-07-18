#!/bin/bash

# Check if the package exists.
if [[ -f "pin.tar.gz" ]]; then
    echo -e "\e[36m\n[+] Found package.\n\e[0m"
else 

    # Check if a URL has been given as an argument.
    if [[ $# -eq 1 ]]; then
        URL=$1
        echo -e "\e[36m\n[+] Downloading package from $URL.\n\e[0m"
    else
        echo -e "Use default URL to download Pin v3.13?[y/n]"
        read choice
        if [[ "$choice" = "y" ]]; then
            URL="https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.13-98189-g60a6ef199-gcc-linux.tar.gz"
            echo -e "\e[36m\n[+] Downloading package from $URL.\n\e[0m"
        else
            exit 0
        fi
    fi
fi

# Fetch the package containing Pin.
wget $URL -O pin.tar.gz

# Extract the package in the Pin directory.
echo -e "\e[36m\n[+] Extracting the package.\e[0m\n"
mkdir pin-dir
tar -zxvf pin.tar.gz -C pin-dir --strip-components=1

# Move the folder to /opt/.
sudo mv pin-dir /opt/

# Make all files depending on the CPU architecture.
cd /opt/pin-dir/source/tools
arch=$(uname -m)
if [[ "$arch" == 'x86_64' ]]; then
    echo -e "\e[36m\n[+] Building for x86_64 architecture.\n\e[0m"
    make all
elif [[ "$arch" == 'x86_32' ]]; then
    echo -e "\e[36m\n[+] Building for x86 architecture.\n\e[0m"
    make all TARGET=ia32
else
    echo -e "\e[31m\n[-] CPU architecture unknown. Exiting.\n\e[0m"
    exit 0
fi

# Remove the zip.
rm pin.tar.gz
echo -e "\e[32m\n[+] Setup complete.\n\e[0m"
