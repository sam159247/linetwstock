# linetwstock

A practice project to query data through [Line](https://line.me/). Data resource is from [FinMind](https://github.com/FinMind/FinMind)

## Description

The basic idea is that Line handles frontend and using AWS Lambda with Amazon API Gateway for backend to deal with data from FinMind.

## Getting Started

### VSCode Quick Start

- Install and run extension "Remote - Containers" (id: ms-vscode-remote.remote-containers).

### Dependencies

- Python 3.9+
- Poetry

### Installing

```bash
poetry install
```

### Local test

```bash
# set up .env file first.

docker-compose -f docker-compose.dev.yml up --build

# example
curl -vsL "http://127.0.0.1:9001/get_stock_price?stock_id=2330&start_date=2021-12-01"
```
