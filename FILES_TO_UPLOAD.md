# Files Safe for GitHub Upload

## ✅ Safe to Upload (Sanitized)

These files have been sanitized and are safe to upload to a public GitHub repository:

### Core Files
- `lambda_function.py` - Lambda handler (no sensitive data)
- `template.yaml` - SAM template (no sensitive data)
- `requirements.txt` - Python dependencies

### Documentation
- `README_GITHUB.md` - Main README (rename to README.md when uploading)
- `DEPLOY_MANUAL.md` - Manual deployment guide (sanitized)
- `LICENSE` - MIT License

### Configuration
- `deploy.sh` - Deployment script (sanitized, empty placeholders)
- `config.example.sh` - Example configuration file
- `.gitignore` - Git ignore rules

## ❌ DO NOT Upload

These files contain sensitive information and should NOT be uploaded:

- `response.json` - May contain your actual IP address
- `ip-ranges.json` - AWS IP ranges (large file, not needed)
- `ip-ranges.csv` - Parsed IP ranges (not needed)
- `parse_ip_ranges.py` - Not related to this project
- `.aws-sam/` - Build artifacts
- `config.local.sh` - If you created it with real credentials
- Any files with your actual:
  - API keys
  - Hosted Zone IDs
  - Domain names
  - IP addresses

## 📝 Before Uploading

1. **Review each file** to ensure no sensitive data
2. **Rename README_GITHUB.md** to README.md
3. **Delete or don't commit**:
   - `response.json`
   - `ip-ranges.json`
   - `ip-ranges.csv`
   - `parse_ip_ranges.py`
   - `.aws-sam/` directory
   - Original `README.md` (has your data)

## 🚀 Upload Checklist

- [ ] Reviewed all files for sensitive data
- [ ] Renamed README_GITHUB.md to README.md
- [ ] Added .gitignore
- [ ] Removed response.json and other test files
- [ ] Verified deploy.sh has empty placeholders
- [ ] Verified DEPLOY_MANUAL.md is sanitized
- [ ] Added LICENSE file
- [ ] Added config.example.sh

## 📦 Recommended GitHub Repository Structure

```
unifi-route53-updater/
├── .gitignore
├── LICENSE
├── README.md (renamed from README_GITHUB.md)
├── DEPLOY_MANUAL.md
├── lambda_function.py
├── template.yaml
├── requirements.txt
├── deploy.sh
└── config.example.sh
```

## 🔒 Security Notes

- The sanitized files use placeholders like:
  - `YOUR_API_KEY`
  - `YOUR_ZONE_ID`
  - `your-domain.example.com`
  - `1.2.3.4` (example IP)
  
- Users will need to replace these with their own values
- config.local.sh is gitignored to prevent accidental commits
