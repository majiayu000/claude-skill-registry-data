---
name: moodle-php-direct
description: Execute PHP scripts directly on the Moodle server via SSH for database queries, user management, course operations, and system administration. Use when you need direct database access, when REST API permissions are insufficient, or when the user asks to "use PHP directly" or "run a script on the server".
allowed-tools:
  - Bash
  - Read
  - Write
---

# Moodle PHP Direct Access Skill

Execute PHP scripts directly on the Moodle server with full access to the Moodle PHP APIs and database.

## SSH Configuration

**Environment Variables:**
```bash
export MOODLE_LIGHTSAIL_IP=52.45.180.231
export MOODLE_SSH_USER=ubuntu
export MOODLE_REMOTE_DIR=/var/www/html/moodle
```

## When to Use This Skill

Use PHP direct access when:
- REST API lacks permissions for the operation
- Need direct database queries
- Performing bulk operations
- System administration tasks
- Creating users, tokens, or services
- Debugging or inspection tasks

## PHP Script Pattern

All PHP scripts must follow this pattern:

```php
<?php
/**
 * Brief description of what this script does
 */

define('CLI_SCRIPT', true);

// Load Moodle environment
require_once('/var/www/html/moodle/config.php');
require_once($CFG->libdir.'/clilib.php');

// Your code here
// Access $DB for database operations
// Access $CFG for configuration
// Use Moodle APIs as needed

?>
```

## Common Operations

### Database Queries
```php
// Get records
$users = $DB->get_records('user', ['deleted' => 0]);
$user = $DB->get_record('user', ['username' => 'someuser']);
$courses = $DB->get_records('course', ['visible' => 1]);

// Count records
$count = $DB->count_records('user', ['deleted' => 0]);

// Execute SQL
$sql = "SELECT * FROM {user} WHERE email LIKE :pattern";
$results = $DB->get_records_sql($sql, ['pattern' => '%@example.com']);

// Insert/Update/Delete
$DB->insert_record('tablename', $dataobject);
$DB->update_record('tablename', $dataobject);
$DB->delete_records('tablename', ['id' => 123]);
```

### User Management
```php
require_once($CFG->dirroot.'/user/lib.php');

// Create user
$user = new stdClass();
$user->username = 'newuser';
$user->firstname = 'First';
$user->lastname = 'Last';
$user->email = 'user@example.com';
$user->auth = 'manual';
$user->confirmed = 1;
$user->mnethostid = $CFG->mnet_localhost_id;
$user->id = user_create_user($user);

// Get user
$user = $DB->get_record('user', ['username' => 'someuser']);
```

### Course Operations
```php
require_once($CFG->dirroot.'/course/lib.php');

// Get course
$course = $DB->get_record('course', ['id' => 6]);

// Get enrolled users
$context = context_course::instance($course->id);
$users = get_enrolled_users($context);
```

### Web Service Tokens
```php
require_once($CFG->libdir.'/externallib.php');

// Create token
$token = new stdClass();
$token->token = md5(uniqid(rand(), 1));
$token->userid = $user->id;
$token->tokentype = EXTERNAL_TOKEN_PERMANENT;
$token->externalserviceid = $serviceid;
$token->contextid = context_system::instance()->id;
$token->creatorid = $user->id;
$token->timecreated = time();
$token->validuntil = 0;
$token->id = $DB->insert_record('external_tokens', $token);
```

## Execution Pattern

```bash
# Create script locally
cat > /tmp/script.php << 'EOF'
<?php
define('CLI_SCRIPT', true);
require_once('/var/www/html/moodle/config.php');
// Your code
?>
EOF

# Upload and execute
scp /tmp/script.php ubuntu@${MOODLE_LIGHTSAIL_IP}:/tmp/
ssh ubuntu@${MOODLE_LIGHTSAIL_IP} "sudo php /tmp/script.php"
```

## Helper Scripts

- **`exec_php.sh`** - Execute a PHP file on the server
- **`query_db.sh`** - Quick database query helper

## Best Practices

NEVER make destructive changes without explicit user instructions. Follow these practices:

1. **Read-only first** - Always query/inspect before modifying
2. **Test queries** - Verify SQL with SELECT before UPDATE/DELETE
3. **Backup awareness** - Assume changes are permanent
4. **Use transactions** - For multi-step operations
5. **Error handling** - Always check return values
6. **Clean up** - Remove temporary scripts after execution

## Security Notes

- **Sudo access required** - Scripts run with elevated privileges
- **Direct database access** - Bypasses Moodle's API safeguards
- **No audit log** - Changes may not appear in Moodle's activity log
- **Permanent changes** - No undo mechanism
- **Use sparingly** - Prefer REST API when possible
