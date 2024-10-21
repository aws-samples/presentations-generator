# Backend API

## Build & Deploy

```bash
sam validate
sam build
sam deploy --stack-name ppt-generator-backend --resolve-s3 --resolve-image-repos --capabilities CAPABILITY_NAMED_IAM
```

- For the question DownloadPresentation and GetDynamoDB has no authentication. Is this okay? Press Y

- After the deployment, copy the Powerpoint Template file to S3 using the following commands:

  `aws s3 cp ./ppt-template.pptx s3://ppt-generator-backend-<AWS Account id>-pptgen/templates/`
