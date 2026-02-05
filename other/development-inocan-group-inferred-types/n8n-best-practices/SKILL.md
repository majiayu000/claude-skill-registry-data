---
name: n8n-best-practices
description: Use when encountering n8n workflow issues, Code node errors, HTTP requests failing, data flow problems, environment variables not working, JSON parsing errors, or need n8n development patterns and debugging strategies
---

# n8n Best Practices

**When to use this skill**: Any time you're working with n8n workflows and encounter errors, unexpected behavior, or need guidance on implementation patterns.

## Critical Knowledge Base

### 🚨 ES5 Syntax Only in Code Nodes

n8n Code nodes **only support ES5 JavaScript**. Modern ES6+ syntax will fail.

**❌ DO NOT USE:**
```javascript
// Arrow functions
const process = (item) => item.value;

// Template literals
const url = `https://api.example.com/${id}`;

// const/let
const value = 123;

// Destructuring
const { name, age } = person;

// Spread operator in function calls
Math.max(...numbers);
```

**✅ USE INSTEAD:**
```javascript
// Regular functions
var process = function(item) {
  return item.value;
};

// String concatenation
var url = 'https://api.example.com/' + id;

// var only
var value = 123;

// Manual assignment
var name = person.name;
var age = person.age;

// apply() for spread
Math.max.apply(null, numbers);

// Object spread alternative
var merged = Object.assign({}, obj1, obj2);
```

### 🌐 HTTP Requests in Code Nodes

**CRITICAL**: `$http` and `axios` are NOT available in Code nodes.

**❌ WRONG:**
```javascript
const response = await $http.request({url: 'https://api.example.com'});
const axios = require('axios');
```

**✅ CORRECT - Use Native HTTPS:**
```javascript
var https = require('https');

function makeRequest(url, options) {
  return new Promise(function(resolve, reject) {
    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        resolve({statusCode: res.statusCode, body: data});
      });
    });
    req.on('error', reject);
    req.end();
  });
}

// Usage
var result = await makeRequest('example.com', {
  hostname: 'example.com',
  path: '/api/endpoint',
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
});
```

### 🔐 Environment Variables Configuration

**CRITICAL**: Variables must be explicitly exported, not just sourced.

**❌ WRONG:**
```bash
source .env.local
pnpm start
# Variables will be undefined in Code nodes!
```

**✅ CORRECT:**
```bash
#!/bin/bash
export NOTION_API_KEY=$(grep NOTION_API_KEY .env.local | cut -d '=' -f2)
export QWEN_API_KEY=$(grep QWEN_API_KEY .env.local | cut -d '=' -f2)
export NODE_FUNCTION_ALLOW_BUILTIN=*
export N8N_BLOCK_ENV_ACCESS_IN_NODE=false
pnpm start
```

**Access in Code nodes:**
```javascript
var apiKey = process.env.NOTION_API_KEY;  // Not $env
```

### 📦 gzip Compression Issues

**Problem**: HTTP requests with gzip compression return garbled data.

**❌ WRONG:**
```javascript
headers: {
  'Accept-Encoding': 'gzip, deflate'
}
// Returns: �������
```

**✅ CORRECT:**
```javascript
headers: {
  'Content-Type': 'application/json'
  // DO NOT include Accept-Encoding header
}
```

### 🔄 Data Flow Patterns

**Always preserve upstream data:**

**✅ CORRECT:**
```javascript
return {
  json: Object.assign({}, $input.item.json, {
    newField: newValue
  })
};
```

**❌ WRONG:**
```javascript
return {
  json: {
    newField: newValue  // Loses all previous data!
  }
};
```

### 📋 JSON Parsing Best Practices

**❌ WRONG:**
```javascript
var data = JSON.parse(response);
// May return undefined without error
```

**✅ CORRECT:**
```javascript
function safeJSONParse(text) {
  try {
    var parsed = JSON.parse(text);
    if (parsed && typeof parsed === 'object') {
      return parsed;
    }
    throw new Error('Parsed value is not an object');
  } catch (e) {
    throw new Error('JSON parsing failed: ' + e.message);
  }
}

var data = safeJSONParse(response);
```

### 🔧 Code Node Sandbox Configuration

**macOS launchd service:**
```xml
<key>EnvironmentVariables</key>
<dict>
  <key>NODE_FUNCTION_ALLOW_BUILTIN</key>
  <string>*</string>
</dict>
```

**Shell script:**
```bash
export NODE_FUNCTION_ALLOW_BUILTIN=*
n8n start
```

### 🐛 Common Pitfalls

**1. Aggregate Node Array Wrapping**
```javascript
// Aggregate converts: {field: value} → {field: [value]}
var data = $input.first().json;
var actualValue = data.field[0];  // Must access array
```

**2. Split Into Batches Data Loss**
```javascript
// ❌ WRONG: Loses data
return items.map(function(item) {
  return {json: {processed: true}};
});

// ✅ CORRECT: Preserves data
return items.map(function(item) {
  return {
    json: Object.assign({}, item.json, {processed: true})
  };
});
```

**3. require() Module Access**
```javascript
// Only available if NODE_FUNCTION_ALLOW_BUILTIN=*
var https = require('https');  // ✅ Works
var axios = require('axios');  // ❌ Not available
```

## Quick Reference

### When Code node fails:
1. Check ES5 syntax (no arrow functions, template literals)
2. Verify environment variables are exported
3. Use `require('https')` not `$http`
4. Remove `Accept-Encoding` header for gzip issues

### When data is lost:
1. Always spread previous data: `Object.assign({}, $input.item.json, newData)`
2. Check Aggregate node array wrapping
3. Verify Split Into Batches preserves data

### When environment variables are undefined:
1. Use `export`, not `source`
2. Access with `process.env.VAR`, not `$env.VAR`
3. Set `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`

## Full Documentation

For complete details, examples, and advanced patterns, see:
`/mnt/d/work/n8n_agent/n8n-skills/n8n-best-practices/README.md`
