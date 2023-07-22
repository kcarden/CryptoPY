#!/bin/bash

# Function to check if a command is available
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to install Python and required Python packages
install_dependencies() {
  echo "Installing Python and required packages..."
  if command_exists apt; then
    # Debian/Ubuntu
    sudo apt update
    sudo apt install -y python3 python3-pip python3-tk
  elif command_exists yum; then
    # CentOS/RHEL
    sudo yum install -y epel-release
    sudo yum install -y python3 python3-pip python3-tkinter
  elif command_exists brew; then
    # macOS with Homebrew
    brew install python-tk
  else
    echo "Unsupported system. Please install Python and tkinter manually."
    exit 1
  fi

  # Install Python packages
  pip3 install -r requirements.txt
}

# Function to create required folders
create_folders() {
  echo "Creating necessary folders..."
  mkdir -p plugins
  mkdir -p modules
}

# Function to download files from the GitHub repository
download_files() {
  echo "Downloading files from GitHub..."
  # Replace the URL below with your actual GitHub repository URL
  git clone https://github.com/kcarden/CryptoPY.git
  # Move the files to the appropriate folders
  mv CryptoPY/main.py .
  mv CryptoPY/plugins/* plugins/
  mv CryptoPY/ReadMe.md .
  mv CryptoPY/DEVELOPERS.md .
  # Delete the downloaded repository folder
  rm -rf CryptoPY
}

main() {
  # Check if Python is installed
  if ! command_exists python3; then
    install_dependencies
  fi

  # Create necessary folders
  create_folders

  # Download files from GitHub
  download_files

  echo "Installation completed successfully!"
}

main
