---
name: cui-javadoc
description: CUI JavaDoc documentation standards for Java classes, methods, and code examples
allowed-tools: [Read, Edit, Write, Grep, Glob]
---

# CUI JavaDoc Documentation Skill

Standards for writing high-quality JavaDoc documentation in CUI Java projects, ensuring consistency, completeness, and maintainability.

## Workflow

### Step 1: Load Applicable JavaDoc Standards

**CRITICAL**: Load current JavaDoc standards to use as enforcement criteria.

1. **Always load foundational JavaDoc standards**:
   ```
   Read: standards/javadoc-core.md
   ```
   This provides core JavaDoc principles, mandatory documentation requirements, basic tag usage, tag order, anti-patterns, and maintenance guidelines that apply to all JavaDoc documentation.

2. **Conditional loading based on documentation context**:

   **A. If documenting classes, interfaces, packages, enums, or annotations**:
   ```
   Read: standards/javadoc-class-documentation.md
   ```
   Provides comprehensive standards for package-info.java files, class/interface documentation, abstract classes, enums, annotations, inheritance, serialization, and generic types.

   **B. If documenting methods or fields**:
   ```
   Read: standards/javadoc-method-documentation.md
   ```
   Covers method documentation (public, private, overridden), field documentation, constructors, special method patterns (builders, factories, fluent APIs), generic methods, and varargs.

   **C. If adding code examples or complex formatting**:
   ```
   Read: standards/javadoc-code-examples.md
   ```
   Provides standards for inline code (`{@code}`, `{@literal}`), code blocks (`<pre><code>`), links (`{@link}`), HTML formatting, tables, lists, and complete code examples.

3. **Extract key requirements from all loaded standards**

4. **Store in working memory** for use during task execution

### Step 2: Analyze Existing Documentation (if applicable)

If working with existing JavaDoc:

1. **Identify documentation gaps**:
   - Check which public/protected APIs lack documentation
   - Identify incomplete parameter/return/exception documentation
   - Find "stating the obvious" documentation that should be improved or removed
   - Locate outdated documentation that doesn't match current code

2. **Assess documentation quality**:
   - Review clarity and usefulness of descriptions
   - Check if examples are complete and compilable
   - Verify all {@link} references are valid
   - Assess tag order and completeness
   - Check for proper HTML tag closure

3. **Review consistency**:
   - Verify consistent terminology across related classes
   - Check consistent tag ordering
   - Ensure uniform documentation style
   - Validate similar APIs are documented similarly

### Step 3: Write/Update JavaDoc According to Standards

When writing or updating JavaDoc:

1. **Apply core principles**:
   - Start with clear purpose statement (what and why)
   - Avoid stating the obvious
   - Focus on behavior, not implementation
   - Document contracts, not code details
   - Keep documentation synchronized with code

2. **Use proper tag structure** (if applicable):
   - Document all parameters with validation rules (@param)
   - Document return values with guarantees (@return)
   - Document all exceptions with conditions (@throws)
   - Add cross-references with @see
   - Include version information (@since for public APIs)
   - Provide migration path for deprecated APIs (@deprecated)
   - Follow standard tag order

3. **Apply class-level documentation** (if applicable):
   - Create or update package-info.java files
   - Document class purpose and behavior
   - Include thread-safety statements
   - Provide usage examples for complex classes
   - Document inheritance relationships
   - Document serialization if applicable

4. **Apply method-level documentation** (if applicable):
   - Document all public/protected methods
   - Include parameter constraints and validation rules
   - Document return value guarantees and null handling
   - Document exception conditions
   - Show examples for complex methods
   - Document overridden methods if they add behavior
   - Use builders/factories/fluent API patterns appropriately

5. **Add code examples and formatting** (if applicable):
   - Use `{@code}` for inline code
   - Use `{@literal}` for special characters
   - Use `{@link}` for class/method references
   - Create complete, compilable code blocks with `<pre><code>`
   - Include error handling in examples
   - Use HTML formatting (lists, paragraphs, headings) appropriately
   - Ensure all HTML tags are properly closed

