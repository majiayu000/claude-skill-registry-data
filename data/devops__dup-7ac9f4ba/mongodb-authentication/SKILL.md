---
name: mongodb-authentication
version: "2.1.0"
description: Master MongoDB authentication methods including SCRAM, X.509 certificates, LDAP, and Kerberos. Learn user creation, role assignment, and securing MongoDB deployments.
sasmp_version: "1.3.0"
bonded_agent: 06-mongodb-security-administration
bond_type: PRIMARY_BOND

# Production-Grade Skill Configuration
capabilities:
  - scram-authentication
  - x509-certificates
  - ldap-integration
  - user-management
  - role-assignment

input_validation:
  required_context:
    - auth_method
    - environment
  optional_context:
    - existing_users
    - ldap_config
    - certificate_chain

output_format:
  user_config: object
  connection_string: string
  verification_steps: array
  security_checklist: array

error_handling:
  common_errors:
    - code: AUTH001
      condition: "Authentication failed"
      recovery: "Verify username, password, authSource database"
    - code: AUTH002
      condition: "User not found"
      recovery: "Check user exists in correct authenticationDatabase"
    - code: AUTH003
      condition: "Password policy violation"
      recovery: "Ensure password meets complexity requirements"

prerequisites:
  mongodb_version: "4.0+"
  required_knowledge:
    - mongodb-basics
    - user-management
  security_requirements:
    - "mongod started with --auth or authorization: enabled"

testing:
  unit_test_template: |
    // Verify authentication
    const client = new MongoClient(uri, { auth: { username, password } })
    await client.connect()
    const status = await client.db('admin').command({ connectionStatus: 1 })
    expect(status.authInfo.authenticatedUsers[0].user).toBe(username)
---

# MongoDB Authentication

Secure your MongoDB with proper authentication.

## Quick Start

### Enable Authentication
```bash
# Start MongoDB with authentication
mongod --auth --dbpath /data/db

# Or in config file (mongod.conf)
security:
  authorization: enabled
```

### Create Admin User
```javascript
// Connect to local server without auth first
const mongo = new MongoClient('mongodb://localhost:27017')
const admin = mongo.db('admin')

// Create admin user
await admin.command({
  createUser: 'admin',
  pwd: 'securepassword',  // Or use passwordPrompt()
  roles: ['root']
})

// Now restart mongod --auth
```

## Authentication Methods

### SCRAM (Salted Challenge Response)
```javascript
// Default, password-based authentication

// Connection string
mongodb://username:password@localhost:27017/database

// With options
mongodb://username:password@localhost:27017/database?authSource=admin

// Create SCRAM user
db.createUser({
  user: 'appuser',
  pwd: 'password123',
  roles: ['readWrite']
})
```

### X.509 Certificate
```javascript
// Enterprise-grade certificate authentication

// Create certificate user (External auth DB)
db.getSiblingDB('$external').createUser({
  user: 'CN=client,OU=Engineering,O=Company',
  roles: ['readWrite']
})

// Client connects with certificate
mongodb://USERNAME@cluster.mongodb.net/?authMechanism=MONGODB-X509&tlsCertificateKeyFile=/path/to/client.pem
```

### LDAP
```javascript
// Enterprise directory integration

// Create LDAP user (External auth DB)
db.getSiblingDB('$external').createUser({
  user: 'ldapuser',
  roles: ['readWrite']
})

// Configure LDAP in mongod.conf
security:
  ldap:
    servers: 'ldap.example.com'
    authzQueryTemplate: 'dc=example,dc=com??sub?(uid={0})'
    bindQueryUser: 'cn=admin,dc=example,dc=com'
    bindQueryPassword: 'password'
```

## User Management

### Create User
```javascript
// Basic user
db.createUser({
  user: 'username',
  pwd: 'password',
  roles: ['readWrite']
})

// With multiple roles
db.createUser({
  user: 'dbadmin',
  pwd: 'password',
  roles: [
    { role: 'dbAdmin', db: 'myapp' },
    { role: 'readWrite', db: 'myapp' }
  ]
})

// Interactive password prompt
db.createUser({
  user: 'username',
  pwd: passwordPrompt(),
  roles: ['readWrite']
})
```

### List Users
```javascript
// Show all users in current database
db.getUsers()

// Show specific user
db.getUser('username')
```

### Update User Password
```javascript
// Change password
db.changeUserPassword('username', 'newpassword')

// Or
db.updateUser('username', {
  pwd: 'newpassword'
})
```

### Remove User
```javascript
db.dropUser('username')
```

## Built-in Roles

### Database User Roles
```javascript
'read' → Read-only access
'readWrite' → Read and write access

// Grant role
db.grantRolesToUser('username', ['read'])
```

