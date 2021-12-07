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

### Set up token on AWS SSM

```bash
# Staging1 secret token
aws ssm put-parameter --name "/stg1/lambda/linetwstock/finmind_token" --value 'secret' --type "SecureString"
aws ssm put-parameter --name "/stg1/lambda/linetwstock/line_channel_secret" --value 'secret' --type "SecureString"
aws ssm put-parameter --name "/stg1/lambda/linetwstock/line_channel_access_token" --value 'secret' --type "SecureString"

# Production secret token
aws ssm put-parameter --name "/prod/lambda/linetwstock/finmind_token" --value 'secret' --type "SecureString"
aws ssm put-parameter --name "/prod/lambda/linetwstock/line_channel_secret" --value 'secret' --type "SecureString"
aws ssm put-parameter --name "/prod/lambda/linetwstock/line_channel_access_token" --value 'secret' --type "SecureString"
```

### Deploy

Use CDK deploy to AWS resource from local.

```bash
# example
# AWS SSO + aws-vault are recommended.
aws-vault exec {AWS_PROFILE} -- npx cdk diff linetwstock-cdk-stack-stg1
aws-vault exec {AWS_PROFILE} -- npx cdk deploy linetwstock-cdk-stack-stg1
```
