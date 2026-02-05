---
name: web-config-page
description: Create complete web configuration pages following Bob The Skull's aesthetic and patterns. Use when creating new config pages, adding settings pages, or extending the web configuration interface.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Web Configuration Page Creation

Creates complete configuration pages following Bob The Skull's established aesthetic, structure, and backend patterns.

## When to Use

- Creating new configuration pages
- Adding settings interfaces for new components
- Extending the web configuration dashboard
- Following the established Bob configuration UX pattern

## Configuration Page Structure

All config pages follow this pattern:

```
1. HTML Template      - web/templates/config_<name>.html
2. Flask Routes       - web/monitor_server.py (GET page, GET settings, POST save)
3. Backend Methods    - web/config_manager.py (get_<name>_settings, save_<name>_settings)
4. Dashboard Card     - web/templates/config_dashboard.html
5. Test Script        - test_<name>_config.py (optional but recommended)
```

## 1. HTML Template Pattern

```html
{% extends "base_config.html" %}

{% block title %}[Page Title] - Bob The Skull Configuration{% endblock %}

{% block config_content %}
    <div class="config-header">
        <h1>[PAGE TITLE]</h1>
        <p class="config-subtitle">[Brief description of what this page configures]</p>
    </div>

    <!-- Loading indicator -->
    <div id="loading" class="loading">
        <p>⏳ LOADING SETTINGS...</p>
    </div>

    <!-- Settings form -->
    <div id="settings-content" style="display: none;">
        <form id="[name]Form">
            <!-- Section 1 -->
            <div class="settings-section">
                <h2>[SECTION NAME]</h2>
                <p style="color: #00aa00; font-size: 0.85em; margin-bottom: 15px;">
                    [Section description]
                </p>

                <!-- Text/Number Input -->
                <div class="form-group">
                    <label for="param_name">[Display Name]</label>
                    <input type="[text|number]" id="param_name" name="param_name"
                           min="X" max="Y" step="Z" required>
                    <span class="form-help">[Help text explaining the parameter]</span>
                </div>

                <!-- Checkbox -->
                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="feature_enabled" name="feature_enabled">
                        <label for="feature_enabled">[Feature Name]</label>
                    </div>
                    <span class="form-help">[Help text]</span>
                </div>

                <!-- Dropdown -->
                <div class="form-group">
                    <label for="option_select">[Option Name]</label>
                    <select id="option_select" name="option_select">
                        <option value="option1">Option 1</option>
                        <option value="option2">Option 2</option>
                    </select>
                    <span class="form-help">[Help text]</span>
                </div>
            </div>

            <!-- Save buttons -->
            <div class="button-group">
                <button type="submit" class="btn btn-primary" id="saveBtn">SAVE SETTINGS</button>
                <a href="/config" class="btn btn-secondary">BACK TO DASHBOARD</a>
            </div>
        </form>

        <!-- Status messages -->
        <div id="status-container"></div>
    </div>

    <script>
        let currentSettings = null;

        // Load settings on page load
        document.addEventListener('DOMContentLoaded', async () => {
            await loadSettings();
        });

        async function loadSettings() {
            try {
                const response = await fetch('/config/[name]/settings');
                const data = await response.json();

                if (data.error) {
                    showStatus('Failed to load settings: ' + data.error, 'error');
                    return;
                }

                currentSettings = data;
                populateForm(data);

                // Hide loading, show content
                document.getElementById('loading').style.display = 'none';
                document.getElementById('settings-content').style.display = 'block';
            } catch (error) {
                showStatus('Failed to load settings: ' + error.message, 'error');
            }
        }

        function populateForm(settings) {
            // Section 1
            document.getElementById('param_name').value = settings.section1.param_name;
            document.getElementById('feature_enabled').checked = settings.section1.feature_enabled;
            document.getElementById('option_select').value = settings.section1.option_select;

            // Section 2
            // ... more fields
        }

        // Handle form submission
        document.getElementById('[name]Form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const saveBtn = document.getElementById('saveBtn');
            saveBtn.disabled = true;
            saveBtn.textContent = 'SAVING...';

            const settings = {
                section1: {
                    param_name: document.getElementById('param_name').value,
                    feature_enabled: document.getElementById('feature_enabled').checked,
                    option_select: document.getElementById('option_select').value
                },
                section2: {
                    // ... more fields
                }
            };

            try {
                showStatus('Saving settings...', 'success');

                const response = await fetch('/config/[name]/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(settings)
                });

                const result = await response.json();

                if (result.success) {
                    showStatus(result.message, 'success');
                    currentSettings = settings;
                } else {
                    showStatus('Save failed: ' + result.message, 'error');
                }
            } catch (error) {
                showStatus('Save failed: ' + error.message, 'error');
            } finally {
                saveBtn.disabled = false;
                saveBtn.textContent = 'SAVE SETTINGS';
            }
        });

        function showStatus(message, type) {
            const container = document.getElementById('status-container');
            const statusDiv = document.createElement('div');
            statusDiv.className = `status-message status-${type}`;
            statusDiv.textContent = message;
            container.innerHTML = '';
            container.appendChild(statusDiv);

            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    </script>
{% endblock %}
```

