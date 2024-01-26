# ceylon

Review and audit smart contracts with AI. ceylon is a tool designed to assist  
in the smart contract development process. It leverages AI for reviewing and  
auditing Solidity contracts. This tool integrates with existing development  
workflows, offering insights into potential vulnerabilities and suggesting  
code improvements.

## Features

- AI-driven review and vulnerability check of smart contract code.
- Integration with Slither for static code analysis.
- Option to remove comments for testing.
- Customizable settings.

## Setup via pkgx

The following script will use pkgx to install all required dependencies

```console
./setup.sh
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

## Acknowledgments

Special thanks to all contributors and supporters of the project.

Peter Robinson (<https://github.com/drinkcoffee>) was a great inspiration in  
<https://www.youtube.com/watch?v=J7dUOSPG0WY&t=1531s> and published useful code  
on <https://github.com/drinkcoffee/EthEngGroupSolidityExamples/blob/master/ai/scripts/reviewsol.py>

## Manual setup

If you used the recommended pkgx setup you can ignore this part.

### Requirements

- Solidity: Check with `solc --version`.
- Python 3.7+.
- Node.js and npm for `truffle-flattener`.

Check `solc --version` to make sure solidity is installed.

#### Install solc (if not yet installed)

<https://docs.soliditylang.org/en/latest/installing-solidity.html>

```console
brew update && brew upgrade && brew tap ethereum/ethereum && brew install solidity
solc-select install 0.8.16
solc-select use 0.8.16
solc --version
```

#### Setup virtual environment (optional)

```console
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

#### Install dependencies

```console
pip3 install -r requirements.txt
```

#### Install truffle-flattener

```console
npm install -g truffle
npm install -g truffle-flattener
```

#### Setup OpenAI API key

Create a `.env` file:

```console
cp .env.example .env
```

and replace `YOUR_API_KEY` with a valid OpenAI API key.

#### Run Slither

```console
solc-select use 0.8.16
slither contracts/BadAuth.sol --json slither_output.json
```
