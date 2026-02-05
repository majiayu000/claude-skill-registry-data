---
name: psr12-moodle
description: Automatically validate and fix Moodle PHP code for PSR-12 compliance with Moodle-specific exceptions (lowercase_with_underscores naming, frankenstyle prefixes). Activates when working with Moodle plugin PHP files or when code standards issues are detected.
allowed-tools: Read, Edit, Grep, Bash
---

# PSR-12 Moodle Compliance Skill

## Automatic Activation Triggers

This skill activates automatically when:
- Writing or editing PHP files in Moodle plugin directories
- User mentions "code standards", "PSR-12", "phpcs", or "coding style"
- Discussions about refactoring or code quality
- After implementing new Moodle functions or classes

## Moodle-Specific PSR-12 Rules

### Core Principle
Moodle follows **PSR-12 with specific exceptions** for legacy compatibility.

### Naming Conventions (EXCEPTIONS to PSR-12)

#### Classes
```php
// ❌ PSR-12 Standard (PascalCase)
class FolderBrowser {}

// ✅ Moodle Standard (lowercase_with_underscores)
class folder_browser {}
```

#### Functions & Methods
```php
// ❌ PSR-12 Standard (camelCase)
public function getUserData() {}

// ✅ Moodle Standard (lowercase_with_underscores)
public function get_user_data() {}
```

#### Variables
```php
// ❌ PSR-12 Standard (camelCase)
$userData = [];

// ✅ Moodle Standard (lowercase_with_underscores)
$user_data = [];
```

### Frankenstyle Naming (REQUIRED)

All functions, classes, and namespaces must include component prefix:

```php
// ❌ Missing component prefix
function get_folder_contents() {}
class folder_browser {}

// ✅ With frankenstyle prefix
function mod_nextcloudfolder_get_folder_contents() {}
class mod_nextcloudfolder_folder_browser {}
```

### PSR-12 Rules FOLLOWED by Moodle

#### 1. Indentation: 4 spaces
```php
// ✅ Correct
function example() {
    if ($condition) {
        do_something();
    }
}
```

#### 2. Line Length: 180 characters max (Moodle extends PSR-12's 120)
```php
// ⚠️ Moodle allows up to 180 characters per line
$result = $DB->get_record_sql('SELECT * FROM {table} WHERE field1 = ? AND field2 = ? AND field3 = ?', [$param1, $param2, $param3]);
```

#### 3. Opening Braces: Same line for control structures
```php
// ✅ Correct
if ($condition) {
    // code
}

// ✅ New line for functions/classes
function my_function()
{
    // code
}
```

#### 4. Namespaces
```php
// ✅ Correct namespace with frankenstyle
namespace mod_nextcloudfolder\local;

class helper {
    // ...
}
```

#### 5. Use statements
```php
// ✅ One per line, alphabetically sorted
use mod_nextcloudfolder\local\api;
use mod_nextcloudfolder\local\helper;
```

## Validation Workflow

### Step 1: Read Current Code
```bash
# Use Read tool to examine PHP file
```

### Step 2: Identify Violations
Check for:
- camelCase naming → lowercase_with_underscores
- Missing frankenstyle prefixes
- Incorrect indentation (not 4 spaces)
- Lines exceeding 180 characters
- Missing or incorrect PHPDoc blocks
- Improper brace placement

### Step 3: Run phpcs
```bash
# Moodle code checker
vendor/bin/phpcs --standard=moodle path/to/plugin/

# Or use dev helper if available
./dev.sh check
```

### Step 4: Apply Fixes

**Automatic fixes:**
```bash
vendor/bin/phpcbf --standard=moodle path/to/plugin/
```

**Manual fixes:** Use Edit tool for:
- Renaming violations
- Adding frankenstyle prefixes
- Fixing complex structural issues

### Step 5: Verify
```bash
# Rerun phpcs to confirm clean
vendor/bin/phpcs --standard=moodle path/to/plugin/
```

## Common Violations & Fixes

### 1. camelCase Function Names
```php
// ❌ Before
function getUserFolders($userid) {
    return $DB->get_records('folders', ['userid' => $userid]);
}

// ✅ After
function mod_nextcloudfolder_get_user_folders($userid) {
    return $DB->get_records('nextcloudfolder', ['userid' => $userid]);
}
```

### 2. Missing PHPDoc
```php
// ❌ Before
function get_folders() {
    // ...
}

// ✅ After
/**
 * Get all folders for current user.
 *
 * @return array Array of folder objects
 */
function mod_nextcloudfolder_get_folders() {
    // ...
}
```

### 3. Class Naming
```php
// ❌ Before
class FolderApi {
    // ...
}

// ✅ After
namespace mod_nextcloudfolder\local;

/**
 * Folder API helper class.
 *
 * @package    mod_nextcloudfolder
 * @copyright  2024 Your Name
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class folder_api {
    // ...
}
```

### 4. Indentation Issues
```php
// ❌ Before (2 spaces or tabs)
function example() {
  if ($condition) {
    do_something();
  }
}

// ✅ After (4 spaces)
function example() {
    if ($condition) {
        do_something();
    }
}
```

### 5. Long Lines
```php
// ❌ Before (>180 chars)
$result = $DB->get_record_sql('SELECT * FROM {table} WHERE field1 = ? AND field2 = ? AND field3 = ? AND field4 = ? AND field5 = ?', [$param1, $param2, $param3, $param4, $param5]);

// ✅ After (split logically)
$sql = 'SELECT * FROM {table}
         WHERE field1 = ? AND field2 = ?
           AND field3 = ? AND field4 = ?
           AND field5 = ?';
$params = [$param1, $param2, $param3, $param4, $param5];
$result = $DB->get_record_sql($sql, $params);
```

## Output Format

After validation and fixes:

```
✅ PSR-12 Moodle Compliance Check

File: mod/nextcloudfolder/lib.php
Status: ✅ PASSED (or ❌ FAILED)

Issues Fixed:
- ✓ Renamed getUserData() → get_user_data()
- ✓ Added frankenstyle prefix to class folder_browser
- ✓ Fixed indentation (27 lines)
- ✓ Added missing PHPDoc blocks (5 functions)
- ✓ Split 3 lines exceeding 180 characters

Remaining Issues: 0

Next: Run `vendor/bin/phpcs --standard=moodle mod/nextcloudfolder/` to verify.
```

## Integration with Development Workflow

1. **Before Commit**: Auto-run this skill on all modified PHP files
2. **During Code Review**: Validate pull requests
3. **CI/CD Pipeline**: Automated standards checking
4. **IDE Integration**: Real-time validation

## References

- [Moodle Coding Style](https://moodledev.io/general/development/policies/codingstyle)
- [PSR-12 Extended Coding Style](https://www.php-fig.org/psr/psr-12/)
- [Moodle Code Checker](https://github.com/moodlehq/moodle-cs)
