# Contributing to api_looter

Thank you for your interest in contributing! 🎉

## How to Contribute

### Adding a New API (Most Common)

**This is the easiest way to contribute!** Just edit one file.

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/api_looter.git
   cd api_looter
   ```

3. **Create a branch**:
   ```bash
   git checkout -b add-your-api-name
   ```

4. **Edit `app/data.py`** - Add your API to the `APIS` list:
   ```python
   {
       "id": 15,  # Next available ID
       "name": "Your API Name",
       "description": "What this API does (1-2 sentences).",
       "endpoint": "https://api.example.com/v1/endpoint",
       "parameters": [  # Leave empty [] if no parameters
           {"name": "query", "label": "Search Query", "type": "text", "required": True}
       ],
       "why_use": "Why would a developer use this API? (Educational!)",
       "how_use": "How/when do developers commonly use this API?",
       "category": "Data"  # Images, Fun, Data, or Cryptocurrency
   },
   ```

5. **Validate your changes**:
   ```bash
   python validate_apis.py
   ```
   This checks:
   - ✅ HTTPS endpoint (not HTTP)
   - ✅ No localhost/private IPs
   - ✅ All required fields present
   - ✅ Educational fields filled in
   - ✅ No security issues

6. **Test locally**:
   ```bash
   cp .env.development .env
   python run.py
   ```
   - Visit http://localhost:8000
   - Find your API in the list
   - Click on it and test it works!

7. **Commit and push**:
   ```bash
   git add app/data.py
   git commit -m "Add Your API Name"
   git push origin add-your-api-name
   ```

8. **Open a Pull Request** on GitHub

That's it! The domain whitelist auto-updates from your endpoint. ✨

---

## API Requirements

### ✅ Required
- **Free to use** (no paid subscription)
- **Publicly accessible** (no special access needed)
- **HTTPS endpoint** (not HTTP, except documented legacy APIs)
- **Family-friendly** (no adult/offensive content)
- **Educational value** (helps people learn about APIs)
- **Working** (you tested it!)

### ❌ Not Accepted
- Localhost/private IP endpoints
- APIs requiring payment
- APIs with adult/offensive content
- Broken/deprecated APIs
- APIs without documentation

---

## Parameter Types

### Text Input
```python
{"name": "search", "label": "Search Query", "type": "text", "required": True}
```

### Dropdown/Select
```python
{
    "name": "category",
    "label": "Category",
    "type": "select",
    "required": True,
    "options": [
        {"value": "option1", "label": "Option 1"},
        {"value": "option2", "label": "Option 2"}
    ]
}
```

---

## Custom Handlers (Advanced - Rarely Needed)

**95% of APIs don't need this!** The default handler works for most APIs.

Only needed if your API has a very unusual response format.

See `app/api_helpers.py` for examples, then update `app/routes.py`.

---

## Other Contributions

### Bug Fixes
1. Create an issue describing the bug
2. Fork and create a branch: `fix-issue-123`
3. Fix the bug
4. Add a test if possible
5. Submit a PR

### Documentation
1. Fork the repository
2. Update documentation files
3. Submit a PR

### Security Issues
**DO NOT create public issues!**
See [SECURITY.md](SECURITY.md) for reporting process.

---

## Development Setup

### Local Development
```bash
# Clone
git clone https://github.com/ComputerAnything/api_looter.git
cd api_looter

# Setup environment
cp .env.development .env

# Install dependencies (optional, use virtual env)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python run.py
# Visit: http://localhost:8000
```

### Code Quality
```bash
# Lint code
ruff check .

# Validate APIs
python validate_apis.py

# Format code
ruff format .
```

---

## Pull Request Process

1. **Automated Checks**: Your PR will be automatically checked for:
   - API validation (security, format, etc.)
   - Code linting
   - Security scanning
   - Secret detection

2. **Review**: Maintainers will review your contribution

3. **Merge**: Once approved and checks pass, we'll merge!

4. **Recognition**: You'll be credited in the release notes ✨

---

## Style Guidelines

- **Python**: Follow PEP 8 (enforced by ruff)
- **Comments**: Explain *why*, not *what*
- **Commit messages**: Clear and descriptive
  - Good: "Add Cat Facts API with description"
  - Bad: "update"

---

## Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open an issue with the bug report template
- **Feature ideas**: Open an issue with the feature request template
- **Security**: See [SECURITY.md](SECURITY.md)

---

## Code of Conduct

Be respectful, inclusive, and helpful. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## License

By contributing, you agree your contributions will be licensed under the MIT License.

---

Thank you for making api_looter better! 🚀
