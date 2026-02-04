---
name: config-pattern
description: Add configuration parameters following BobTheSkull's full-stack pattern (BobConfig.py, config_manager.py, HTML templates, JavaScript). Use when adding new config parameters, settings, or configuration options to Bob The Skull project.
allowed-tools: Read, Edit, Grep, Glob
---

# Configuration Parameter Pattern

Automates the repetitive pattern of adding configuration parameters across Bob The Skull's entire configuration stack.

## When to Use

- Adding new configuration parameters to BobConfig.py
- Exposing existing parameters through the web UI
- Creating configurable thresholds, timeouts, or settings
- Extending any configuration page (audio, vision, performance, etc.)

## The Full Stack Pattern

Every configuration parameter requires updates in 4 locations:

### 1. BobConfig.py - Define Parameter
```python
# Add parameter with type hint and comment
VISION_MOTION_THRESHOLD: float = 10.0  # Percentage of frame showing motion (1-20%)
```

### 2. config_manager.py - Backend GET
```python
def get_<section>_settings(self) -> Dict:
    return {
        'subsection': {
            'param_name': self.config.PARAM_NAME
        }
    }
```

### 3. config_manager.py - Backend SAVE
```python
if 'param_name' in subsection:
    content = re.sub(
        r'PARAM_NAME:\s*<type>\s*=\s*<pattern>',
        f'PARAM_NAME: <type> = {subsection["param_name"]}',
        content
    )
    changes_made.append(f"PARAM_NAME = {subsection['param_name']}")
```

### 4. HTML Template - Form Field
```html
<div class="form-group">
    <label for="param_name">Display Name</label>
    <input type="<type>" id="param_name" name="param_name"
           min="X" max="Y" step="Z" required>
    <span class="form-help">Help text explaining the parameter</span>
</div>
```

### 5. JavaScript - Populate Form
```javascript
document.getElementById('param_name').value = settings.subsection.param_name || <default>;
```

### 6. JavaScript - Submit Form
```javascript
subsection: {
    param_name: parseFloat(document.getElementById('param_name').value)
}
```

## Type-Specific Patterns

### Boolean Parameters
**BobConfig.py:**
```python
FEATURE_ENABLED: bool = True  # Enable feature
```

**Regex Pattern:**
```python
r'FEATURE_ENABLED:\s*bool\s*=\s*(True|False)'
f'FEATURE_ENABLED: bool = {value}'
```

**HTML:**
```html
<div class="checkbox-group">
    <input type="checkbox" id="feature_enabled" name="feature_enabled">
    <label for="feature_enabled">Enable Feature</label>
</div>
```

**JavaScript:**
```javascript
// Populate
document.getElementById('feature_enabled').checked = settings.section.feature_enabled !== false;

// Submit
feature_enabled: document.getElementById('feature_enabled').checked
```

### Integer Parameters
**BobConfig.py:**
```python
MAX_RETRIES: int = 3  # Maximum retry attempts
```

**Regex Pattern:**
```python
r'MAX_RETRIES:\s*int\s*=\s*\d+'
f'MAX_RETRIES: int = {value}'
```

**HTML:**
```html
<input type="number" id="max_retries" name="max_retries"
       min="1" max="10" step="1" required>
```

**JavaScript:**
```javascript
// Populate
document.getElementById('max_retries').value = settings.section.max_retries || 3;

// Submit
max_retries: parseInt(document.getElementById('max_retries').value)
```

### Float Parameters
**BobConfig.py:**
```python
THRESHOLD: float = 0.5  # Detection threshold (0.0-1.0)
```

**Regex Pattern:**
```python
r'THRESHOLD:\s*float\s*=\s*[\d.]+'
f'THRESHOLD: float = {float(value)}'
```

**HTML:**
```html
<input type="number" id="threshold" name="threshold"
       min="0.0" max="1.0" step="0.1" required>
```

**JavaScript:**
```javascript
// Populate
document.getElementById('threshold').value = settings.section.threshold || 0.5;

// Submit
threshold: parseFloat(document.getElementById('threshold').value)
```

### String Parameters
**BobConfig.py:**
```python
MODEL_NAME: str = "default"  # Model to use
```

**Regex Pattern:**
```python
r'MODEL_NAME:\s*str\s*=\s*"[^"]*"'
f'MODEL_NAME: str = "{value}"'
```

