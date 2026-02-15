#!/bin/bash

# Verification script to check for sensitive data before GitHub upload
# Run this before committing to ensure no credentials are exposed

echo "============================================================"
echo "Sanitization Verification Script"
echo "============================================================"
echo ""

ISSUES_FOUND=0

# Patterns to search for (potential sensitive data)
PATTERNS=(
    "gjK6FkydTn8cFEpPK4n0k28CL5xcx6us"  # API key pattern
    "Z08509852NYSK7DLFNTPM"              # Hosted Zone ID
    "remote.inlinecloud.io"              # Real DNS record
    "backup.inlinecloud.io"              # Real DNS record
    "32.216.218.147"                     # Real IP
    "174.168.77.50"                      # Real IP
    "dan.roberts@gmail.com"              # Email
    "Spire-CloudKey"                     # Device name
)

echo "Checking for sensitive data patterns..."
echo ""

for pattern in "${PATTERNS[@]}"; do
    echo "Searching for: $pattern"
    
    # Search in all tracked files (excluding .git directory)
    results=$(grep -r "$pattern" . --exclude-dir=.git --exclude-dir=.aws-sam --exclude-dir=__pycache__ --exclude="*.log" --exclude="verify_sanitization.sh" 2>/dev/null)
    
    if [ ! -z "$results" ]; then
        echo "  ⚠️  FOUND in:"
        echo "$results" | sed 's/^/    /'
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo "  ✓ Not found"
    fi
    echo ""
done

echo "============================================================"
echo "Verification Summary"
echo "============================================================"
echo ""

if [ $ISSUES_FOUND -eq 0 ]; then
    echo "✓ No sensitive data found!"
    echo "✓ Repository is ready for GitHub upload"
    exit 0
else
    echo "⚠️  Found $ISSUES_FOUND potential issue(s)"
    echo "⚠️  Please review and sanitize before uploading"
    exit 1
fi
