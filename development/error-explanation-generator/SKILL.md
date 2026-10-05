---
name: error-explanation-generator
description: Explain cryptic error messages, stack traces, and compiler errors in plain language with fix suggestions and prevention strategies. Use when encountering.
---

# Error Explanation Generator

Transforms cryptic error messages, stack traces, and compiler diagnostics into plain-language explanations with actionable fix suggestions. This skill covers common error patterns across major programming languages, provides systematic approaches to stack trace parsing, and offers prevention strategies to avoid recurring errors.

## When to Use This Skill

Use this skill for:

- Understanding a cryptic compiler error or warning that is not self-explanatory
- Parsing and interpreting a multi-frame stack trace to find the root cause
- Diagnosing runtime exceptions that occur intermittently or in production
- Explaining build tool errors (Maven, Gradle, npm, pip, cargo)
- Interpreting database error codes and connection failures
- Understanding HTTP error responses and API failures
- Translating low-level system errors (segfaults, OOM, permission denied) into actionable fixes
- Helping junior developers learn from error messages

**Trigger phrases**: "explain this error", "what does this error mean", "help me understand this stack trace", "fix this error", "debug this exception", "why am I getting this error", "error explanation", "stack trace help", "compiler error", "runtime exception"

## What This Skill Does

This skill provides structured error analysis:

- **Error Classification**: Categorizes errors by type (syntax, type, runtime, logic, configuration, environment, network, resource)
- **Plain Language Explanation**: Translates technical error messages into clear descriptions of what went wrong and why
- **Root Cause Analysis**: Traces from the error symptom back to the actual cause, which may be several layers removed from the error message
- **Fix Suggestions**: Provides specific, actionable code changes or configuration adjustments to resolve the error
- **Prevention Strategies**: Recommends coding practices, tooling, and patterns that prevent the error from recurring
- **Context-Aware Interpretation**: Considers the programming language, framework, and runtime environment when interpreting errors

## Instructions

### Step 1: Classify the Error Type

Determine which category the error falls into, as this guides the analysis approach.

| Error Category | Examples | Analysis Approach |
|---------------|----------|-------------------|
| **Syntax Error** | Missing semicolons, unclosed brackets, invalid tokens | Look at the exact line and character position; check for typos |
| **Type Error** | Type mismatch, invalid cast, null pointer | Trace the variable's type through assignments; check for null |
| **Import/Module Error** | Module not found, unresolved reference, classpath issues | Verify installation, check paths, confirm versions |
| **Runtime Exception** | IndexOutOfBounds, KeyError, NullPointerException | Examine the data that triggered the exception; check preconditions |
| **Configuration Error** | Invalid config, missing environment variable, wrong port | Check config files, environment, and deployment settings |
| **Build/Compilation Error** | Dependency conflict, version mismatch, missing plugin | Check build files, dependency tree, and tool versions |
| **Network Error** | Connection refused, timeout, DNS resolution failure | Check service availability, ports, firewalls, certificates |
| **Resource Error** | Out of memory, disk full, too many open files | Check resource usage, limits, and potential leaks |
| **Permission Error** | Access denied, insufficient privileges, read-only filesystem | Check file permissions, user roles, and security policies |
| **Concurrency Error** | Deadlock, race condition, thread starvation | Analyze lock ordering, shared state access, timing |

### Step 2: Parse the Error Message Structure

Most error messages follow a consistent structure. Identify each component.

#### Error Message Anatomy

```
[SEVERITY] [ERROR_CODE]: [DESCRIPTION]
  at [LOCATION] ([FILE]:[LINE]:[COLUMN])
  at [CALLER_LOCATION] ([FILE]:[LINE]:[COLUMN])
  ...
Caused by: [UNDERLYING_ERROR]
  at [LOCATION] ...
```

**Key components**:

- **Severity**: error, warning, fatal, panic
- **Error code**: numeric or symbolic code (e.g., E0308, TS2345, ENOENT)
- **Description**: human-readable message (often the most useful part)
- **Location**: file, line, column where the error was detected (not necessarily where the bug is)
- **Caused by chain**: nested exceptions showing the causal chain (read bottom-up for root cause)

### Step 3: Explain Common Error Patterns by Language

#### Python Common Errors

**TypeError: unsupported operand type(s) for +: 'int' and 'str'**

```python
# ERROR
age = 25
message = "I am " + age + " years old"
# TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Plain language explanation**: Python does not automatically convert between types when using the `+` operator. You are trying to concatenate a string with an integer, but Python requires both operands to be the same type.

**Fix**:

```python
# Option 1: Convert explicitly
message = "I am " + str(age) + " years old"

