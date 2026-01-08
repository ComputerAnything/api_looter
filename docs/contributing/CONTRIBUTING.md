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
       "parameters": [],  # Leave empty [] if no parameters needed
       "why_use": "Why would a developer use this API? (Educational!)",
       "how_use": "How/when do developers commonly use this API?",
       "category": "Data",  # Images, Fun, Data, or Cryptocurrency
       "has_handler": False  # Set to True only if you need custom response parsing (see below)
   },
   ```

   **With parameters example:**
   ```python
   {
       "id": 15,
       "name": "Weather API",
       "description": "Get weather data for any city.",
       "endpoint": "https://api.weather.com/v1/current",
       "parameters": [
           {"name": "city", "label": "City Name", "type": "text", "required": True}
       ],
       "why_use": "Learn how to work with real-time weather data in applications.",
       "how_use": "Used in weather apps, travel sites, and location-based services.",
       "category": "Data",
       "has_handler": False
   },
   ```

5. **Validate your changes**:
   ```bash
   python validate_apis.py
   ```
   This checks:
   - ✅ HTTPS endpoint (not HTTP, except Numbers API)
   - ✅ No localhost/private IPs
   - ✅ No internal domains (.internal, .corp, etc.)
   - ✅ All required fields present
   - ✅ Educational fields filled in
   - ✅ No security issues
   - ✅ Endpoint domain is accessible

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
- **HTTPS endpoint** (not HTTP, except documented legacy APIs like Numbers API)
- **Family-friendly** (appropriate for general audiences)
- **Educational value** (helps people learn about APIs)
- **Working** (you tested it!)

### ❌ Not Accepted
- Localhost/private IP endpoints
- APIs requiring payment
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

## Custom Handlers (Advanced - Optional)

**Most APIs don't need custom handlers!** The default handler shows the full JSON response.

### When to Use a Custom Handler

Use `"has_handler": True` if you want to **extract specific fields** from the API response for a cleaner display.

**Example - Without custom handler** (`has_handler: False`):
```json
{
  "slip": {
    "id": 123,
    "advice": "Don't be a dick"
  }
}
```

**Example - With custom handler** (`has_handler: True`):
```
Don't be a dick
```

### How to Add a Custom Handler

1. **Set `has_handler: True` in `app/data.py`**:
   ```python
   {
       "id": 15,
       "name": "Cat Facts",
       "has_handler": True,  # ← Enable custom handler
       # ... other fields
   }
   ```

2. **Create handler function in `app/api_handlers.py`**:

   The function name must follow this pattern:
   - API name: "Cat Facts" → Function: `handle_cat_facts_api`
   - API name: "Dog CEO" → Function: `handle_dog_ceo_api`
   - API name: "Kanye Rest" → Function: `handle_kanye_rest_api`

   ```python
   def handle_cat_facts_api(api, params=None):
       """Custom handler for Cat Facts API"""
       endpoint = api['endpoint']

       # SSRF Protection - always include this!
       if not is_allowed_domain(endpoint):
           return "This API endpoint is not allowed for security reasons.", "error"

       response = requests.get(endpoint, headers={"Accept": "application/json"}, timeout=10)

       try:
           data = response.json()
           # Extract the specific field you want
           fact = data["fact"]
           return fact, "text"  # Return as plain text
       except (KeyError, ValueError):
           return "Failed to parse API response.", "text"
   ```

3. **That's it!** The routing system automatically finds your handler based on the API name.

### Handler Return Types

Your handler should return a tuple: `(content, type)`

**Available types:**
- `"text"` - Plain text display
- `"json"` - Syntax-highlighted JSON
- `"image"` - Display an image URL
- `"joke"` - Special formatting for jokes (setup + delivery)
- `"error"` - Error message

**Examples:**

```python
# Plain text
return "This is a cat fact", "text"

# JSON
return json.dumps({"data": "value"}, indent=2), "json"

# Image URL
return "https://example.com/image.jpg", "image"

# Joke format
return {"setup": "Why did...", "delivery": "Because..."}, "joke"

# Error
return "API request failed", "error"
```

### Examples to Reference

Check these existing handlers in `app/api_handlers.py`:
- `handle_cat_facts_api` - Extracts a single field
- `handle_advice_slip_api` - Nested field extraction
- `handle_jokeapi` - Dynamic URL construction with parameters
- `handle_default_api` - The default handler (shows full JSON)

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

2. **Manual Review**: Maintainers will manually review your contribution for:
   - API quality and relevance
   - Appropriate content warnings (if needed)
   - Educational value

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
