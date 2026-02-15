# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-15

### Added
- Full dual WAN support with separate DNS records for WAN1 and WAN2
- New environment variable `RECORD_NAME_WAN2` for configuring second DNS record
- Dual API endpoint approach for reliable WAN IP detection:
  - `/v1/devices` endpoint for WAN1 IP (from gateway device)
  - `/v1/hosts` endpoint for WAN2 IP (from host information)
- Comprehensive documentation for dual WAN configuration
- Warning messages when WAN2 is configured but not available
- Enhanced response format showing both WAN IPs and their DNS records

### Changed
- Lambda function now queries two UniFi Cloud API endpoints instead of one
- Updated response format to include separate `wan1` and `wan2` objects
- Improved error handling and logging for dual WAN scenarios
- Enhanced README with dual WAN architecture diagrams and troubleshooting

### Fixed
- Reliable detection of both WAN interfaces on UniFi gateway devices
- Proper handling of single WAN configurations (backward compatible)

## [1.0.0] - Initial Release

### Added
- Basic Lambda function for updating Route53 DNS records
- UniFi Cloud API integration
- Single WAN support
- AWS SAM deployment templates
- EventBridge scheduled execution (5-minute intervals)
- Basic error handling and logging
