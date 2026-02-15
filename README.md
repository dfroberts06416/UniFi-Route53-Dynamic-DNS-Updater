# UniFi Route53 Dynamic DNS Updater

AWS Lambda function that automatically updates Route53 DNS records with your external IP addresses from UniFi Cloud API. Supports dual WAN configurations with separate DNS records for each WAN interface.

## Features

- 🔄 Automatically retrieves external IPs from UniFi Cloud API
- 🌐 Updates Route53 A records automatically
- 🔀 Full support for dual WAN configurations (WAN1 and WAN2)
- 🎯 Separate DNS records for each WAN interface
- ⏰ Runs on a schedule (default: every 5 minutes)
- 💰 Minimal cost (~$0.50/month)
- 🚀 Easy deployment with AWS SAM

## How It Works

The Lambda function queries two UniFi Cloud API endpoints to retrieve both WAN IP addresses:

1. **`/v1/devices`** - Retrieves WAN1 IP from your UniFi gateway device (USG, UDM, etc.)
2. **`/v1/hosts`** - Retrieves WAN2 IP from the top-level host information

This approach works reliably for dual WAN setups where both interfaces are active on the same gateway device.

## Prerequisites

- AWS Account with Route53 hosted zone
- UniFi Cloud account with API access
- UniFi gateway device (USG, UDM, UDM-Pro, etc.)
- AWS CLI configured
- AWS SAM CLI (optional, for deployment)
- Python 3.11+

## Supported UniFi Devices

This function works with UniFi gateway devices that report to UniFi Cloud:
- UniFi Security Gateway (USG)
- UniFi Security Gateway Pro (USG-Pro-4)
- UniFi Dream Machine (UDM)
- UniFi Dream Machine Pro (UDM-Pro)
- Other UniFi gateways with Cloud access enabled

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
export RECORD_NAME_WAN2="home-wan2.example.com"  # Optional, for dual WAN setups
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
- `RECORD_NAME`: DNS record to update for WAN1 (e.g., home.example.com)
- `RECORD_NAME_WAN2`: DNS record to update for WAN2 (optional, e.g., home-wan2.example.com)
- `TTL`: DNS record TTL in seconds (default: 300)

### Single WAN vs Dual WAN Configuration

**Single WAN Setup:**
- Only configure `RECORD_NAME`
- Leave `RECORD_NAME_WAN2` empty or unset
- The function will update only the WAN1 record

**Dual WAN Setup:**
- Configure both `RECORD_NAME` and `RECORD_NAME_WAN2`
- The function will update both DNS records with their respective IPs
- WAN1 IP is retrieved from your gateway device in `/v1/devices`
- WAN2 IP is retrieved from the host information in `/v1/hosts`

If `RECORD_NAME_WAN2` is configured but WAN2 is not available, the function will update only WAN1 and include a warning in the response.

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
    response.json

cat response.json
```

Expected output (single WAN):

```json
{
  "statusCode": 200,
  "body": {
    "message": "DNS record(s) updated successfully",
    "wan1": {
      "record": "home.example.com",
      "ip": "1.2.3.4"
    },
    "changeId": "/change/C123456789"
  }
}
```

Expected output (dual WAN):

```json
{
  "statusCode": 200,
  "body": {
    "message": "DNS record(s) updated successfully",
    "wan1": {
      "record": "home.example.com",
      "ip": "1.2.3.4"
    },
    "wan2": {
      "record": "home-wan2.example.com",
      "ip": "5.6.7.8"
    },
    "changeId": "/change/C123456789"
  }
}
```

Expected output (WAN2 configured but not available):

```json
{
  "statusCode": 200,
  "body": {
    "message": "DNS record(s) updated successfully",
    "wan1": {
      "record": "home.example.com",
      "ip": "1.2.3.4"
    },
    "changeId": "/change/C123456789",
    "warning": "WAN2 record configured but no second WAN interface found in UniFi device"
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
- Check that your UniFi device is online and connected to UniFi Cloud
- Ensure you have API access enabled in your UniFi account

### Route53 Errors

- Verify IAM permissions are correct
- Check that the hosted zone ID is valid
- Ensure the record names match your domain

### Dual WAN Issues

- Verify both WAN interfaces are configured and active on your UniFi gateway
- Check that your gateway device appears in the UniFi Cloud console
- The function retrieves WAN1 from `/v1/devices` and WAN2 from `/v1/hosts`
- If only one WAN is active, only that record will be updated

### Lambda Errors

View detailed logs:

```bash
aws logs tail /aws/lambda/UniFi-Route53-Updater --follow
```

## How the Dual WAN Detection Works

The Lambda function uses a two-endpoint approach to retrieve both WAN IP addresses:

1. **WAN1 Detection:**
   - Queries UniFi Cloud API endpoint: `https://api.ui.com/v1/devices`
   - Searches for your gateway device (USG, UDM, etc.) by looking for devices with:
     - `productLine` = "network"
     - `model` contains "USG" or similar gateway identifiers
   - Extracts the `ip` field from the gateway device

2. **WAN2 Detection:**
   - Queries UniFi Cloud API endpoint: `https://api.ui.com/v1/hosts`
   - Retrieves the top-level `ipAddress` field
   - This typically represents the secondary/backup WAN interface

This approach works because UniFi Cloud reports different WAN interfaces through different API endpoints, allowing the function to retrieve both IPs reliably.

## Architecture

### Single WAN
```
┌─────────────┐
│  EventBridge│
│   (5 min)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   Lambda    │─────▶│  UniFi API   │
│  Function   │      │   /devices   │
└──────┬──────┘      └──────────────┘
       │
       ▼
┌─────────────┐
│  Route53    │
│ (Update DNS)│
└─────────────┘
```

### Dual WAN
```
┌─────────────┐
│  EventBridge│
│   (5 min)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────────┐
│   Lambda    │─────▶│  UniFi API   │
│  Function   │      │   /devices   │ (WAN1)
│             │      └──────────────┘
│             │      ┌──────────────┐
│             │─────▶│  UniFi API   │
│             │      │    /hosts    │ (WAN2)
└──────┬──────┘      └──────────────┘
       │
       ▼
┌─────────────┐
│  Route53    │
│ (Update 2   │
│  DNS Records)│
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
