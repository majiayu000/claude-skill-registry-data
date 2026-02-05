---
name: Security Code Review
description: Identify security vulnerabilities and suggest secure coding practices
---

# Security Code Review Guidelines

When reviewing code for security issues, systematically check for common vulnerabilities and suggest secure alternatives.

## OWASP Top 10 Focus Areas

### 1. Injection Attacks (SQL, NoSQL, Command, LDAP)

**Look for**:
- String concatenation in SQL queries
- Unsanitized user input in database queries
- Direct execution of user input

**Vulnerable**:
```java
// SQL Injection
String query = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);

// Command Injection
Runtime.getRuntime().exec("ping " + userInput);
```

**Secure**:
```java
// Use Prepared Statements
String query = "SELECT * FROM users WHERE username = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, username);
ResultSet rs = pstmt.executeQuery();

// Avoid direct command execution; use APIs instead
// If unavoidable, validate and sanitize input
List<String> allowedHosts = Arrays.asList("localhost", "example.com");
if (allowedHosts.contains(userInput)) {
    // proceed
}
```

### 2. Broken Authentication

**Look for**:
- Passwords stored in plain text
- Weak password requirements
- Missing session timeout
- Predictable session IDs
- Missing multi-factor authentication

**Vulnerable**:
```java
// Plain text password
user.setPassword(password);

// Weak session ID
String sessionId = user.getId() + System.currentTimeMillis();
```

**Secure**:
```java
// Hash passwords with bcrypt
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
String hashedPassword = encoder.encode(password);
user.setPassword(hashedPassword);

// Use cryptographically secure random session IDs
String sessionId = UUID.randomUUID().toString();
```

### 3. Sensitive Data Exposure

**Look for**:
- Logging sensitive information
- Transmitting data over HTTP
- Storing secrets in code
- Returning detailed error messages

**Vulnerable**:
```java
// Logging sensitive data
logger.info("User password: " + password);

// Hardcoded secrets
String apiKey = "sk_live_1234567890abcdef";

// Detailed error messages
catch (Exception e) {
    return "Database error: " + e.getMessage();
}
```

**Secure**:
```java
// Mask sensitive data in logs
logger.info("User authenticated: " + username);

// Use environment variables
String apiKey = System.getenv("API_KEY");

// Generic error messages for users
catch (Exception e) {
    logger.error("Database error", e); // Log details internally
    return "An error occurred. Please try again later.";
}
```

### 4. XML External Entities (XXE)

**Look for**:
- XML parsers without XXE protection
- Processing untrusted XML data

**Vulnerable**:
```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(userProvidedXml);
```

**Secure**:
```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(userProvidedXml);
```

### 5. Broken Access Control

**Look for**:
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities
- CORS misconfiguration

**Vulnerable**:
```java
// No authorization check
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id);
}

// Path traversal
File file = new File("/uploads/" + filename);
```

**Secure**:
```java
// Check authorization
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id, Principal principal) {
    User currentUser = getCurrentUser(principal);
    if (!currentUser.canAccess(id)) {
        throw new AccessDeniedException("Unauthorized");
    }
    return userRepository.findById(id);
}

// Validate and sanitize file paths
Path basePath = Paths.get("/uploads").toAbsolutePath().normalize();
Path filePath = basePath.resolve(filename).normalize();
if (!filePath.startsWith(basePath)) {
    throw new SecurityException("Invalid file path");
}
```

### 6. Security Misconfiguration

**Look for**:
- Debug mode in production
- Default credentials
- Unnecessary features enabled
- Missing security headers
- Verbose error messages

**Vulnerable**:
```yaml
# application.yml
spring:
  profiles:
    active: dev
debug: true
```

**Secure**:
```yaml
# application-prod.yml
spring:
  profiles:
    active: prod
debug: false

# Add security headers
server:
  servlet:
    session:
      cookie:
        secure: true
        http-only: true
```

### 7. Cross-Site Scripting (XSS)

**Look for**:
- Unescaped user input in HTML
- innerHTML usage with user data
- Dangerous template rendering

**Vulnerable**:
```javascript
// Reflected XSS
document.getElementById('greeting').innerHTML =
    "Hello " + userInput;

// DOM-based XSS
element.innerHTML = location.hash.substring(1);
```

**Secure**:
```javascript
// Escape user input
document.getElementById('greeting').textContent =
    "Hello " + userInput;

// Use safe methods
const div = document.createElement('div');
div.textContent = userInput;
element.appendChild(div);
```

### 8. Insecure Deserialization

**Look for**:
- Deserializing untrusted data
- Using vulnerable serialization libraries

**Vulnerable**:
```java
ObjectInputStream ois = new ObjectInputStream(userInputStream);
Object obj = ois.readObject(); // Dangerous!
```

