#!/bin/bash

# Function to check if a package is installed
check_package_installed() {
    dpkg -s "$1" &> /dev/null
    return $?
}

# List of required packages
PACKAGES=("libyaml-cpp-dev" "libtbb-dev" "gdb")

# Update package list
sudo apt-get update

# Loop through packages and install if not already installed
for package in "${PACKAGES[@]}"
do
    if check_package_installed "$package"; then
        echo "$package is already installed."
    else
        echo "$package is not installed. Installing..."
        sudo apt-get install -y "$package"
        if [ $? -eq 0 ]; then
            echo "Successfully installed $package."
        else
            echo "Failed to install $package. Exiting."
            exit 1
        fi
    fi
done

echo "All dependencies checked and installed successfully."