#!/bin/bash

# Check if pkgx is installed
if ! command -v pkgx &> /dev/null
then
    echo "pkgx could not be found, installing it now."
    curl -Ssf https://pkgx.sh | sh
else
    echo "pkgx is already installed."
fi

# Install Solidity, Python, Node.js, and truffle-flattener
pkgx install solc@0.8.24
solc-select install 0.8.24
solc-select use 0.8.24
pkgx install python@3.7
pkgx install node
pkgx npm install -g truffle
pkgx npm install -g truffle-flattener

# Set up virtual environment using Python
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Check if .env file exists, otherwise create it and prompt for OpenAI API key
if [ ! -f ".env" ]; then
    echo "Enter your OpenAI API key:"
    read OPENAI_API_KEY
    echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env
fi

echo "Setup complete."