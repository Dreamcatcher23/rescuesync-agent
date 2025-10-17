# RescueSync Agent - Deployment Guide

## Quick Deploy (30 Minutes)

### Prerequisites
- AWS Account with $100 credits
- IAM permissions for Lambda, Bedrock, S3, API Gateway

### Step 1: Create IAM Role (5 mins)
1. Go to IAM Console → Roles → Create role
2. Select AWS service → Lambda
3. Add permissions:
   - `AWSLambdaBasicExecutionRole`
   - `AmazonBedrockFullAccess`
4. Name: `RescueSyncLambdaRole`

### Step 2: Create Lambda Function (10 mins)
1. Go to Lambda Console → Create function
2. Function name: `rescuesync-agent`
3. Runtime: Python 3.11
4. Execution role: Use `RescueSyncLambdaRole`
5. Copy code from `lambda_function.py`
6. Configuration:
   - Timeout: 60 seconds
   - Memory: 512 MB

### Step 3: Create API Gateway (5 mins)
1. API Gateway Console → Create REST API
2. API name: `rescuesync-api`
3. Create POST method → Lambda proxy integration
4. Enable CORS (Lambda handles headers)
5. Deploy to stage: `prod`
6. Copy Invoke URL

### Step 4: Deploy Website (10 mins)
1. S3 Console → Create bucket: `rescuesync-demo-yourname`
2. Uncheck "Block all public access"
3. Enable static website hosting (index.html)
4. Add bucket policy:
{
"Version": "2012-10-17",
"Statement": [{
"Effect": "Allow",
"Principal": "",
"Action": "s3:GetObject",
"Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/"
}]
}

5. Update `index.html` with your API Gateway URL
6. Upload with public-read ACL
7. Access via bucket website endpoint

## Cost Estimate
- Demo usage: ~$0.15 (within $100 credits)
- Per coordination: $0.01-0.03
- Lambda/API/S3: Free tier eligible

## Troubleshooting
- **ValidationException**: Use inference profile `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- **ThrottlingException**: Wait 1 minute between tests
- **S3 403**: Check bucket policy and public access settings
- **CORS error**: Lambda response includes required headers
