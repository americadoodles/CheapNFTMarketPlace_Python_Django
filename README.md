# Cheap-NFT-Marketplace
Cheap NFT Marketplace - Backend &amp; Web3 con django

Affordable NFT Marketplace API with Python and Django An optimized, full-featured boilerplate template designed for seamless Web3 integration, tailored specifically for NFT marketplace developers. This solution provides a comprehensive foundation for building scalable and efficient NFT marketplaces.

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
