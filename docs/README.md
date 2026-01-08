# API Looter - Documentation

Educational collection of free APIs with preview functionality and enterprise-grade security.

---

## 📚 Documentation Index

### Getting Started
- **[Development Guide](setup/DEVELOPMENT.md)** - Local development setup and workflow
- **[Production Deployment](setup/PRODUCTION.md)** - Deploying to production with Docker
- **[Environment Setup](setup/ENVIRONMENTS.md)** - Managing dev/staging/production environments

### Security
- **[Security Documentation](security/SECURITY.md)** - Complete security architecture
  - SSRF Protection (Domain Whitelist)
  - Rate Limiting
  - Security Headers (CSP, HSTS, etc.)
  - Input Validation
  - And more...

### Contributing
- **[Contributing Guide](contributing/CONTRIBUTING.md)** - How to add new APIs
- **[Code of Conduct](contributing/CODE_OF_CONDUCT.md)** - Community standards

### CI/CD
- **[GitHub Actions](ci-cd/WORKFLOWS.md)** - Automated validation and security scanning

---

## 🚀 Quick Links

### Development

```bash
# Start development server (no Docker needed)
cp .env.development .env
python run.py
```

**App:** http://localhost:8000

### Contributing an API

**Just edit one file!** - `app/data.py`

The domain whitelist auto-extracts from your endpoint. See [CONTRIBUTING.md](contributing/CONTRIBUTING.md) for details.

---

## 🔐 Security Highlights

This application implements **enterprise-grade security** despite being a simple educational tool:

- ✅ **SSRF Protection** - Auto-generated domain whitelist
- ✅ **Rate Limiting** - 30 requests/minute (Redis-backed)
- ✅ **Security Headers** - CSP, HSTS, X-Frame-Options, and more
- ✅ **Input Validation** - Parameter length limits, type checking
- ✅ **No Database** - Zero SQL injection risk (static data)
- ✅ **Automated Security Scanning** - CodeQL, Dependabot, Bandit

**Security Score:** Enterprise-grade for a simple educational app

See [Security Documentation](security/SECURITY.md) for complete details.

---

## 📊 Architecture

### Technology Stack

**Backend:**
- Flask (Python web framework)
- Flask-Limiter (rate limiting)
- Flask-WTF (CSRF protection)
- Gunicorn (production WSGI server)
- Redis (rate limit storage)

**Infrastructure:**
- Docker + Docker Compose
- Cloudflare Tunnel (HTTPS, DDoS protection)
- Static data structure (no database)

### Project Structure

```
api_looter/
├── app/
│   ├── __init__.py            # Flask app factory + security
│   ├── data.py                # Static API data (contributors edit this!)
│   ├── routes.py              # API endpoints
│   ├── api_handlers.py         # API call handlers
│   ├── static/                # CSS, JS, images
│   └── templates/             # HTML templates
│
├── docs/                      # Documentation (you are here!)
├── .github/workflows/         # CI/CD automation
├── validate_apis.py           # Security validation script
├── docker-compose.*.yml       # Docker configurations
└── run.py                     # Application entry point
```

---

## 🎯 Use Cases

This platform is ideal for:

- **Learning APIs** - Understand how APIs work by testing real endpoints
- **API Discovery** - Find free APIs for your projects
- **Educational Projects** - Reference implementation for Flask security
- **Beginner-Friendly** - No API keys required, instant testing
- **Open Source Reference** - Enterprise security patterns for simple apps

---

## 🛡️ OWASP Top 10 Coverage

This application addresses relevant OWASP Top 10 (2021) vulnerabilities:

1. **Broken Access Control** - Rate limiting prevents abuse
2. **Cryptographic Failures** - HTTPS, secure cookies, HSTS
3. **Injection** - No database (static data), input validation
4. **Insecure Design** - Defense-in-depth architecture
5. **Security Misconfiguration** - Comprehensive security headers
6. **Vulnerable Components** - Dependabot auto-updates
7. **Authentication Failures** - Rate limiting on all endpoints
8. **Data Integrity Failures** - Input validation, CSRF protection
9. **Logging Failures** - Security event logging (production)
10. **SSRF** - Domain whitelist, auto-extracted from endpoints

See [Security Documentation](security/SECURITY.md) for implementation details.

---

## 📊 API Collection

Current APIs: **14 free APIs**

**Categories:**
- 🖼️ **Images** - Dog CEO, Random Fox
- 🎉 **Fun** - Cat Facts, Dad Jokes, Kanye Quotes, Advice Slip, Jokes
- 📚 **Data** - Numbers API, Open Library, Genderize, Agify, Nationalize
- 💰 **Cryptocurrency** - CoinGecko

All APIs are:
- ✅ Free to use (no paid subscription)
- ✅ Publicly accessible (no API key required)
- ✅ HTTPS-only (except Numbers API - HTTP allowed)
- ✅ Family-friendly
- ✅ Educational value

---

## 🤝 Contributing

**Want to add an API?**

1. Edit `app/data.py` (just one file!)
2. Add your API to the `APIS` list
3. Submit a PR
4. Automated validation checks security requirements
5. Done!

The domain whitelist auto-extracts from your endpoint - no manual updates needed.

See [CONTRIBUTING.md](contributing/CONTRIBUTING.md) for step-by-step guide.

---

## 📞 Support

- **Security Issues:** See [SECURITY.md](security/SECURITY.md)
- **Bug Reports:** GitHub Issues
- **Feature Requests:** GitHub Issues
- **Questions:** GitHub Discussions

---

## 📝 License

See LICENSE file for details.

---

*Documentation Last Updated: January 2026*
*Application Version: 2.0 (Database-less refactor)*
