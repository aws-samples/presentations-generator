# AWS Presentations Generator demo Generative AI

## Architecture

![Architecture](./assets/architecture.png)

## Prerequisites

1. It is recommended to run this sample in a **sandbox account**. The sample has no tests and not all security best practices are implemented.
2. [AWS CLI](https://docs.aws.amazon.com/en_us/cli/latest/userguide/getting-started-install.html) configured with a user that has Admin permissions. This user will be used by AWS SAM
3. [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed
4. Solution tested in _us-east-1_ region
5. Node.js v18.16.0, NPM v9.5.1, Python v3.12
6. Docker installed

## Getting Started

1. [Manage Amazon Bedrock model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
2. Deploy the [backend](./backend/README.md)
3. Add your content and sync Bedrock KB
4. Change the API endpoint in [services](./frontend/src/services/api.js)
5. Deploy the [frontend](./frontend/README.md)
