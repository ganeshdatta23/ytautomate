# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainer privately
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Best Practices

### API Keys

- Never commit API keys to the repository
- Use `.env` files (already in `.gitignore`)
- Use GitHub Secrets for CI/CD
- Rotate keys regularly

### YouTube OAuth

- Keep `client_secret.json` private
- Never share `token.pickle`
- Use OAuth 2.0 flow properly

### Dependencies

- Keep dependencies updated
- Review `requirements.txt` regularly
- Use `pip install --upgrade` cautiously

## Disclosure Policy

- We will acknowledge receipt within 48 hours
- We will provide a fix timeline within 7 days
- We will credit reporters (unless they prefer anonymity)

Thank you for helping keep this project secure! 🔒
