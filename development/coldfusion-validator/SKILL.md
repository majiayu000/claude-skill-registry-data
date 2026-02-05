---
name: coldfusion-validator
description: Comprehensive ColdFusion (CFML) syntax validation and best practices verification. Use when validating ColdFusion code, checking for security vulnerabilities (SQL injection, proper cfqueryparam usage), ensuring proper variable scoping, verifying code quality standards, or reviewing ColdFusion applications for senior developer best practices.
---

# ColdFusion Syntax Validation Skill

## Overview
This skill provides comprehensive ColdFusion (CFML) syntax validation and best practices verification based on senior developer standards. It helps ensure code quality, security, and maintainability.

## Tools and Validation Methods

### 1. CFLint - Primary Validation Tool
CFLint is the standard tool for ColdFusion syntax validation and best practices checking.

**Installation:**
\`\`\`bash
# Install via npm
npm install -g cflint

# Or download standalone JAR from GitHub
wget https://github.com/cflint/CFLint/releases/latest/download/cflint-assembly-1.5.0.jar
\`\`\`

**Basic Usage:**
\`\`\`bash
# Validate a single file
cflint -file path/to/file.cfm

# Validate entire directory
cflint -folder /path/to/project -html -htmlfile report.html

# JSON output for programmatic parsing
cflint -folder /path/to/project -json -jsonfile report.json
\`\`\`

### 2. Configuration File (.cflintrc)
Create a \`.cflintrc\` configuration file for project-specific rules including checks for SQL injection, missing cfqueryparam, nested cfoutput, and proper documentation.

## Senior Developer Standards

### Critical Security Rules

#### 1. SQL Injection Prevention
**Always use \`cfqueryparam\` for dynamic SQL:**

❌ **Bad:**
\`\`\`cfml
<cfquery name="getUser">
    SELECT * FROM users 
    WHERE username = '#form.username#'
</cfquery>
\`\`\`

✅ **Good:**
\`\`\`cfml
<cfquery name="getUser">
    SELECT id, username, email, created_date 
    FROM users 
    WHERE username = <cfqueryparam value="#form.username#" cfsqltype="cf_sql_varchar">
</cfquery>
\`\`\`

#### 2. Variable Scoping
**Always scope variables properly:**

❌ **Bad:**
\`\`\`cfml
<cffunction name="getUser">
    userID = arguments.id  <!--- Implicitly in variables scope --->
</cffunction>
\`\`\`

✅ **Good:**
\`\`\`cfml
<cffunction name="getUser">
    <cfset var local.userID = arguments.id>
    <cfset local.userData = queryNew()>
</cffunction>
\`\`\`

### Code Quality Standards

#### 3. Component Documentation
**Always provide hints for components, functions, and arguments:**

✅ **Good:**
\`\`\`cfml
<cfcomponent hint="Handles user authentication and session management">
    <cffunction name="authenticateUser" access="public" returntype="boolean" 
                hint="Validates user credentials and creates session">
        <cfargument name="username" type="string" required="true" 
                    hint="User's login name">
        <cfargument name="password" type="string" required="true" 
                    hint="User's password (will be hashed)">
        <cfset var local = {}>
    </cffunction>
</cfcomponent>
\`\`\`

#### 4. Use CFScript for Logic
Modern ColdFusion prefers script syntax for business logic with proper error handling.

## Validation Process

When validating ColdFusion code:

1. **Install CFLint** if not already available
2. **Run validation** using cflint command
3. **Parse results** and highlight critical security issues
4. **Check for**:
   - SQL injection vulnerabilities
   - Missing cfqueryparam
   - SELECT * usage
   - Variable scoping issues
   - Missing documentation
   - Nested cfoutput tags
5. **Provide specific fixes** with before/after examples
6. **Explain reasoning** behind each best practice

## Manual Review Checklist

1. **Security**
   - [ ] All SQL queries use cfqueryparam
   - [ ] No direct form/URL variable usage in queries
   - [ ] Sensitive data is encrypted
   - [ ] File upload paths are validated

2. **Performance**
   - [ ] Queries specify columns (no SELECT *)
   - [ ] Appropriate query caching
   - [ ] Indexes exist for queried columns

3. **Code Quality**
   - [ ] Variables properly scoped (var/local)
   - [ ] Functions have hints/documentation
   - [ ] No nested cfoutput tags
   - [ ] Proper error handling (try/catch)

4. **Maintainability**
   - [ ] Consistent naming conventions
   - [ ] DRY principle followed
   - [ ] Separation of concerns (MVC/layered)
