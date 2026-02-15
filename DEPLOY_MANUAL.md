# Manual Deployment Guide

Since AWS SAM requires AWS credentials, here's how to deploy manually:

## Step 1: Configure AWS Credentials

```powershell
# Option 1: Configure AWS CLI
aws configure

# Option 2: Set environment variables
$env:AWS_ACCESS_KEY_ID="your-access-key"
$env:AWS_SECRET_ACCESS_KEY="your-secret-key"
$env:AWS_DEFAULT_REGION="us-east-1"
```

## Step 2: Deploy with SAM

Once credentials are configured, run:

```powershell
bash deploy.sh
```

Or manually:

```powershell
sam build --region us-east-1
sam deploy --stack-name unifi-route53-updater --region us-east-1 --parameter-overrides UniFiApiKey=YOUR_API_KEY HostedZoneId=YOUR_ZONE_ID RecordName=your-domain.example.com TTL=300 ScheduleExpression="rate(5 minutes)" --capabilities CAPABILITY_IAM --resolve-s3
```

## Alternative: Deploy via AWS Console

1. **Create IAM Role** for Lambda:
   - Go to IAM Console
   - Create role with Lambda trust policy
   - Attach policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "route53:ChangeResourceRecordSets",
           "route53:GetChange"
         ],
         "Resource": [
           "arn:aws:route53:::hostedzone/YOUR_HOSTED_ZONE_ID",
           "arn:aws:route53:::change/*"
         ]
       },
       {
         "Effect": "Allow",
         "Action": [
           "logs:CreateLogGroup",
           "logs:CreateLogStream",
           "logs:PutLogEvents"
         ],
         "Resource": "arn:aws:logs:*:*:*"
       }
     ]
   }
   ```

2. **Create Lambda Function**:
   - Go to Lambda Console
   - Click "Create function"
   - Name: `UniFi-Route53-Updater`
   - Runtime: Python 3.11
   - Role: Select the role created above
   - Click "Create function"

3. **Upload Code**:
   - Copy contents of `lambda_function.py`
   - Paste into Lambda code editor
   - Click "Deploy"

4. **Configure Environment Variables**:
   - Go to Configuration → Environment variables
   - Add:
     - `UNIFI_API_KEY`: YOUR_UNIFI_API_KEY
     - `HOSTED_ZONE_ID`: YOUR_HOSTED_ZONE_ID
     - `RECORD_NAME`: your-domain.example.com
     - `TTL`: 300

5. **Add EventBridge Trigger**:
   - Go to Configuration → Triggers
   - Click "Add trigger"
   - Select "EventBridge (CloudWatch Events)"
   - Create new rule:
     - Name: `UniFi-Route53-Schedule`
     - Rule type: Schedule expression
     - Schedule expression: `rate(5 minutes)`
   - Click "Add"

6. **Test**:
   - Go to Test tab
   - Create test event (empty JSON: `{}`)
   - Click "Test"
   - Check logs for success

## Verify Deployment

After deployment, check:

```powershell
# View logs
aws logs tail /aws/lambda/UniFi-Route53-Updater --follow --region us-east-1

# Test function
aws lambda invoke --function-name UniFi-Route53-Updater --region us-east-1 response.json
cat response.json

# Check Route53 record
aws route53 list-resource-record-sets --hosted-zone-id YOUR_ZONE_ID --region us-east-1 | Select-String -Pattern "your-domain.example.com" -Context 5
```

## Example Configuration

- **External IP**: Retrieved from UniFi API
- **DNS Record**: your-domain.example.com
- **Hosted Zone**: YOUR_HOSTED_ZONE_ID
- **Update Frequency**: Every 5 minutes
