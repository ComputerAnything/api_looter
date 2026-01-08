# Security Policy

## Supported Versions

We actively maintain security updates for the latest version:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Security Features

api_looter implements multiple layers of security:

### Application Security
- ✅ **SSRF Protection**: Auto-whitelisted domains only (extracted from `data.py`)
- ✅ **Rate Limiting**: 10 POST requests/minute per IP globally (all APIs combined)
- ✅ **Input Validation**: 500 character limit on all parameters
- ✅ **Security Headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- ✅ **HTTPS Enforcement**: Production mode requires HTTPS
- ✅ **No XSS**: React-style template escaping + CSP headers
- ✅ **CORS Configuration**: Proper credential handling

### Infrastructure Security (Production)
- ✅ **Read-only filesystem**: Containers run with immutable root
- ✅ **Capability dropping**: Minimal Linux capabilities
- ✅ **Non-root user**: Containers don't run as root
- ✅ **Health checks**: Automatic restart on failures
- ✅ **Redis auth**: Password-protected rate limit storage
- ✅ **Network isolation**: Separate Docker networks

### Dependency Security
- ✅ **Dependabot**: Weekly automated dependency updates
- ✅ **CodeQL**: Automated code scanning
- ✅ **Bandit**: Python security linting
- ✅ **TruffleHog**: Secret scanning

## Reporting a Vulnerability

**Please DO NOT create public GitHub issues for security vulnerabilities.**

Instead, please report security issues privately:

1. **Email**: [Create a private security advisory on GitHub](https://github.com/ComputerAnything/api_looter/security/advisories/new)
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### What to Expect

- **Response time**: Within 48 hours
- **Updates**: Every 72 hours until resolved
- **Credit**: Security researchers will be credited (unless you prefer to remain anonymous)
- **Fix timeline**: Critical issues within 7 days, high within 14 days

## Security Best Practices for Contributors

When adding new APIs to `app/data.py`:

### ✅ Required Security Checks

1. **HTTPS Only**: Endpoints MUST use `https://` (not `http://`)
   - Exception: Legacy APIs like numbersapi.com (documented)

2. **No Private IPs**: Do NOT add:
   - `localhost`, `127.0.0.1`, `0.0.0.0`
   - Private IPs: `10.x.x.x`, `172.16.x.x`-`172.31.x.x`, `192.168.x.x`
   - Internal domains: `.internal`, `.corp`, `.lan`, `.local`

3. **Validate APIs**: Always run before committing:
   ```bash
   python validate_apis.py
   ```

4. **Test Locally**: Verify the API works:
   ```bash
   python run.py
   # Visit http://localhost:8000 and test your API
   ```

### ❌ Security Anti-Patterns

**Never add APIs that:**
- Require credentials in the URL
- Expose sensitive data (PII, credentials, secrets)
- Are known to have security vulnerabilities
- Return executable code (JavaScript, shell scripts)
- Allow arbitrary URL injection
- Can be used for DDoS amplification

### 🔍 Example: Secure API Entry

```python
{
    "id": 15,
    "name": "Safe Example API",
    "description": "Returns public data only.",
    "endpoint": "https://api.example.com/v1/public",  # ✅ HTTPS
    "parameters": [],
    "why_use": "Learn about public APIs.",
    "how_use": "Used for testing and education.",
    "category": "Data",
    "has_handler": False  # Set to True only if custom response parsing needed
}
```

**If adding a custom handler** (`has_handler: True`):
- Create handler function in `app/api_handlers.py`
- **MUST include SSRF protection**: `if not is_allowed_domain(endpoint):`
- **MUST use timeout**: `requests.get(..., timeout=10)`
- See existing handlers for examples

## Automated Security Checks

Every pull request is automatically scanned for:

- ✅ **API Validation**: `validate_apis.py` checks all security requirements
- ✅ **Code Quality**: Ruff linting
- ✅ **Security Scanning**: Bandit for Python security issues
- ✅ **Secret Detection**: TruffleHog scans for leaked credentials
- ✅ **Dependency Scan**: Snyk checks for vulnerable dependencies

PRs must pass all checks before merging.

## Security Update Process

1. **Discovery**: Vulnerability identified (internal or external report)
2. **Assessment**: Severity and impact evaluated
3. **Fix**: Patch developed and tested
4. **Release**: Security update published
5. **Disclosure**: Public disclosure after fix is deployed
6. **Credit**: Reporter credited in release notes

## Questions?

For security-related questions that are NOT vulnerabilities:
- Open a GitHub Discussion
- Email: support@computeranything.dev (public inquiries only)

---

**Last Updated**: January 2026
