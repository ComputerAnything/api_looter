#!/usr/bin/env python3
"""
API Validation Script - Enforces security and quality standards
Run this before committing changes to data.py
"""

import sys
import re
from urllib.parse import urlparse
from typing import List, Tuple
import ipaddress


def validate_apis():
    """Validate all APIs in data.py for security and quality"""
    # Import the APIS list
    sys.path.insert(0, '.')
    from app.data import APIS

    errors = []
    warnings = []

    print("🔍 Validating APIs...")
    print(f"Found {len(APIS)} APIs to validate\n")

    seen_ids = set()
    seen_names = set()
    seen_endpoints = set()

    for idx, api in enumerate(APIS):
        api_num = idx + 1
        api_name = api.get('name', f'API #{api_num}')

        # 1. SECURITY: Check required fields
        required_fields = ['id', 'name', 'description', 'endpoint', 'parameters', 'why_use', 'how_use', 'category']
        for field in required_fields:
            if field not in api:
                errors.append(f"❌ {api_name}: Missing required field '{field}'")

        # 2. SECURITY: Validate endpoint URL
        endpoint = api.get('endpoint', '')
        if not endpoint:
            errors.append(f"❌ {api_name}: Endpoint cannot be empty")
            continue

        try:
            parsed = urlparse(endpoint)

            # SECURITY: Must use HTTPS (not HTTP)
            if parsed.scheme != 'https':
                # Allow http only for numbersapi.com (legacy API)
                if 'numbersapi.com' not in parsed.netloc:
                    errors.append(f"❌ {api_name}: Endpoint must use HTTPS, not {parsed.scheme}://")
                else:
                    warnings.append(f"⚠️  {api_name}: Using HTTP (legacy API - consider finding HTTPS alternative)")

            # SECURITY: Check for valid domain
            if not parsed.netloc:
                errors.append(f"❌ {api_name}: Invalid endpoint URL (no domain)")
                continue

            # SECURITY: Block localhost, private IPs, and internal networks
            domain = parsed.netloc.split(':')[0]  # Remove port if present

            # Check if it's an IP address
            try:
                ip = ipaddress.ip_address(domain)
                if ip.is_private or ip.is_loopback or ip.is_link_local:
                    errors.append(f"❌ {api_name}: Cannot use private/localhost IP addresses: {domain}")
            except ValueError:
                # Not an IP, it's a domain - that's good
                pass

            # SECURITY: Block localhost domains
            localhost_patterns = ['localhost', '127.0.0.1', '0.0.0.0', '::1', 'local.', '.local']
            if any(pattern in domain.lower() for pattern in localhost_patterns):
                errors.append(f"❌ {api_name}: Cannot use localhost/local domains: {domain}")

            # SECURITY: Block internal domains
            internal_patterns = ['.internal', '.corp', '.lan', '.home']
            if any(domain.lower().endswith(pattern) for pattern in internal_patterns):
                errors.append(f"❌ {api_name}: Cannot use internal domains: {domain}")

        except Exception as e:
            errors.append(f"❌ {api_name}: Invalid endpoint URL: {e}")

        # 3. Check for duplicate IDs
        api_id = api.get('id')
        if api_id in seen_ids:
            errors.append(f"❌ {api_name}: Duplicate ID {api_id}")
        seen_ids.add(api_id)

        # 4. Check for duplicate names
        if api_name in seen_names:
            errors.append(f"❌ Duplicate API name: {api_name}")
        seen_names.add(api_name)

        # 5. Check for duplicate endpoints
        if endpoint in seen_endpoints:
            warnings.append(f"⚠️  {api_name}: Duplicate endpoint (may be intentional): {endpoint}")
        seen_endpoints.add(endpoint)

        # 6. Validate ID sequence
        expected_id = idx + 1
        if api_id != expected_id:
            warnings.append(f"⚠️  {api_name}: ID is {api_id}, expected {expected_id} (should be sequential)")

        # 7. Check educational fields are filled
        if not api.get('why_use') or len(api.get('why_use', '').strip()) < 10:
            errors.append(f"❌ {api_name}: 'why_use' field is too short (min 10 characters)")

        if not api.get('how_use') or len(api.get('how_use', '').strip()) < 10:
            errors.append(f"❌ {api_name}: 'how_use' field is too short (min 10 characters)")

        # 8. Validate category
        valid_categories = ['Images', 'Fun', 'Data', 'Cryptocurrency']
        category = api.get('category', '')
        if category and category not in valid_categories:
            warnings.append(f"⚠️  {api_name}: New category '{category}' (valid: {', '.join(valid_categories)})")

        # 9. Validate parameters structure
        params = api.get('parameters', [])
        if not isinstance(params, list):
            errors.append(f"❌ {api_name}: 'parameters' must be a list")
        else:
            for pidx, param in enumerate(params):
                if not isinstance(param, dict):
                    errors.append(f"❌ {api_name}: Parameter #{pidx+1} must be a dictionary")
                    continue

                # Check required parameter fields
                param_required = ['name', 'label', 'type', 'required']
                for field in param_required:
                    if field not in param:
                        errors.append(f"❌ {api_name}: Parameter '{param.get('name', pidx+1)}' missing field '{field}'")

                # Validate parameter types
                param_type = param.get('type', '')
                if param_type not in ['text', 'select']:
                    errors.append(f"❌ {api_name}: Parameter '{param.get('name')}' has invalid type '{param_type}' (must be 'text' or 'select')")

                # If select, must have options
                if param_type == 'select':
                    if 'options' not in param or not param['options']:
                        errors.append(f"❌ {api_name}: Select parameter '{param.get('name')}' must have 'options'")

        # 10. SECURITY: Check for suspicious content in descriptions
        suspicious_keywords = ['<script', 'javascript:', 'onclick', 'onerror', 'eval(']
        for field in ['name', 'description', 'why_use', 'how_use']:
            value = str(api.get(field, '')).lower()
            for keyword in suspicious_keywords:
                if keyword in value:
                    errors.append(f"❌ {api_name}: Suspicious content in '{field}': {keyword}")

    # Print results
    print("\n" + "="*60)
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  {error}")
        print("\n" + "="*60)
        print(f"\n💥 VALIDATION FAILED: {len(errors)} error(s) found")
        return False
    else:
        print(f"\n✅ VALIDATION PASSED!")
        print(f"   - {len(APIS)} APIs validated")
        print(f"   - {len(warnings)} warning(s)")
        print("="*60)
        return True


def extract_domains():
    """Extract all unique domains from API endpoints"""
    sys.path.insert(0, '.')
    from app.data import APIS

    domains = set()
    for api in APIS:
        endpoint = api.get('endpoint', '')
        if endpoint:
            try:
                parsed = urlparse(endpoint)
                if parsed.netloc:
                    domains.add(parsed.netloc)
            except:
                pass

    return sorted(domains)


if __name__ == '__main__':
    print("🔒 API Security Validator\n")

    # Run validation
    success = validate_apis()

    # Show extracted domains
    print("\n📋 Extracted domains (for ALLOWED_API_DOMAINS):")
    domains = extract_domains()
    print(f"   {domains}\n")

    # Exit with appropriate code
    sys.exit(0 if success else 1)