### Step 4: Verify Documentation Quality

Before completing the task:

1. **Verify standards compliance**:
   - [ ] All public/protected APIs documented
   - [ ] No "stating the obvious" documentation
   - [ ] Proper tag order followed
   - [ ] All parameters/returns/exceptions documented
   - [ ] @since tags for public APIs
   - [ ] Migration paths for deprecated APIs

2. **Verify completeness**:
   - [ ] Class purpose clearly stated
   - [ ] Thread-safety documented where relevant
   - [ ] Null handling documented
   - [ ] Usage examples for complex APIs
   - [ ] All {@link} references valid

3. **Generate and review JavaDoc**:
   ```bash
   # Generate JavaDoc to check for warnings/errors
   ./mvnw javadoc:javadoc

   # Check generated HTML for formatting
   open target/site/apidocs/index.html
   ```

4. **Verify formatting**:
   - [ ] All HTML tags properly closed
   - [ ] Code blocks render correctly
   - [ ] Links work correctly
   - [ ] Examples are readable and correctly formatted

### Step 5: Report Results

Provide summary of:

1. **Documentation created/updated**: List classes, methods, packages documented
2. **Standards applied**: Which standards were followed
3. **Examples added**: Code examples and usage patterns included
4. **Links created**: Cross-references and @see tags added
5. **Any deviations**: Document and justify any standard deviations

## Quality Verification

### Documentation Completeness Checklist

- [ ] All public classes/interfaces documented
- [ ] All public/protected methods documented
- [ ] Package-info.java files present
- [ ] All parameters documented with constraints
- [ ] All return values documented
- [ ] All exceptions documented with conditions
- [ ] @since tags present for public APIs

### Content Quality Checklist

- [ ] Clear purpose statements (no "stating the obvious")
- [ ] Focus on behavior/contracts, not implementation
- [ ] Examples are complete and compilable
- [ ] Examples show error handling
- [ ] Examples follow project coding standards
- [ ] No outdated documentation
- [ ] Consistent terminology used

### Format Quality Checklist

- [ ] Proper tag order (param, return, throws, see, since, deprecated)
- [ ] All {@link} references valid
- [ ] HTML tags properly closed
- [ ] Code formatted with {@code} or <pre><code>
- [ ] Lists use proper HTML tags
- [ ] Paragraphs separated with <p>

### Generation Verification

- [ ] JavaDoc generation succeeds: `./mvnw javadoc:javadoc`
- [ ] No warnings or errors in output
- [ ] Generated HTML displays correctly
- [ ] Links navigate correctly
- [ ] Code examples render properly

## Common Patterns and Examples

### Basic Method Documentation

```java
/**
 * Validates the JWT token signature and expiration time against the configured
 * issuer and clock skew tolerance.
 *
 * @param token the JWT token to validate, must not be null or empty
 * @return validation result containing status and any error messages, never null
 * @throws IllegalArgumentException if token is null or empty
 * @since 1.2.0
 */
public ValidationResult validate(String token) {
    // Implementation
}
```

### Class Documentation with Example

```java
/**
 * Validates JWT tokens according to RFC 7519 specifications, verifying
 * signature, expiration, and issuer claims.
 *
 * <p>This validator supports both symmetric (HS256) and asymmetric (RS256)
 * signature algorithms.
 *
 * <p><b>Thread Safety:</b> This class is immutable and thread-safe.
 *
 * <p>Example usage:
 * <pre><code>
 * JwtTokenValidator validator = JwtTokenValidator.builder()
 *     .issuer("https://auth.example.com")
 *     .clockSkewSeconds(30)
 *     .build();
 *
 * ValidationResult result = validator.validate(jwtToken);
 * if (!result.isValid()) {
 *     log.warn("Token validation failed: {}", result.getErrors());
 * }
 * </code></pre>
 *
 * @see TokenValidator
 * @see ValidationResult
 * @since 1.2.0
 */
public class JwtTokenValidator implements TokenValidator {
    // Implementation
}
```