# Option 2: Use f-string (preferred)
message = f"I am {age} years old"

# Option 3: Use format()
message = "I am {} years old".format(age)
```

**Prevention**: Use f-strings consistently for string interpolation; they handle type conversion automatically.

---

**KeyError: 'username'**

```python
# ERROR
data = {"name": "Alice", "email": "alice@example.com"}
username = data["username"]
# KeyError: 'username'
```

**Plain language explanation**: You are trying to access a dictionary key that does not exist. The dictionary `data` has keys "name" and "email" but not "username".

**Fix**:

```python
# Option 1: Use .get() with a default value
username = data.get("username", "unknown")

# Option 2: Check existence first
if "username" in data:
    username = data["username"]
else:
    username = "unknown"

# Option 3: Use try/except for complex logic
try:
    username = data["username"]
except KeyError:
    logger.warning("Missing username field in data")
    username = generate_default_username(data)
```

**Prevention**: Use `.get()` with defaults for optional fields. Use TypedDict or dataclasses to enforce structure.

---

**ImportError: cannot import name 'foo' from 'bar'**

```python
# ERROR
from mypackage import MyClass
# ImportError: cannot import name 'MyClass' from 'mypackage'
```

**Plain language explanation**: Python found the package `mypackage` but could not find `MyClass` inside it. Common causes: the name is misspelled, the class was renamed or moved, the `__init__.py` does not export it, or you have a circular import.

**Fix checklist**:

1. Verify the exact name (case-sensitive): check the source file for the correct spelling
2. Check `__init__.py`: confirm the name is imported or defined in the package's `__init__.py`
3. Check for circular imports: if module A imports from module B and module B imports from module A, one of them will see an incomplete module
4. Verify installation: run `pip show mypackage` to confirm the correct version is installed

---

#### JavaScript Common Errors

**TypeError: Cannot read properties of undefined (reading 'map')**

```javascript
// ERROR
const response = await fetch("/api/users");
const data = await response.json();
const names = data.users.map(u => u.name);
// TypeError: Cannot read properties of undefined (reading 'map')
```

**Plain language explanation**: You are trying to call `.map()` on a value that is `undefined`. The `data.users` property does not exist on the response object, so accessing it returns `undefined`, and you cannot call methods on `undefined`.

**Fix**:

```javascript
// Option 1: Optional chaining with fallback
const names = data.users?.map(u => u.name) ?? [];

// Option 2: Defensive check
const names = Array.isArray(data.users) ? data.users.map(u => u.name) : [];

// Option 3: Validate response structure
if (!data.users || !Array.isArray(data.users)) {
    throw new Error(`Unexpected API response: missing 'users' array. Got: ${JSON.stringify(data)}`);
}
const names = data.users.map(u => u.name);
```

**Prevention**: Validate API response shapes using a schema validator (Zod, Joi, Ajv) before accessing nested properties.

---

**ReferenceError: X is not defined**

```javascript
// ERROR
function processData() {
    const result = calculateTotal(items);
    //                              ^
    // ReferenceError: items is not defined
}
```

**Plain language explanation**: You are referencing a variable (`items`) that has not been declared in the current scope or any enclosing scope. This usually means the variable was not passed as a parameter, was declared in a different scope, or was misspelled.

**Fix**: Pass the variable as a parameter, import it, or declare it in the correct scope.

**Prevention**: Use TypeScript for static analysis. Configure ESLint with `no-undef` rule.

---

**SyntaxError: Unexpected token '<'**

```
SyntaxError: Unexpected token '<' (at bundle.js:1:1)
```

**Plain language explanation**: The JavaScript parser encountered an HTML tag (`<`) where it expected JavaScript code. This almost always means a non-JavaScript file was served instead of the expected JavaScript bundle. The server returned an HTML error page (like a 404 page) instead of the JS file.

**Fix**:

1. Check the network tab in browser dev tools to see what the server actually returned for the script URL
2. Verify the script URL path is correct
3. Check that the build output directory is being served correctly
4. Verify the server is not returning an HTML 404 page for missing assets

---

#### Java Common Errors

**NullPointerException**

```java
// ERROR
String name = user.getAddress().getCity().toUpperCase();
// java.lang.NullPointerException: Cannot invoke "Address.getCity()"
// because the return value of "User.getAddress()" is null
```

**Plain language explanation**: You are calling a method on a `null` reference. `user.getAddress()` returned `null`, and then you tried to call `.getCity()` on that `null` value. Java cannot invoke methods on `null`.

**Fix**:

```java
// Option 1: Null checks
String name = "unknown";
if (user.getAddress() != null && user.getAddress().getCity() != null) {
    name = user.getAddress().getCity().toUpperCase();
}

