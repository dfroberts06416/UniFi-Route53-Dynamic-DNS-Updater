#!/bin/bash

# Deployment script for UniFi Route53 Updater Lambda

# Configuration
STACK_NAME="unifi-route53-updater"
UNIFI_API_KEY=""    # Set your Unifi API Key 
HOSTED_ZONE_ID=""  # Set your hosted zone ID
RECORD_NAME=""     # Set your DNS record for WAN1 (e.g., home.example.com)
RECORD_NAME_WAN2="" # Set your DNS record for WAN2 (optional, e.g., home-wan2.example.com)
TTL="300"
SCHEDULE="rate(5 minutes)"

# Check if AWS SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "AWS SAM CLI not found. Installing..."
    pip install aws-sam-cli
fi

# Validate template
echo "Validating SAM template..."
sam validate

# Build the application
echo "Building Lambda function..."
sam build

# Deploy the application
echo "Deploying to AWS..."
sam deploy \
    --stack-name $STACK_NAME \
    --region us-east-1 \
    --parameter-overrides \
        UniFiApiKey=$UNIFI_API_KEY \
        HostedZoneId=$HOSTED_ZONE_ID \
        RecordName=$RECORD_NAME \
        RecordNameWan2=$RECORD_NAME_WAN2 \
        TTL=$TTL \
        ScheduleExpression="$SCHEDULE" \
    --capabilities CAPABILITY_IAM \
    --resolve-s3

echo "Deployment complete!"
