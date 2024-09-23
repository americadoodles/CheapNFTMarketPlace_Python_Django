# Cheap-NFT-Marketplace
Cheap NFT Marketplace - Backend &amp; Web3 con django

## Development env setup

```bash
py -m venv env
source ./env/Scripts/activate // linux
./env/Scripts/Activate.ps1 // windows
```

## Install dependencies

```bash
pip install -r ./requirements.txt
```

## Run server

```bash
cd cheapNFT
python manage.py runserver
```

## Endpoints

### GET **/list**

Get all auction list

### GET **/{id}**

Get auction data

### PUT **/bid/{id}**

Put bid to auction

### POST **/create**

Create new auction