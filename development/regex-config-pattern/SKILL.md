---
name: regex-config-pattern
description: Generate regex patterns for config_manager.py save operations. Use when adding config save logic, creating regex for BobConfig.py updates, or troubleshooting config regex patterns.
allowed-tools: Read
---

# Regex Configuration Patterns

Generates the correct regex patterns for `config_manager.py` save operations that update BobConfig.py.

## When to Use

- Adding save logic to config_manager.py
- Creating regex patterns for new config parameters
- Troubleshooting regex matching issues
- Understanding the config save pattern

## Pattern Structure

All config saves follow this pattern:

```python
content = re.sub(
    r'PATTERN_TO_MATCH',
    f'REPLACEMENT_STRING',
    content
)
changes_made.append(f"PARAM_NAME = {value}")
```

## Type-Specific Patterns

### Boolean Parameters

**BobConfig.py:**
```python
FEATURE_ENABLED: bool = True
```

**Regex Pattern:**
```python
if 'feature_enabled' in section:
    content = re.sub(
        r'FEATURE_ENABLED:\s*bool\s*=\s*(True|False)',
        f'FEATURE_ENABLED: bool = {section["feature_enabled"]}',
        content
    )
    changes_made.append(f"FEATURE_ENABLED = {section['feature_enabled']}")
```

**Pattern Breakdown:**
- `FEATURE_ENABLED:` - Exact parameter name + colon
- `\s*` - Zero or more whitespace
- `bool` - Type annotation
- `\s*=\s*` - Equals sign with optional whitespace
- `(True|False)` - Either True or False (capture group)

### Integer Parameters

**BobConfig.py:**
```python
MAX_RETRIES: int = 3
```

**Regex Pattern:**
```python
if 'max_retries' in section:
    content = re.sub(
        r'MAX_RETRIES:\s*int\s*=\s*\d+',
        f'MAX_RETRIES: int = {section["max_retries"]}',
        content
    )
    changes_made.append(f"MAX_RETRIES = {section['max_retries']}")
```

**Pattern Breakdown:**
- `\d+` - One or more digits (matches any integer)

### Float Parameters

**BobConfig.py:**
```python
THRESHOLD: float = 0.5
PERCENTAGE: float = 10.0
```

**Regex Pattern:**
```python
if 'threshold' in section:
    content = re.sub(
        r'THRESHOLD:\s*float\s*=\s*[\d.]+',
        f'THRESHOLD: float = {float(section["threshold"])}',
        content
    )
    changes_made.append(f"THRESHOLD = {section['threshold']}")
```

**Pattern Breakdown:**
- `[\d.]+` - One or more digits or decimal points
- Note: `float()` conversion in f-string ensures proper formatting

**Important:** Always cast to float in f-string!
```python
# ✓ Correct
f'THRESHOLD: float = {float(section["threshold"])}'

# ✗ Wrong - may produce "0.5" vs "0.50"
f'THRESHOLD: float = {section["threshold"]}'
```

### String Parameters

**BobConfig.py:**
```python
MODEL_NAME: str = "default"
API_URL: str = "http://localhost:5000"
```

**Regex Pattern:**
```python
if 'model_name' in section:
    content = re.sub(
        r'MODEL_NAME:\s*str\s*=\s*"[^"]*"',
        f'MODEL_NAME: str = "{section["model_name"]}"',
        content
    )
    changes_made.append(f"MODEL_NAME = {section['model_name']}")
```

**Pattern Breakdown:**
- `"[^"]*"` - Matches string in double quotes
- `[^"]` - Any character except double quote
- `*` - Zero or more characters

**For single quotes:**
```python
r"MODEL_NAME:\s*str\s*=\s*'[^']*'"
f"MODEL_NAME: str = '{section[\"model_name\"]}'"
```

### Optional Parameters

**BobConfig.py:**
```python
API_KEY: Optional[str] = None
```

**Regex Pattern:**
```python
if 'api_key' in section:
    content = re.sub(
        r'API_KEY:\s*Optional\[str\]\s*=\s*(?:"[^"]*"|None)',
        f'API_KEY: Optional[str] = "{section["api_key"]}" if section["api_key"] else "None"',
        content
    )
    changes_made.append(f"API_KEY = {section['api_key']}")
```

**Pattern Breakdown:**
- `Optional\[str\]` - Type annotation (brackets escaped)
- `(?:"[^"]*"|None)` - Non-capturing group: either string or None
- `"[^"]*"` - String in quotes
- `|` - OR
- `None` - Literal None

### List Parameters

**BobConfig.py:**
```python
ALLOWED_MODELS: List[str] = ["model1", "model2"]
```

**Regex Pattern (Complex):**
```python
if 'allowed_models' in section:
    models_str = str(section["allowed_models"])  # Convert list to string
    content = re.sub(
        r'ALLOWED_MODELS:\s*List\[str\]\s*=\s*\[.*?\]',
        f'ALLOWED_MODELS: List[str] = {models_str}',
        content
    )
    changes_made.append(f"ALLOWED_MODELS = {len(section['allowed_models'])} items")
```

**Pattern Breakdown:**
- `\[.*?\]` - Matches list brackets with any content
- `.*?` - Non-greedy match (minimum characters)

## Common Pattern Variations

### With Comments

**BobConfig.py:**
```python
MAX_FPS: int = 30  # Maximum frames per second
```

**Regex (preserves comment):**
```python
r'MAX_FPS:\s*int\s*=\s*\d+(\s*#.*)?'
```

**Pattern Breakdown:**
- `(\s*#.*)?` - Optional group for comment
- `\s*#` - Whitespace + hash
- `.*` - Rest of comment
- `?` - Group is optional

### Multiline Parameters

**BobConfig.py:**
```python
LONG_LIST: List[str] = [
    "item1",
    "item2"
]
```