### Package Documentation (package-info.java)

```java
/**
 * Provides token validation and authentication services for OAuth2 and JWT tokens.
 *
 * <h2>Key Components</h2>
 * <ul>
 *   <li>{@link de.cuioss.portal.authentication.TokenValidator} - Main validation interface</li>
 *   <li>{@link de.cuioss.portal.authentication.JwtTokenParser} - JWT token parsing</li>
 *   <li>{@link de.cuioss.portal.authentication.OAuth2TokenValidator} - OAuth2 validation</li>
 * </ul>
 *
 * <h2>Usage Example</h2>
 * <pre><code>
 * TokenValidator validator = new JwtTokenValidator(issuerConfig);
 * ValidationResult result = validator.validate(bearerToken);
 * if (result.isValid()) {
 *     // Process authenticated request
 * }
 * </code></pre>
 *
 * @since 1.0.0
 * @author CUI Team
 */
package de.cuioss.portal.authentication;
```

### Builder Pattern Documentation

```java
/**
 * Sets the token issuer URL.
 *
 * @param issuer the issuer URL (must be valid HTTPS URL)
 * @return this builder for method chaining
 * @throws IllegalArgumentException if issuer is null or not a valid HTTPS URL
 */
public Builder issuer(String issuer) {
    // Implementation
    return this;
}

/**
 * Builds and returns a configured JWT token validator.
 *
 * @return a new JwtTokenValidator instance with the configured settings, never null
 * @throws IllegalStateException if required settings (issuer, publicKey) are not set
 */
public JwtTokenValidator build() {
    // Implementation
}
```

### Deprecated API Documentation

```java
/**
 * Validates a token using legacy validation rules.
 *
 * @param token the token to validate
 * @return true if valid, false otherwise
 * @deprecated since 2.0.0, use {@link #validate(String)} instead which
 *             returns detailed validation results and supports modern
 *             token formats. This method will be removed in 3.0.0.
 */
@Deprecated
public boolean validateLegacy(String token) {
    // Implementation
}
```

## Common Documentation Tasks

### Task: Document a new public class

1. Load javadoc-core.md and javadoc-class-documentation.md
2. Add class-level JavaDoc with purpose, thread-safety, and example
3. Document all public constructors
4. Document all public methods with params/returns/exceptions
5. Add @since tag with current version
6. Generate JavaDoc and verify

### Task: Add code examples to existing documentation

1. Load javadoc-core.md and javadoc-code-examples.md
2. Identify methods that need examples (complex APIs, common use cases)
3. Write complete, compilable examples with error handling
4. Use proper `<pre><code>` formatting
5. Ensure examples follow project coding standards
6. Generate JavaDoc and verify examples render correctly

### Task: Update documentation for API changes

1. Load javadoc-core.md and javadoc-method-documentation.md
2. Review changed methods/classes
3. Update parameter/return/exception documentation
4. Add @deprecated tags if removing APIs
5. Update @since tags if adding new parameters
6. Verify all {@link} references still valid
7. Generate JavaDoc and check for warnings

## Error Handling

If encountering issues:

1. **JavaDoc generation errors**: Review error messages, fix broken {@link} references and unclosed HTML tags
2. **Unclear documentation purpose**: Review core principles, focus on behavior not implementation
3. **Missing standards information**: Ask user for clarification on specific APIs or patterns
4. **Complex APIs to document**: Break down into steps, provide comprehensive examples
5. **Deprecated API migration**: Document clear migration path with code examples

## References

* Core JavaDoc Standards: standards/javadoc-core.md
* Class Documentation: standards/javadoc-class-documentation.md
* Method Documentation: standards/javadoc-method-documentation.md
* Code Examples and Formatting: standards/javadoc-code-examples.md
