# Release Notes - Version 2.0.0

## Dual WAN Support Release

This major release adds full support for dual WAN configurations, allowing you to update separate DNS records for each WAN interface on your UniFi gateway.

### 🎉 What's New

#### Dual WAN Support
- Configure separate DNS records for WAN1 and WAN2 interfaces
- Automatic detection of both WAN IP addresses from UniFi Cloud API
- Simultaneous updates to both Route53 DNS records
- Backward compatible with single WAN setups

#### Enhanced API Integration
- Dual endpoint approach for reliable IP detection:
  - `/v1/devices` - Retrieves WAN1 IP from gateway device
  - `/v1/hosts` - Retrieves WAN2 IP from host information
- Works with all UniFi gateway devices (USG, UDM, UDM-Pro, etc.)

#### Improved Response Format
```json
{
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
```

### 📋 Configuration

#### New Environment Variable
- `RECORD_NAME_WAN2` - DNS record for WAN2 interface (optional)

#### Example Configuration
```bash
# Single WAN
RECORD_NAME=home.example.com

# Dual WAN
RECORD_NAME=home.example.com
RECORD_NAME_WAN2=home-wan2.example.com
```

### 🔧 Deployment

#### New Deployment
```bash
sam build --region us-east-1
sam deploy --guided
```

#### Updating Existing Deployment
If you already have the Lambda function deployed:

1. Update the code:
```bash
sam build --region us-east-1
sam deploy
```

2. Add the WAN2 environment variable via AWS Console:
   - Go to Lambda → UniFi-Route53-Updater
   - Configuration → Environment variables
   - Add: `RECORD_NAME_WAN2` = `your-wan2-record.example.com`

### 📚 Documentation Updates

- Comprehensive dual WAN setup guide
- Architecture diagrams for single and dual WAN
- Troubleshooting section for dual WAN issues
- API endpoint documentation
- Contributing guidelines

### 🐛 Bug Fixes

- Fixed WAN IP detection for various UniFi gateway models
- Improved error handling for API failures
- Better logging for debugging

### ⚠️ Breaking Changes

None - This release is fully backward compatible with single WAN configurations.

### 🔒 Security

- No sensitive data in repository
- All credentials via environment variables
- Follows AWS security best practices

### 📝 Files Changed

- `lambda_function.py` - Core dual WAN logic
- `template.yaml` - Added WAN2 parameter
- `README.md` - Comprehensive documentation
- `config.example.sh` - Example configuration
- `deploy.sh` - Updated deployment script
- `.gitignore` - Enhanced security patterns

### 🙏 Acknowledgments

Thanks to all users who requested dual WAN support and provided feedback!

### 📖 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete version history.