**Use re.DOTALL flag:**
```python
content = re.sub(
    r'LONG_LIST:\s*List\[str\]\s*=\s*\[.*?\]',
    f'LONG_LIST: List[str] = {value}',
    content,
    flags=re.DOTALL
)
```

## Complete Save Method Template

```python
def save_<section>_settings(self, settings: Dict) -> Dict:
    """Save <section> settings to BobConfig.py"""
    try:
        config_path = Path(__file__).parent.parent / 'BobConfig.py'

        if not config_path.exists():
            return {'success': False, 'message': f'Config file not found: {config_path}'}

        # Read current config
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        changes_made = []

        # Boolean parameter
        if 'bool_param' in settings['section']:
            content = re.sub(
                r'BOOL_PARAM:\s*bool\s*=\s*(True|False)',
                f'BOOL_PARAM: bool = {settings["section"]["bool_param"]}',
                content
            )
            changes_made.append(f"BOOL_PARAM = {settings['section']['bool_param']}")

        # Integer parameter
        if 'int_param' in settings['section']:
            content = re.sub(
                r'INT_PARAM:\s*int\s*=\s*\d+',
                f'INT_PARAM: int = {settings["section"]["int_param"]}',
                content
            )
            changes_made.append(f"INT_PARAM = {settings['section']['int_param']}")

        # Float parameter
        if 'float_param' in settings['section']:
            content = re.sub(
                r'FLOAT_PARAM:\s*float\s*=\s*[\d.]+',
                f'FLOAT_PARAM: float = {float(settings["section"]["float_param"])}',
                content
            )
            changes_made.append(f"FLOAT_PARAM = {settings['section']['float_param']}")

        # String parameter
        if 'str_param' in settings['section']:
            content = re.sub(
                r'STR_PARAM:\s*str\s*=\s*"[^"]*"',
                f'STR_PARAM: str = "{settings["section"]["str_param"]}"',
                content
            )
            changes_made.append(f"STR_PARAM = {settings['section']['str_param']}")

        if not changes_made:
            return {'success': False, 'message': 'No valid settings to update'}

        # Write updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Updated settings: {', '.join(changes_made)}")

        return {
            'success': True,
            'message': f'Settings saved. Updated: {", ".join(changes_made)}'
        }

    except Exception as e:
        logger.error(f"Error saving settings: {e}", exc_info=True)
        return {'success': False, 'message': f'Error: {str(e)}'}
```

## Testing Regex Patterns

**Python REPL Test:**
```python
import re

# Test content
content = "THRESHOLD: float = 0.5  # Detection threshold"

# Test pattern
pattern = r'THRESHOLD:\s*float\s*=\s*[\d.]+'
replacement = f'THRESHOLD: float = {float(10.0)}'

result = re.sub(pattern, replacement, content)
print(result)
# Output: THRESHOLD: float = 10.0  # Detection threshold
```

**Online Regex Tester:**
- https://regex101.com/ (Python flavor)
- Paste BobConfig.py line
- Test pattern
- Verify match and replacement

## Common Mistakes

### 1. Wrong Pattern for Float
```python
# ✗ Wrong - only matches integers
r'THRESHOLD:\s*float\s*=\s*\d+'

# ✓ Correct - matches floats with decimals
r'THRESHOLD:\s*float\s*=\s*[\d.]+'
```

### 2. Missing Float Conversion
```python
# ✗ Wrong - may lose precision
f'THRESHOLD: float = {value}'

# ✓ Correct - explicit float conversion
f'THRESHOLD: float = {float(value)}'
```

### 3. Greedy vs Non-Greedy
```python
# ✗ Wrong - matches too much (greedy)
r'PARAM:\s*str\s*=\s*".*"'  # Matches from first to LAST quote

# ✓ Correct - matches minimal (non-greedy)
r'PARAM:\s*str\s*=\s*"[^"]*"'  # Matches one string
```

### 4. Not Escaping Special Characters
```python
# ✗ Wrong - brackets are regex special chars
r'List[str]'

# ✓ Correct - escape brackets
r'List\[str\]'
```

### 5. Missing changes_made Entry
```python
# ✗ Wrong - silent success, no tracking
content = re.sub(pattern, replacement, content)

# ✓ Correct - track changes
content = re.sub(pattern, replacement, content)
changes_made.append(f"PARAM = {value}")
```

## Debugging Regex Issues

**Pattern doesn't match:**
1. Copy actual line from BobConfig.py
2. Test in regex101.com with Python flavor
3. Check for extra whitespace or comments
4. Verify type annotation exact spelling

**Match but wrong replacement:**
1. Check capture groups in pattern
2. Verify f-string uses correct variable
3. Test with print before writing file

**Multiple matches:**
1. Make pattern more specific (add context)
2. Use parameter name prefix (e.g., `VISION_THRESHOLD`)
3. Check for duplicates in BobConfig.py

## Quick Reference

| Type | Pattern | Example Match |
|------|---------|---------------|
| bool | `(True\|False)` | `True`, `False` |
| int | `\d+` | `42`, `100` |
| float | `[\d.]+` | `0.5`, `10.0` |
| str | `"[^"]*"` | `"value"` |
| Optional[str] | `(?:"[^"]*"\|None)` | `"value"` or `None` |
| List | `\[.*?\]` | `["a", "b"]` |

## Pro Tips

1. **Test patterns first** - Use regex101.com before coding
2. **Copy exact lines** - Use actual BobConfig.py content for testing
3. **Be specific** - Include parameter name to avoid false matches
4. **Track changes** - Always append to changes_made list
5. **Handle errors** - Wrap in try/except
6. **Log changes** - Use logger.info for change tracking
7. **Validate input** - Check types before regex