### Database Admin Roles
```javascript
'dbAdmin' → Database administration
'dbOwner' → Full database access
'userAdmin' → User management

// Example
db.createUser({
  user: 'dbadmin',
  pwd: 'password',
  roles: ['dbAdmin', 'userAdmin']
})
```

### Cluster Admin Roles
```javascript
'clusterAdmin' → Full cluster access
'clusterManager' → Cluster management
'clusterMonitor' → Read-only monitoring

// Cluster role
db.getSiblingDB('admin').createUser({
  user: 'clusteradmin',
  pwd: 'password',
  roles: ['clusterAdmin']
})
```

### All Built-in Roles
```
Admin: root, dbAdmin, userAdmin, clusterAdmin
Read: read
Write: readWrite
Backup: backup, restore
Monitoring: clusterMonitor, serverStatus, monitoring
```

## Custom Roles

### Create Custom Role
```javascript
// Create custom 'reportViewer' role
db.createRole({
  role: 'reportViewer',
  privileges: [
    {
      resource: { db: 'reporting', collection: '' },
      actions: ['find']
    }
  ],
  roles: []
})

// Assign to user
db.grantRolesToUser('analyst', [
  { role: 'reportViewer', db: 'admin' }
])
```

### Privilege Structure
```javascript
{
  resource: {
    db: 'myapp',           // Database ('' = all dbs)
    collection: 'users'    // Collection ('' = all collections)
  },
  actions: [
    'find',        // Query documents
    'insert',      // Insert documents
    'update',      // Update documents
    'remove',      // Delete documents
    'createIndex', // Index management
    'dropIndex'
  ]
}
```

## Password Policies

### Strong Passwords
```javascript
// Requirements for production:
// ✅ Minimum 12 characters
// ✅ Mix of uppercase, lowercase, numbers, symbols
// ✅ No dictionary words
// ✅ Not related to username

// Example strong password
// P@ssw0rd2024!MongoDB

// DON'T USE
// password, 123456, monkey, qwerty, password123
```

### Password Rotation
```javascript
// Change passwords regularly
// Monthly for service accounts
// Quarterly for normal users

// Update password
db.changeUserPassword('username', 'newpassword')

// Check user details
db.getUser('username')
```

## Connection with Authentication

### MongoDB Shell
```bash
# Connect with authentication
mongosh --username admin --password --authenticationDatabase admin mongodb://localhost:27017

# Or with connection string
mongosh 'mongodb://admin:password@localhost:27017/?authSource=admin'
```

### Node.js Driver
```javascript
const MongoClient = require('mongodb').MongoClient

// Option 1: Connection string
const client = new MongoClient(
  'mongodb://username:password@localhost:27017/database?authSource=admin'
)

// Option 2: With encodeURIComponent for special chars
const user = encodeURIComponent('user@example.com')
const pass = encodeURIComponent('pass!@#$%')
const client = new MongoClient(
  `mongodb://${user}:${pass}@localhost:27017/database?authSource=admin`
)

// Option 3: Auth options
const client = new MongoClient('mongodb://localhost:27017', {
  auth: {
    username: 'admin',
    password: 'password'
  },
  authSource: 'admin'
})
```

### Python PyMongo
```python
from pymongo import MongoClient

# Connection string
client = MongoClient('mongodb://username:password@localhost:27017/database?authSource=admin')

# Or with options
client = MongoClient(
    'mongodb://localhost:27017',
    username='username',
    password='password',
    authSource='admin'
)
```

## Security Best Practices

✅ **User Management:**
1. **Unique passwords** - Each user gets own password
2. **Strong passwords** - 12+ chars, complex
3. **Regular rotation** - Change periodically
4. **Least privilege** - Only needed roles
5. **Separate accounts** - Admin vs. app users

✅ **Production Security:**
1. **Always enable auth** - --auth or authorization: enabled
2. **Use network authentication** - Bind to specific IPs
3. **Enable TLS/SSL** - Encrypt connections
4. **Regular audits** - Check user permissions
5. **Disable default users** - Remove guest, test users

✅ **Atlas Security:**
1. **Enable SCRAM** - Default method
2. **Use strong passwords** - Auto-generated preferred
3. **Create service accounts** - For applications
4. **Limited roles** - readWrite for apps, not admin
5. **Monitor activity** - Check who accessed what

❌ **Avoid:**
1. ❌ Sharing passwords
2. ❌ Weak passwords
3. ❌ No authentication
4. ❌ Admin credentials for apps
5. ❌ Hardcoded passwords in code

## Next Steps

1. **Enable authentication** - On your MongoDB
2. **Create admin user** - Initial setup
3. **Create app user** - For application
4. **Test connection** - From application
5. **Setup TLS** - Encrypt connections
6. **Monitor users** - Who can access what

---

**Secure your MongoDB with authentication!** 🔐