## 2. Flask Routes (monitor_server.py)

Add these routes to `MonitorServer` class:

```python
@self.app.route('/config/[name]')
def config_[name]():
    """[Name] configuration page"""
    return render_template('config_[name].html')

@self.app.route('/config/[name]/settings')
def get_[name]_settings():
    """Get current [name] settings"""
    settings = self.config_manager.get_[name]_settings()
    return jsonify(settings)

@self.app.route('/config/[name]/save', methods=['POST'])
def save_[name]_settings():
    """Save [name] settings"""
    settings = request.get_json()
    result = self.config_manager.save_[name]_settings(settings)
    return jsonify(result)
```

## 3. Backend Methods (config_manager.py)

```python
def get_[name]_settings(self) -> Dict:
    """
    Get current [name] settings from BobConfig

    Returns:
        Dictionary containing all configurable [name] settings
    """
    try:
        return {
            'section1': {
                'param1': self.config.PARAM1,
                'param2': self.config.PARAM2
            },
            'section2': {
                'param3': self.config.PARAM3
            }
        }
    except Exception as e:
        logger.error(f"Error getting [name] settings: {e}", exc_info=True)
        return {'error': str(e)}

def save_[name]_settings(self, settings: Dict) -> Dict:
    """
    Save [name] settings to BobConfig.py

    Args:
        settings: Dictionary of settings to save (can be partial update)

    Returns:
        Dictionary with success status and message
    """
    try:
        config_path = Path(__file__).parent.parent / 'BobConfig.py'

        if not config_path.exists():
            return {'success': False, 'message': f'Config file not found: {config_path}'}

        # Read current config file
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Track changes
        changes_made = []

        # Section 1 settings
        if 'section1' in settings:
            sec1 = settings['section1']

            if 'param1' in sec1:
                content = re.sub(
                    r'PARAM1:\s*int\s*=\s*\d+',
                    f'PARAM1: int = {sec1["param1"]}',
                    content
                )
                changes_made.append(f"PARAM1 = {sec1['param1']}")

            if 'param2' in sec1:
                content = re.sub(
                    r'PARAM2:\s*bool\s*=\s*(True|False)',
                    f'PARAM2: bool = {sec1["param2"]}',
                    content
                )
                changes_made.append(f"PARAM2 = {sec1['param2']}")

        # Section 2 settings
        if 'section2' in settings:
            sec2 = settings['section2']

            if 'param3' in sec2:
                content = re.sub(
                    r'PARAM3:\s*float\s*=\s*[\d.]+',
                    f'PARAM3: float = {float(sec2["param3"])}',
                    content
                )
                changes_made.append(f"PARAM3 = {sec2['param3']}")

        if not changes_made:
            return {'success': False, 'message': 'No valid settings to update'}

        # Write updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Updated [name] settings: {', '.join(changes_made)}")

        return {
            'success': True,
            'message': f'Settings saved successfully. Updated: {", ".join(changes_made)}'
        }

    except Exception as e:
        logger.error(f"Error saving [name] settings: {e}", exc_info=True)
        return {'success': False, 'message': f'Error: {str(e)}'}
```

## 4. Dashboard Card (config_dashboard.html)

Add card to dashboard (around line 100-200):

```html
<!-- [Name] Configuration -->
<a href="/config/[name]" class="config-card">
    <div class="config-icon">[EMOJI]</div>
    <h3>[Name] Settings</h3>
    <p>[Brief description]</p>
    <div class="config-status">
        <span class="badge badge-success">✓ Available</span>
    </div>
</a>
```

## 5. Test Script Pattern