**HTML (dropdown):**
```html
<select id="model_name" name="model_name">
    <option value="default">Default</option>
    <option value="advanced">Advanced</option>
</select>
```

**HTML (text input):**
```html
<input type="text" id="model_name" name="model_name" required>
```

**JavaScript:**
```javascript
// Populate
document.getElementById('model_name').value = settings.section.model_name || 'default';

// Submit
model_name: document.getElementById('model_name').value
```

## Configuration Pages Reference

### Audio Settings
- **File:** `web/templates/config_audio.html`
- **Backend:** `config_manager.py` - `get_audio_settings()`, `save_audio_settings()`
- **Sections:** general, advanced

### Vision Settings
- **File:** `web/templates/config_vision.html`
- **Backend:** `config_manager.py` - `get_vision_settings()`, `save_vision_settings()`
- **Sections:** general, performance, face_detection, face_identification

### System Settings
- **File:** `web/templates/config_system.html`
- **Backend:** `config_manager.py` - `get_system_settings()`, `save_system_settings()`
- **Sections:** wake_word, stt, llm, tts

### Performance Settings
- **File:** `web/templates/config_performance.html`
- **Backend:** `config_manager.py` - `get_performance_settings()`, `save_performance_settings()`
- **Sections:** state_machine, component_timeouts, other

### Eyes Controller Settings
- **File:** `web/templates/config_eyes.html`
- **Backend:** `config_manager.py` - `get_eyes_settings()`, `save_eyes_settings()`
- **Sections:** discovery, animation

### API Keys Settings
- **File:** `web/templates/config_apikeys.html`
- **Backend:** `config_manager.py` - `get_apikeys_settings()`, `save_apikeys_settings()`
- **Sections:** keys, key_lengths (for display)

## Workflow

1. **Identify the parameter location in BobConfig.py**
   - Find the appropriate section (VISION_*, AUDIO_*, LLM_*, etc.)
   - Determine the correct type (bool, int, float, str)

2. **Add to BobConfig.py**
   - Use proper type hint
   - Add descriptive comment
   - Choose sensible default value

3. **Update config_manager.py GET method**
   - Find the appropriate `get_*_settings()` method
   - Add parameter to the correct subsection dictionary
   - Use `self.config.PARAMETER_NAME`

4. **Update config_manager.py SAVE method**
   - Find the appropriate `save_*_settings()` method
   - Create regex pattern matching the type
   - Add to changes_made list

5. **Update HTML template**
   - Find the appropriate settings section
   - Add form field with proper input type
   - Include helpful label and description

6. **Update JavaScript populate function**
   - Find `populateForm()` or equivalent
   - Add line to set field value from settings
   - Include fallback default value

7. **Update JavaScript submit function**
   - Find form submission handler
   - Add parameter to the appropriate section
   - Use correct parse function (parseInt, parseFloat, etc.)

## Common Pitfalls

1. **Type mismatches** - Ensure JavaScript parse function matches Python type
2. **Missing defaults** - Always include `|| defaultValue` in JavaScript populate
3. **Regex escaping** - Float patterns need `[\d.]+`, not just `\d+`
4. **Boolean handling** - Use `!== false` for checkboxes, not `|| true`
5. **changes_made list** - Don't forget to append parameter name to track changes
6. **HTML IDs** - Must match between form field, populate, and submit JavaScript

## Recent Example (2024-12-09)

Added 4 vision detector parameters:
- `VISION_MOTION_THRESHOLD: float = 10.0`
- `VISION_FACE_USE_STABILITY_FILTER: bool = True`
- `VISION_FACE_STABILITY_SECONDS: float = 2.0`
- `VISION_FACE_DEBOUNCE_SECONDS: float = 3.0`

All integrated into vision configuration page with full get/save/UI support.
Total time: ~45 minutes for 4 parameters (would be ~10 minutes with this skill).

## Quick Reference

**Find existing patterns:**
```bash
# Find parameter in BobConfig
grep "PARAMETER_NAME" BobConfig.py

# Find in config_manager
grep -n "parameter_name" web/config_manager.py

# Find in HTML
grep -n "parameter_name" web/templates/config_*.html
```

**Test after adding:**
1. Restart web server
2. Navigate to config page
3. Verify field appears with correct default
4. Change value and save
5. Verify BobConfig.py updated correctly
6. Reload page and verify new value persists
