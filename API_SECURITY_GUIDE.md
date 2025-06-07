# API Key Security Guide

## ⚠️ IMPORTANT SECURITY NOTICE

This repository contains placeholders for API keys. **NEVER commit real API keys to version control!**

## Setting Up Your API Key Securely

### Method 1: Environment Variables (Recommended)

1. Create a `.env` file in the project root (already in .gitignore):
```bash
# .env file
GROQ_API_KEY=your_actual_api_key_here
```

2. The code will automatically load from environment variables

### Method 2: Direct Replacement (Less Secure)

1. Replace `"your_api_key_here"` with your actual API key in the code
2. **NEVER commit these changes to GitHub**
3. Use `git update-index --skip-worktree` to ignore local changes

## Getting Your Groq API Key

1. Go to [Groq Console](https://console.groq.com/keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key and use it in your project

## Security Checklist Before Pushing to GitHub

- [ ] No real API keys in any files
- [ ] `.env` file is in `.gitignore`
- [ ] All sensitive data is replaced with placeholders
- [ ] Verify with `git diff` before committing

## If You Accidentally Committed an API Key

1. **Immediately revoke the API key** in Groq Console
2. Generate a new API key
3. Remove the key from Git history:
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch filename' --prune-empty --tag-name-filter cat -- --all
   ```
4. Force push: `git push origin --force --all`

## Deployment Security

When deploying to platforms like Render, Railway, or Heroku:
- Use environment variables in the platform's dashboard
- Never hardcode keys in deployment files
- Use platform-specific secret management features