// Option 2: Optional chain (Java 8+)
String name = Optional.ofNullable(user.getAddress())
    .map(Address::getCity)
    .map(String::toUpperCase)
    .orElse("unknown");

// Option 3: Null-safe utility
String name = Objects.toString(
    user.getAddress() != null ? user.getAddress().getCity() : null,
    "unknown"
).toUpperCase();
```

**Prevention**: Use `@NonNull` / `@Nullable` annotations. Configure NullAway or Checker Framework for compile-time null safety. Design domain objects to avoid nullable fields where possible.

---

**ClassNotFoundException / NoClassDefFoundError**

```java
// ERROR
Exception in thread "main" java.lang.ClassNotFoundException: com.example.MyService
    at java.base/java.net.URLClassLoader.findClass(URLClassLoader.java:445)
    at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:587)
```

**Plain language explanation**: The JVM cannot find the class `com.example.MyService` on the classpath at runtime. This means either the JAR containing this class is not included in the runtime classpath, the class was removed or renamed, or there is a version mismatch where an older version of the JAR is being used that does not contain this class.

**Fix checklist**:

1. Check that the dependency is declared in `pom.xml` or `build.gradle`
2. Run `mvn dependency:tree` or `gradle dependencies` to verify the dependency is resolved
3. Check for version conflicts: another dependency may be pulling in an older version
4. For runtime errors: verify the JAR is included in the deployment artifact (WAR, uber-JAR)
5. Check for typos in the fully qualified class name

---

**ConcurrentModificationException**

```java
// ERROR
List<String> names = new ArrayList<>(List.of("Alice", "Bob", "Charlie"));
for (String name : names) {
    if (name.startsWith("B")) {
        names.remove(name);  // ConcurrentModificationException
    }
}
```

**Plain language explanation**: You are modifying a collection while iterating over it with a for-each loop. Java's iterator detects that the underlying collection was structurally modified and throws this exception to prevent undefined behavior.

**Fix**:

```java
// Option 1: Use Iterator.remove()
Iterator<String> it = names.iterator();
while (it.hasNext()) {
    if (it.next().startsWith("B")) {
        it.remove();
    }
}

// Option 2: Use removeIf (Java 8+, preferred)
names.removeIf(name -> name.startsWith("B"));

// Option 3: Collect and remove separately
List<String> toRemove = names.stream()
    .filter(name -> name.startsWith("B"))
    .collect(Collectors.toList());
names.removeAll(toRemove);
```

**Prevention**: Always use `removeIf()` for conditional removal from collections. Never modify a collection inside a for-each loop.

### Step 4: Parse Multi-Frame Stack Traces

Stack traces are read from bottom to top for causation (the bottom frame is the root cause) but from top to bottom for the call chain (the top frame is where the error was detected).

#### Stack Trace Reading Strategy

1. **Start at the top**: the first line tells you the exception type and message
2. **Find your code**: scan down the frames looking for frames in your package/namespace (skip framework and library frames)
3. **Read the "Caused by" chain**: if present, the deepest "Caused by" is often the root cause
4. **Check the transition points**: where your code calls a library or framework, the mismatch between what you passed and what was expected is usually the bug

#### Python Stack Trace Example

```python
Traceback (most recent call last):
  File "app.py", line 45, in handle_request          # YOUR CODE: entry point
    result = process_order(request.json)
  File "services/orders.py", line 23, in process_order  # YOUR CODE: this is likely where the bug is
    validated = validate_order(data)
  File "services/validation.py", line 67, in validate_order  # YOUR CODE: deeper
    schema.validate(data)
  File "/venv/lib/jsonschema/validators.py", line 218, in validate  # LIBRARY
    raise ValidationError(msg)
