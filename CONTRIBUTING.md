# Contributing to UniFi Route53 Dynamic DNS Updater

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

When reporting a bug, include:
- Your UniFi device model (USG, UDM, etc.)
- AWS Lambda runtime version
- Error messages and logs
- Steps to reproduce
- Expected vs actual behavior

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

#### Testing
- Test with both single and dual WAN configurations
- Verify error handling
- Check CloudWatch logs for issues
- Test with different UniFi device models if possible

#### Documentation
- Update README.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Add inline comments for complex code
- Update environment variable documentation

#### Security
- Never commit API keys, credentials, or sensitive data
- Use environment variables for configuration
- Follow AWS security best practices
- Report security issues privately

## Development Setup

1. Clone the repository
2. Install AWS SAM CLI: `pip install aws-sam-cli`
3. Configure AWS credentials
4. Copy `config.example.sh` to `config.local.sh` and add your values
5. Build: `sam build`
6. Test locally: `sam local invoke`

## Testing

### Local Testing
```bash
# Build the function
sam build

# Test locally with SAM
sam local invoke UpdateDNSFunction

# Run unit tests (if available)
python -m pytest tests/
```

### Integration Testing
```bash
# Deploy to test environment
sam deploy --guided

# Invoke the function
aws lambda invoke --function-name UniFi-Route53-Updater response.json

# Check logs
aws logs tail /aws/lambda/UniFi-Route53-Updater --follow
```

## Questions?

Feel free to open an issue for questions or discussions!
