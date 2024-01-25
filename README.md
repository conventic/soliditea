# ceylon

Review and audit smart contracts with AI

## Requirements

Check `solc --version` to make sure solidity is installed.  

### Install solc (if not yet installed)

<https://docs.soliditylang.org/en/latest/installing-solidity.html>

```console
brew update && brew upgrade && brew tap ethereum/ethereum && brew install solidity
solc-select install 0.8.16
solc-select use 0.8.16
solc --version
```

### Setup virtual environment (optional)

```console
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

### Install dependencies

```console
pip3 install -r requirements.txt
```

### Install truffle-flattener

```console
npm install -g truffle
npm install -g truffle-flattener
```

### Setup OpenAI API key

Create a `.env` file:

```console
cp .env.example .env
```

and replace `YOUR_API_KEY` with a valid API key.

### Run Slither

```console
solc-select use 0.8.16
slither contracts/BadAuth.sol --json slither_output.json
```

## Run AI code check

```console
python3 main.py analyze contracts/BadAuth.sol
```

To remove comments from the code you can use

```console
python3 main.py analyze contracts/BadAuth.sol \
    --without-comments
```
