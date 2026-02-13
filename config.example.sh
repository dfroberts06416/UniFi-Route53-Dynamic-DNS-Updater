#!/bin/bash

# Example configuration file for UniFi Route53 Updater
# Copy this file to config.local.sh and fill in your values
# config.local.sh is gitignored for security

# Your UniFi API Key from https://account.ui.com/
export UNIFI_API_KEY="your-unifi-api-key-here"

# Your AWS Route53 Hosted Zone ID
export HOSTED_ZONE_ID="Z1234567890ABC"

# The DNS record name to update
export RECORD_NAME="home.example.com"

# DNS TTL in seconds
export TTL="300"

# How often to check for IP changes
export SCHEDULE="rate(5 minutes)"