jsonschema.exceptions.ValidationError: 'quantity' is a required property
```

**Reading**: Start at the bottom. The error is a `ValidationError` from the jsonschema library saying that "quantity" is a required property. Your code at `validation.py:67` called the schema validator. The data came from `orders.py:23`. The fix is to ensure the input data includes a "quantity" field before it reaches validation, or to handle the ValidationError gracefully.

### Step 5: Explain Build and Configuration Errors

#### npm / Node.js

**Error: Cannot find module 'express'**

```
Error: Cannot find module 'express'
Require stack:
- /app/src/server.js
```

**Explanation**: Node.js cannot find the "express" package. Either it was never installed, it was installed globally but not locally, or `node_modules` was deleted.

**Fix**: Run `npm install` in the project root. If express is not in `package.json`, run `npm install express`.

---

#### Maven / Java

**ERROR: Failed to execute goal ... Could not resolve dependencies**

```
[ERROR] Failed to execute goal on project my-app:
Could not resolve dependencies for project com.example:my-app:jar:1.0:
Could not find artifact com.example:my-library:jar:2.3.1
in central (https://repo.maven.apache.org/maven2)
```

**Explanation**: Maven cannot find version 2.3.1 of `com.example:my-library` in the configured repositories. Either this version does not exist, the artifact is in a private repository that is not configured, or there is a network issue.

**Fix**: Verify the correct version exists. Check `~/.m2/settings.xml` for private repository configuration. Run `mvn dependency:tree` to understand the dependency chain.

---

#### pip / Python

**ERROR: Could not find a version that satisfies the requirement**

```
ERROR: Could not find a version that satisfies the requirement
torch==2.1.0+cu118 (from -r requirements.txt (line 5))
ERROR: No matching distribution found for torch==2.1.0+cu118
```

**Explanation**: pip cannot find a package matching the exact version specifier. The `+cu118` suffix indicates a CUDA-specific build that may not be available from the default PyPI index.

**Fix**: Use the PyTorch-specific index URL: `pip install torch==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118`

### Step 6: Generate the Error Explanation Report

When explaining an error, use this structure:

```
## Error Explanation

### Error Message
{paste the exact error message}

### Classification
- **Type**: {syntax / type / runtime / build / config / network / resource / permission}
- **Language/Platform**: {Python 3.x / Node.js 18 / Java 17 / etc.}
- **Severity**: {fatal / error / warning}

### Plain Language Explanation
{1-3 sentences explaining what went wrong in non-technical terms}

### Root Cause
{What specifically caused this error -- the actual bug or misconfiguration}

### Fix
{Specific code or configuration change to resolve the error}

### Prevention
{How to avoid this error in the future -- tools, patterns, practices}

### Related Errors
{Other errors that are commonly confused with this one or stem from the same root cause}
```

## Best Practices

- **Read the entire error message before searching for solutions**: the message often contains the exact cause and even the fix; many developers stop reading after the error type
- **Focus on your code in stack traces, not framework code**: the bug is almost always in your code, not in the framework; find where your code calls the framework and examine what you passed
- **Read "Caused by" chains bottom-up**: the root cause is at the bottom of the chain; the top-level exception is often a generic wrapper
- **Check the exact line and character position**: compilers and interpreters point to where the error was detected, which is often at or near the actual problem
- **Reproduce the error before fixing it**: if you cannot reliably reproduce the error, you cannot verify that your fix works; capture the exact inputs and environment that trigger it
- **Search for the error code, not just the message**: error codes (E0308, TS2345, SQLSTATE 42P01) are more specific than messages and yield better search results
- **Consider the error context**: the same error message can have different causes depending on the framework, library version, and runtime environment
- **Keep a team error knowledge base**: document errors that are specific to your project, stack, or infrastructure so that team members do not waste time re-diagnosing the same issues
- **Use structured logging for production errors**: include request IDs, user context, and input data (redacted) in error logs to speed up diagnosis

## Common Pitfalls

- **Fixing the symptom instead of the root cause**: adding a null check to suppress a NullPointerException without understanding why the value is null leads to bugs that surface elsewhere
- **Copying StackOverflow solutions without understanding them**: blindly applying a fix may resolve the error but introduce new problems; understand why the fix works before applying it
- **Ignoring warnings**: compiler and linter warnings often predict future errors; a deprecation warning today becomes a runtime error after the next dependency upgrade
- **Assuming the error location is the bug location**: a NullPointerException on line 50 may be caused by a null assignment on line 20; trace the data flow backward from the error
- **Not reading the full stack trace**: developers often read only the first line; the middle frames and "Caused by" chains contain critical context
- **Conflating correlation with causation in intermittent errors**: an error that appears after a deployment may not be caused by the deployment; check for time-based triggers, data changes, or infrastructure events
- **Ignoring error codes**: error codes are more specific and stable than error messages, which may change between versions; always search by code when available
- **Not reproducing before fixing**: guessing at fixes for errors you cannot reproduce leads to wasted effort and false confidence; invest time in reproduction first
- **Suppressing errors with empty catch blocks**: catching and ignoring exceptions hides real problems; at minimum, log the exception; prefer handling it meaningfully