**Secure**:
```java
// Use safe alternatives like JSON
ObjectMapper mapper = new ObjectMapper();
MyObject obj = mapper.readValue(jsonString, MyObject.class);

// If ObjectInputStream required, validate class types
ObjectInputStream ois = new ObjectInputStream(userInputStream) {
    @Override
    protected Class<?> resolveClass(ObjectStreamClass desc)
            throws IOException, ClassNotFoundException {
        if (!desc.getName().equals("com.example.SafeClass")) {
            throw new InvalidClassException("Unauthorized deserialization");
        }
        return super.resolveClass(desc);
    }
};
```

### 9. Using Components with Known Vulnerabilities

**Look for**:
- Outdated dependencies
- Unpatched libraries
- Dependencies with security advisories

**Check**:
```bash
# Maven
mvn versions:display-dependency-updates
mvn dependency-check:check

# npm
npm audit

# Python
pip-audit
```

**Recommendation**:
- Keep dependencies updated
- Monitor security advisories
- Use dependency scanning tools in CI/CD
- Remove unused dependencies

### 10. Insufficient Logging and Monitoring

**Look for**:
- No audit logs for security events
- Missing failed login tracking
- No alerting for suspicious activity

**Vulnerable**:
```java
@PostMapping("/login")
public void login(String username, String password) {
    if (authenticate(username, password)) {
        // Login successful
    }
    // No logging
}
```

**Secure**:
```java
@PostMapping("/login")
public void login(String username, String password, HttpServletRequest request) {
    boolean success = authenticate(username, password);

    if (success) {
        auditLog.info("Successful login: user={}, ip={}",
            username, request.getRemoteAddr());
    } else {
        auditLog.warn("Failed login attempt: user={}, ip={}",
            username, request.getRemoteAddr());
        failedLoginTracker.record(username, request.getRemoteAddr());
    }
}
```

## Additional Security Checks

### Cryptography

**Look for**:
- Use of weak algorithms (MD5, SHA1, DES)
- Hardcoded encryption keys
- Missing initialization vectors
- Weak random number generators

**Vulnerable**:
```java
MessageDigest md = MessageDigest.getInstance("MD5");
Random random = new Random();
byte[] key = "hardcodedkey1234".getBytes();
```

**Secure**:
```java
MessageDigest md = MessageDigest.getInstance("SHA-256");
SecureRandom random = new SecureRandom();
byte[] key = loadKeyFromSecureStorage();
```

### API Security

**Look for**:
- Missing rate limiting
- No API authentication
- Excessive data exposure
- Missing input validation

**Secure Practices**:
```java
@RestController
@RequestMapping("/api/v1")
public class UserController {

    // Rate limiting
    @RateLimiter(name = "userApi")
    @GetMapping("/users")
    public Page<UserDto> getUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            Principal principal) {

        // Validate input
        if (size > 100) {
            throw new IllegalArgumentException("Page size too large");
        }

        // Return only necessary fields
        return userService.findAll(page, size)
            .map(this::toDto);
    }
}
```

## Security Review Checklist

When reviewing code, check:

- [ ] Input validation on all user inputs
- [ ] Output encoding for all user-controlled data
- [ ] Parameterized queries for all database access
- [ ] Authentication on all protected resources
- [ ] Authorization checks before accessing resources
- [ ] Secure password storage (bcrypt, Argon2)
- [ ] HTTPS for all data transmission
- [ ] Security headers (CSP, X-Frame-Options, etc.)
- [ ] Error handling that doesn't leak information
- [ ] Logging of security-relevant events
- [ ] Rate limiting on public APIs
- [ ] CSRF protection for state-changing operations
- [ ] Updated dependencies without known vulnerabilities
- [ ] Secrets stored in environment variables or vault
- [ ] Proper session management and timeout

## Reporting Security Issues

When documenting security findings:

```markdown
### [CRITICAL] SQL Injection in User Search

**Location**: UserController.java:45

**Issue**: User input is concatenated directly into SQL query, allowing SQL injection attacks.

**Vulnerable Code**:
```java
String query = "SELECT * FROM users WHERE name LIKE '%" + searchTerm + "%'";
```

**Impact**: Attackers can execute arbitrary SQL, potentially accessing all database data or modifying records.

**Recommendation**: Use parameterized queries with PreparedStatement.

**Fixed Code**:
```java
String query = "SELECT * FROM users WHERE name LIKE ?";
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, "%" + searchTerm + "%");
```

**Severity**: Critical
**CVSS Score**: 9.8 (Critical)
**Remediation Priority**: Immediate
```

## When This Skill Activates

This skill automatically activates when:
- Reviewing code for security vulnerabilities
- Performing security audits
- Analyzing authentication/authorization code
- Checking for OWASP Top 10 vulnerabilities
- Questions about secure coding practices
- Reviewing API security
- Analyzing cryptographic implementations
