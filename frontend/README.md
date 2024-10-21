# Frontend SPA

## Run local

```bash
npm install
```

Change the Step Function ARN in [pages](./frontend/src/pages/Presentation.js) (line 44)

```bash
npm start
```

If you have any problems, please check if CORS are enable in API Gateway


## Build

```bash
npm run build
```

## Deploy

```bash
aws cloudformation create-stack --stack-name ppt-generator-frontend --template-body file://template.yaml
aws cloudformation wait stack-create-complete --stack-name ppt-generator-frontend
bucket_name=$(aws cloudformation describe-stacks --stack-name ppt-generator-frontend --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' --output text)
cloudfront_id=$(aws cloudformation describe-stacks --stack-name ppt-generator-frontend --query 'Stacks[0].Outputs[?OutputKey==`CFDistributionID`].OutputValue' --output text)
cloudfront_name=$(aws cloudformation describe-stacks --stack-name ppt-generator-frontend --query 'Stacks[0].Outputs[?OutputKey==`CFDistributionName`].OutputValue' --output text)
aws s3 sync ./build s3://$bucket_name
aws cloudfront create-invalidation --distribution-id $cloudfront_id --paths "/*"
echo Access the page $cloudfront_name
```

Info: src/assets/logo.jpg is used under the terms of the Creative Commons CC0 1.0 Universal Public Domain Dedication: https://creativecommons.org/publicdomain/zero/1.0/deed.en