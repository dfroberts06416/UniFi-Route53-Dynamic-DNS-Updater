# UniFi Route53 Dynamic DNS Updater

AWS Lambda function that automatically updates a Route53 DNS record with your external IP address from UniFi Cloud API.

## Features

- 🔄 Automatically retrieves external IP from UniFi Cloud API
- 🌐 Updates Route53 A record automatically
- ⏰ Runs on a schedule (default: every 5 minutes)
- 💰 Minimal cost (~$0.50/month)
- 🚀 Easy deployment with AWS SAM

## Prerequisites

- AWS Account with Route53 hosted zone
- UniFi Cloud account with API access
- AWS CLI configured
- AWS SAM CLI (optional, for deployment)
- Python 3.11+

## Quick Start

### 1. Get Your UniFi API Key

1. Visit https://account.ui.com/
2. Generate an API key
3. Save it securely

### 2. Configure Your Settings

Copy the example configuration:

```bash
cp config.example.sh config.local.sh
```

Edit `config.local.sh` with your values:

```bash
export UNIFI_API_KEY="your-api-key"
export HOSTED_ZONE_ID="your-zone-id"
export RECORD_NAME="home.example.com"
```

### 3. Deploy

#### Option A: Using AWS SAM (Recommended)

```bash
# Install SAM CLI
pip install aws-sam-cli

# Build and deploy
sam build --region us-east-1
sam deploy --guided
```

#### Option B: Using the deployment script

```bash
# Edit deploy.sh with your configuration
nano deploy.sh

# Run deployment
chmod +x deploy.sh
./deploy.sh
```

#### Option C: Manual deployment via AWS Console

See [DEPLOY_MANUAL.md](DEPLOY_MANUAL.md) for step-by-step instructions.

## Configuration

### Environment Variables

The Lambda function requires these environment variables:

- `UNIFI_API_KEY`: Your UniFi Cloud API key
- `HOSTED_ZONE_ID`: Route53 hosted zone ID
- `RECORD_NAME`: DNS record to update (e.g., home.example.com)
- `TTL`: DNS record TTL in seconds (default: 300)

### Schedule

By default, the function runs every 5 minutes. You can adjust this in `template.yaml`:

```yaml
ScheduleExpression: "rate(5 minutes)"
```

Other examples:
- `rate(1 minute)` - Every minute
- `rate(10 minutes)` - Every 10 minutes
- `rate(1 hour)` - Every hour

## IAM Permissions

The Lambda function requires these permissions:

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
        "arn:aws:route53:::hostedzone/YOUR_ZONE_ID",
        "arn:aws:route53:::change/*"
      ]
    }
  ]
}
```

## Testing

Test the function manually:

```bash
aws lambda invoke \
    --function-name UniFi-Route53-Updater \
    --payload '{}' \
    response.json

cat response.json
```

Expected output:

```json
{
  "statusCode": 200,
  "body": {
    "message": "DNS record updated successfully",
    "record": "home.example.com",
    "ip": "1.2.3.4",
    "changeId": "/change/C123456789"
  }
}
```

## Monitoring

View logs in CloudWatch:

```bash
aws logs tail /aws/lambda/UniFi-Route53-Updater --follow
```

Check your DNS record:

```bash
nslookup home.example.com
```

Or with AWS CLI:

```bash
aws route53 list-resource-record-sets \
    --hosted-zone-id YOUR_ZONE_ID \
    --query "ResourceRecordSets[?Name=='home.example.com.']"
```

## Cost Estimate

- **Lambda**: ~$0.00 (within free tier for 5-minute intervals)
- **Route53**: $0.50/month per hosted zone + $0.40 per million queries
- **Total**: ~$0.50/month

## Troubleshooting

### UniFi API Errors

- Verify your API key is correct
- Check that your UniFi device is online
- Ensure you have API access enabled

### Route53 Errors

- Verify IAM permissions are correct
- Check that the hosted zone ID is valid
- Ensure the record name matches your domain

### Lambda Errors

View detailed logs:

```bash
aws logs tail /aws/lambda/UniFi-Route53-Updater --follow
```

## Architecture

```
┌─────────────┐
│  EventBridge│
│   (5 min)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   Lambda    │─────▶│  UniFi API   │
│  Function   │      │ (Get Ext IP) │
└──────┬──────┘      └──────────────┘
       │
       ▼
┌─────────────┐
│  Route53    │
│ (Update DNS)│
└─────────────┘
```

## Development

### Project Structure

```
.
├── lambda_function.py      # Main Lambda handler
├── template.yaml           # SAM template
├── requirements.txt        # Python dependencies
├── deploy.sh              # Deployment script
├── README.md              # This file
├── DEPLOY_MANUAL.md       # Manual deployment guide
└── .gitignore             # Git ignore rules
```

### Local Testing

You can test the Lambda function locally:

```bash
sam local invoke UpdateDNSFunction --event event.json
```

## Security

- Never commit your API keys or credentials
- Use AWS Secrets Manager for production deployments
- Rotate your UniFi API key regularly
- Use least-privilege IAM policies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Built with [AWS SAM](https://aws.amazon.com/serverless/sam/)
- Uses [UniFi Cloud API](https://api.ui.com/)
- Inspired by dynamic DNS solutions

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review AWS CloudWatch logs for errors