```python
"""
Test [Name] Configuration
Quick test to verify [name] routes are registered
"""

from BobConfig import BobConfig
from web.monitor_server import MonitorServer
from local_event_bus import LocalEventBus
import time

def test_[name]_settings():
    print("=" * 60)
    print("[Name] Configuration - Test")
    print("=" * 60)

    # Initialize components
    print("\n1. Initializing MonitorServer...")
    config = BobConfig()
    event_bus = LocalEventBus()
    monitor = MonitorServer(event_bus=event_bus, config=config)

    print("   [PASS] MonitorServer initialized")

    # List all registered routes
    print("\n2. Checking registered routes...")
    required_routes = ['/config/[name]', '/config/[name]/settings', '/config/[name]/save']
    all_routes = [rule.rule for rule in monitor.app.url_map.iter_rules()]

    for route in required_routes:
        if route in all_routes:
            print(f"   [FOUND] {route}")
        else:
            print(f"   [MISSING] {route}")
            return False

    # Start server in background
    print("\n3. Starting web server...")
    import threading
    server_thread = threading.Thread(target=lambda: monitor.start(), daemon=True)
    server_thread.start()
    time.sleep(2)

    # Test with requests
    print("\n4. Testing routes...")
    import requests

    try:
        response = requests.get('http://localhost:5000/config/[name]/settings', timeout=5)
        print(f"   GET /config/[name]/settings: {response.status_code}")
        if response.status_code == 200:
            settings = response.json()
            print(f"   Response keys: {list(settings.keys())}")
            for section in settings:
                print(f"   - {section}: {list(settings[section].keys())}")
    except Exception as e:
        print(f"   Error: {e}")
        return False

    print("\n" + "="*60)
    print("[PASS] All [name] configuration tests passed!")
    print("="*60)
    print("\nServer is running. Open in browser:")
    print("  - Config Dashboard: http://localhost:5000/config")
    print("  - [Name] Settings:  http://localhost:5000/config/[name]")
    print("\nPress Ctrl+C to stop...")
    print("="*60)

    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping...")

    return True

if __name__ == "__main__":
    test_[name]_settings()
```

## Bob The Skull Aesthetic

### Colors
- **Background:** `#1a1a1a` (dark gray)
- **Text:** `#00ff00` (terminal green)
- **Accent:** `#00aa00` (darker green)
- **Error:** `#ff4444` (red)
- **Success:** `#00ff00` (green)
- **Warning:** `#ffaa00` (orange)

### Typography
- **Font:** Courier New, monospace
- **Headers:** ALL CAPS, bold
- **Body:** 14px
- **Help text:** 0.85em, lighter green

### Form Elements
```css
input[type="text"],
input[type="number"],
select {
    background: #2a2a2a;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 8px;
    font-family: 'Courier New', monospace;
}

button.btn-primary {
    background: #00aa00;
    color: #000;
    border: 2px solid #00ff00;
    padding: 10px 20px;
    font-weight: bold;
}
```

### Status Messages
```html
<div class="status-message status-success">
    ✓ Settings saved successfully
</div>

<div class="status-message status-error">
    ✗ Error saving settings
</div>
```

## Existing Pages Reference

1. **Audio** (`config_audio.html`) - Device selection, volumes
2. **Vision** (`config_vision.html`) - Camera, face detection, performance
3. **System** (`config_system.html`) - Wake word, STT, LLM, TTS models
4. **Performance** (`config_performance.html`) - Timeouts, state machine
5. **Eyes** (`config_eyes.html`) - Hardware interface, discovery
6. **API Keys** (`config_apikeys.html`) - API key management

## Checklist

- [ ] Create HTML template following aesthetic
- [ ] Add Flask routes to monitor_server.py
- [ ] Implement get_settings() in config_manager.py
- [ ] Implement save_settings() in config_manager.py
- [ ] Add dashboard card to config_dashboard.html
- [ ] Create test script
- [ ] Test loading settings
- [ ] Test saving settings
- [ ] Test error handling
- [ ] Verify mobile responsiveness
- [ ] Update TODO.md

## Common Patterns

**Input Validation:**
```javascript
if (value < min || value > max) {
    showStatus('Value must be between ' + min + ' and ' + max, 'error');
    return;
}
```

**Confirmation for destructive actions:**
```javascript
if (!confirm('Are you sure you want to reset all settings?')) {
    return;
}
```

**Loading states:**
```javascript
saveBtn.disabled = true;
saveBtn.textContent = 'SAVING...';
// ... do save ...
saveBtn.disabled = false;
saveBtn.textContent = 'SAVE SETTINGS';
```

## Pro Tips

1. **Use existing pages as templates** - Copy structure from similar page
2. **Test incrementally** - Test routes, then GET, then POST
3. **Watch for typos** - IDs must match across HTML/JavaScript
4. **Use browser DevTools** - Check console for JavaScript errors
5. **Test with invalid values** - Ensure validation works
6. **Mobile test** - Bob's aesthetic works on mobile too
