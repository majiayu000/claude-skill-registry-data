---
name: using-web-search
description: Use when researching best practices, tutorials, and expert opinions using WebSearch and WebFetch tools - assesses source authority and recency to synthesize findings with citations
---

# Using Web Search

Use this skill when researching best practices, tutorials, and expert opinions using WebSearch and WebFetch tools.

## Core Principles

- Search with specific, current queries
- Fetch promising results for detailed analysis
- Assess source authority and recency
- Synthesize findings with citations

## Workflow

### 1. Craft Search Query

**Be specific and current:**

```python
# ❌ Vague
WebSearch(query="authentication best practices")

# ✅ Specific
WebSearch(query="OAuth2 JWT authentication Node.js 2024")
```

**Query patterns:**
- Technology + use case + year: `"React server-side rendering 2024"`
- Problem + solution: `"avoid N+1 queries GraphQL"`
- Comparison: `"REST vs GraphQL microservices 2024"`
- Pattern: `"repository pattern TypeScript best practices"`

**Account for current date:**
- Current date from <env>: Check "Today's date"
- Use current/recent year in queries
- Avoid outdated year filters (e.g., don't search "2024" if it's 2025)

### 2. Domain Filtering

**Include trusted sources:**

```python
# Focus on specific domains
WebSearch(
    query="React performance optimization",
    allowed_domains=["react.dev", "web.dev", "kentcdodds.com"]
)
```

**Block unreliable sources:**

```python
# Exclude low-quality sites
WebSearch(
    query="TypeScript patterns",
    blocked_domains=["w3schools.com", "tutorialspoint.com"]
)
```

**Trusted sources by category:**

**Frontend:**
- react.dev, web.dev, developer.mozilla.org
- kentcdodds.com, joshwcomeau.com, overreacted.io

**Backend:**
- martinfowler.com, 12factor.net
- fastapi.tiangolo.com, docs.python.org

**Architecture:**
- microservices.io, aws.amazon.com/blogs
- martinfowler.com, thoughtworks.com

**Security:**
- owasp.org, auth0.com/blog, securityheaders.com

### 3. Fetch and Analyze

**Use WebFetch** for detailed content:

```python
# Fetch specific article
content = WebFetch(
    url="https://kentcdodds.com/blog/authentication-patterns",
    prompt="Extract key recommendations for authentication patterns, including code examples and security considerations"
)
```

**Fetch prompt patterns:**
- "Extract key recommendations for [topic]"
- "Summarize best practices with code examples"
- "List security considerations and common pitfalls"
- "Compare approaches mentioned with pros/cons"

### 4. Authority Assessment

**Evaluate sources:**

```markdown
Source: Kent C. Dodds - Authentication Patterns (2024)
Authority: ⭐⭐⭐⭐⭐
- Industry expert, React core contributor
- Recent publication (Jan 2024)
- Cited by 50+ articles
- Production examples from real apps
```

**Authority indicators:**
- ✅ Known experts in field
- ✅ Official documentation
- ✅ Recent publication dates
- ✅ Specific, detailed examples
- ✅ Acknowledges trade-offs

**Red flags:**
- ❌ No author/date
- ❌ Generic advice without context
- ❌ No code examples
- ❌ Outdated libraries/patterns
- ❌ Copy-pasted content

## Reporting Format

Structure findings as:

```markdown
## Web Research Findings

### 1. Authentication Best Practices

**Source:** Auth0 Blog - "Modern Authentication Patterns" (2024-10-15)
**Authority:** ⭐⭐⭐⭐⭐ (Official security vendor documentation)
**URL:** https://auth0.com/blog/authentication-patterns

**Key Recommendations:**

1. **Token Storage**
   > "Never store tokens in localStorage due to XSS vulnerabilities. Use httpOnly cookies for refresh tokens."

   - ✅ Refresh tokens → httpOnly cookies
   - ✅ Access tokens → memory only
   - ❌ localStorage for sensitive data

2. **Token Rotation**
   ```javascript
   // Recommended pattern
   const rotateToken = async (refreshToken) => {
     const { access, refresh } = await api.rotate(refreshToken)
     invalidateOldToken(refreshToken)
     return { access, refresh }
   }
   ```

**Trade-offs:**
- Memory-only tokens lost on refresh (need refresh flow)
- HttpOnly cookies require CSRF protection
- Complexity vs. security balance

---

### 2. Performance Optimization

**Source:** web.dev - "React Performance Guide" (2024-08)
**Authority:** ⭐⭐⭐⭐⭐ (Google official web platform docs)
**URL:** https://web.dev/react-performance

**Findings:**

1. **Code Splitting**
   - Lazy load routes: 40% faster initial load
   - Use React.lazy() + Suspense
   - Combine with route-based splitting

2. **Memoization Strategy**
   - useMemo for expensive computations (>16ms)
   - useCallback only when passed to memoized children
   - Don't over-optimize - measure first

**Benchmarks cited:**
- Code splitting: 2.1s → 1.3s load time
- Proper memoization: 15% render reduction
```

## Search Strategies

### Pattern Discovery
```python
WebSearch(query="factory pattern TypeScript best practices 2024")
```

### Problem Solutions
```python
WebSearch(query="prevent race conditions React useEffect")
```

### Technology Comparisons
```python
WebSearch(query="Prisma vs TypeORM PostgreSQL 2024")
```

### Migration Guides
```python
WebSearch(query="migrate Express to Fastify performance")
```

## Anti-Patterns

❌ **Don't:** Search without year context
✅ **Do:** Include current year for recent practices

❌ **Don't:** Accept first result without verification
✅ **Do:** Fetch 2-3 sources, compare findings

❌ **Don't:** Copy recommendations without understanding
✅ **Do:** Synthesize findings, note trade-offs

❌ **Don't:** Skip source credibility check
✅ **Do:** Assess authority, recency, specificity

## Citation Format

Always cite findings:

```markdown
**Recommendation:** Use dependency injection for testability

Source: Martin Fowler - "Inversion of Control Containers" (2023)
URL: https://martinfowler.com/articles/injection.html
Authority: ⭐⭐⭐⭐⭐ (Industry thought leader, 20+ years)

Quote: "Constructor injection makes dependencies explicit and enables testing without mocks."
```

## Example Session

```python
# 1. Search for auth patterns
results = WebSearch(
    query="JWT refresh token rotation Node.js 2024",
    allowed_domains=["auth0.com", "oauth.net"]
)
# → Found 5 articles from Auth0, OAuth.net

# 2. Fetch most promising
article1 = WebFetch(
    url="https://auth0.com/blog/refresh-tokens-rotation",
    prompt="Extract token rotation implementation patterns and security considerations"
)
# → Got detailed rotation strategy with code

# 3. Fetch second source for comparison
article2 = WebFetch(
    url="https://oauth.net/2/refresh-tokens/",
    prompt="Summarize OAuth2 refresh token best practices"
)
# → Got official OAuth2 spec recommendations

# 4. Search for implementation gotchas
gotchas = WebSearch(
    query="JWT refresh token common mistakes pitfalls"
)
# → Found 3 articles on common errors

# 5. Synthesize findings
# Compare sources, note consensus vs. disagreement
# Highlight trade-offs and context-specific advice
```

## Quality Indicators

**High-quality findings have:**
- ✅ Multiple authoritative sources agree
- ✅ Publication dates within last 2 years
- ✅ Specific code examples with explanation
- ✅ Acknowledges trade-offs and context
- ✅ Cites benchmarks or case studies

**Reconsider if:**
- ❌ Only one source found
- ❌ Sources conflict without explanation
- ❌ Generic advice without specifics
- ❌ Outdated patterns (>3 years old for web)
- ❌ No consideration of modern alternatives
