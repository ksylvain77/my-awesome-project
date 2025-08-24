#!/usr/bin/env python3
"""
check-test-coverage.py: Enforce 4-phase test coverage for business logic features/endpoints.

Fails if any backend function or API endpoint is missing from any test phase.
Automatically excludes utility functions that don't need comprehensive testing.
"""
import sys
import os
import ast
import re

# --- Configuration ---
MODULES_DIR = 'modules'
TEST_SUITE = 'tests/test_suite.py'
API_FILE = 'hello_world_app.py'  # Will be replaced in generated project

# Functions matching these patterns are excluded from mandatory testing
EXCLUDE_PATTERNS = [
    '__init__',
    '__str__', 
    '__repr__',
    'format_response',
    'sanitize_filename', 
    'validate_input',
    'log_',
    'debug_',
    '_helper',
    '_util',
    'cleanup_',
    'setup_'
]

# Template escaping patterns to prevent regex parsing failures
TEMPLATE_ESCAPE_PATTERNS = [
    (r'\{\{[^}]*\}\}', '{{ VAR }}'),           # Jinja2 variables
    (r'\{%[^%]*%\}', '{% TAG %}'),             # Jinja2 tags
    (r'render_template_string\([^)]*\)', '""'), # Template strings
    (r'"""[^"]*\{\{[^}]*\}\}[^"]*"""', '""'),  # Multiline strings with templates
]

# --- Helper functions ---
def sanitize_for_parsing(content):
    """Remove template syntax that interferes with regex parsing"""
    for pattern, replacement in TEMPLATE_ESCAPE_PATTERNS:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return content

def should_exclude_function(func_name):
    """Exclude utility functions that don't need comprehensive testing"""
    return any(pattern in func_name for pattern in EXCLUDE_PATTERNS)

def get_functions_from_module(module_path):
    with open(module_path, 'r') as f:
        content = f.read()
    # Sanitize content to handle template strings before AST parsing
    sanitized_content = sanitize_for_parsing(content)
    try:
        tree = ast.parse(sanitized_content, filename=module_path)
        all_functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        # Filter out utility functions that don't need comprehensive testing
        return [f for f in all_functions if not should_exclude_function(f)]
    except SyntaxError as e:
        print(f"⚠️  Warning: Could not parse {module_path}: {e}")
        return []

def get_api_endpoints(api_path):
    endpoints = set()
    if not os.path.exists(api_path):
        return endpoints
    
    with open(api_path, 'r') as f:
        content = f.read()
    
    # Sanitize content before regex parsing
    sanitized_content = sanitize_for_parsing(content)
    
    for line in sanitized_content.split('\n'):
        m = re.search(r'@app\.route\(["\'](/api/[^"\']*)', line)
        if m:
            endpoints.add(m.group(1))
    return endpoints

def get_test_dict_keys(test_path, dict_name):
    with open(test_path, 'r') as f:
        content = f.read()
    m = re.search(rf'{dict_name}\s*=\s*{{(.*?)}}', content, re.DOTALL)
    if not m:
        return set()
    dict_body = m.group(1)
    keys = re.findall(r'"([^"]+)":', dict_body)
    return set(keys)

# --- Main check ---
def main():
    # Backend functions (excluding utility functions)
    all_backend_funcs = set()
    excluded_funcs = set()
    
    for fname in os.listdir(MODULES_DIR):
        if fname.endswith('.py'):
            module_path = os.path.join(MODULES_DIR, fname)
            with open(module_path, 'r') as f:
                tree = ast.parse(f.read(), filename=module_path)
            all_funcs = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            
            for func in all_funcs:
                if should_exclude_function(func):
                    excluded_funcs.add(func)
                else:
                    all_backend_funcs.add(func)
    
    # API endpoints
    api_endpoints = get_api_endpoints(API_FILE)
    
    # Test suite dicts
    backend_tests = get_test_dict_keys(TEST_SUITE, 'backend_tests')
    api_tests = get_test_dict_keys(TEST_SUITE, 'api_tests')
    contract_tests = get_test_dict_keys(TEST_SUITE, 'contract_tests')
    frontend_tests = get_test_dict_keys(TEST_SUITE, 'frontend_tests')
    
    # Check coverage
    missing_backend = all_backend_funcs - backend_tests
    missing_api = api_endpoints - api_tests
    missing_contract = api_endpoints - contract_tests
    missing_frontend = api_endpoints - frontend_tests
    
    # Report results
    if excluded_funcs:
        print(f"ℹ️  Excluded {len(excluded_funcs)} utility functions from testing requirements:")
        for func in sorted(excluded_funcs):
            print(f"    - {func}")
        print()
    
    errors = []
    if missing_backend:
        errors.append(f"Missing backend tests for: {sorted(missing_backend)}")
    if missing_api:
        errors.append(f"Missing API tests for: {sorted(missing_api)}")
    if missing_contract:
        errors.append(f"Missing contract tests for: {sorted(missing_contract)}")
    if missing_frontend:
        errors.append(f"Missing frontend tests for: {sorted(missing_frontend)}")
    
    if errors:
        print("❌ 4-Phase Test Coverage Check Failed:")
        for err in errors:
            print("  -", err)
        print(f"\nℹ️  Only business logic functions require comprehensive testing.")
        print(f"   Utility functions are automatically excluded.")
        sys.exit(1)
    
    print(f"✅ All {len(all_backend_funcs)} business logic functions and {len(api_endpoints)} endpoints have 4-phase test coverage!")
    if excluded_funcs:
        print(f"   ({len(excluded_funcs)} utility functions automatically excluded)")

if __name__ == '__main__':
    main()
