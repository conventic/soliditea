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
pip install solc-select
solc-select install 0.8.16
solc-select use 0.8.16
pkgx install node
pkgx install npm
npm install truffle 
npm install truffle-flattener
pip install -r requirements.txt

# Check if .env file exists, otherwise create it and prompt for OpenAI API key
if [ ! -f ".env" ]; then
    echo "Enter your OpenAI API key:"
    read OPENAI_API_KEY
    echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env
fi

echo "Setup complete."