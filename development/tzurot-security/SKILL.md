---
name: tzurot-security
description: Security best practices for Tzurot v3 - Secret management, AI-specific security (prompt injection, PII scrubbing), Economic DoS prevention, Discord permission verification, microservices security, and supply chain integrity. Use when handling secrets, user input, or security-critical code.
lastUpdated: '2025-12-21'
---

# Security Skill - Tzurot v3

**Use this skill when:** Handling secrets, user input, file uploads, AI providers, admin commands, or when security concerns arise.

## Quick Reference

```bash
# Pre-commit secret check
git diff --cached | grep -iE '(password|secret|token|api.?key|postgresql://|redis://)'

# Audit dependencies
npm audit --audit-level=moderate

# View Railway secrets (values hidden)
railway variables --service <name>
```

## 🚨 Tier 1: Core Security (MUST FOLLOW)

### 1. Never Commit Secrets

**Happened TWICE in this project. Always verify!**

| ❌ NEVER Commit              | ✅ Use Instead                   |
| ---------------------------- | -------------------------------- |
| Database URLs with passwords | Environment variables            |
| API keys/tokens              | `.env.example` with placeholders |
| Private keys                 | Railway secrets management       |
| Real user data in tests      | Generic test data                |

**If you commit a secret:**

1. **Rotate immediately** (regenerate in provider dashboard)
2. Update Railway: `railway variables set KEY=new-value`
3. Consider git history rewrite if not shared

### 2. Environment Variable Management

```typescript
// ✅ CORRECT - Fail fast if missing
const required = ['DISCORD_TOKEN', 'DATABASE_URL', 'REDIS_URL'] as const;
for (const v of required) {
  if (!process.env[v]) throw new Error(`Missing: ${v}`);
}
```

### 3. Security Logging (No PII)

```typescript
// ❌ WRONG - Logs PII
logger.info({ user }, 'User authenticated');
logger.debug({ token }, 'Initializing');

// ✅ CORRECT - Log only safe identifiers
logger.info({ userId: user.id }, 'User authenticated');
logger.debug({ tokenPrefix: token.slice(0, 10) }, 'Initializing');
```

**NEVER log:** Emails, phones, IPs, usernames, message content, API keys
**Safe to log:** User IDs, guild IDs, channel IDs, timestamps, error codes

### 4. Token Budgeting (Economic DoS Prevention)

AI APIs cost money. Implement per-user token limits:

```typescript
// In Redis: token_budget:{userId} → { tokensUsed, windowStart }
if (budget.tokensUsed + estimated > BUDGET_PER_HOUR) {
  return res.status(429).json({ error: 'Token budget exceeded' });
}
```

### 5. Discord Permission Verification

```typescript
// ❌ WRONG - Trusts client-side
if (interaction.member.permissions.has('Administrator')) {
}

// ✅ CORRECT - Server-side with cache
const guild = await client.guilds.fetch(guildId);
const member = await guild.members.fetch(userId);
const hasAdmin = member.permissions.has(PermissionFlagsBits.Administrator);
```

## 🛡️ Tier 2: Important Security (SHOULD IMPLEMENT)

### 6. PII Scrubbing Before Embedding

Scrub emails, phones, SSNs before storing in pgvector:

```typescript
const EMAIL_REGEX = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/g;
const scrubbedText = text.replace(EMAIL_REGEX, '<EMAIL_REDACTED>');
```

### 7. Prompt Injection Detection

```typescript
const JAILBREAK_PATTERNS = [
  /ignore (previous|all) (instructions|rules)/i,
  /dan mode/i,
  /developer mode/i,
  /forget (everything|all)/i,
];

if (JAILBREAK_PATTERNS.some(p => p.test(prompt))) {
  return { content: '⚠️ Prompt violates policies.', flagged: true };
}
```

### 8. Signed BullMQ Jobs (If Redis Compromised)

Sign jobs with HMAC to prevent injection:

```typescript
const signature = crypto.createHmac('sha256', SECRET).update(JSON.stringify(payload)).digest('hex');
// Include signature in job, verify in worker
```

### 9. Content Validation for Attachments

Validate using magic numbers, not extensions:

```typescript
import fileType from 'file-type';
const detected = await fileType.fromBuffer(buffer);
if (!ALLOWED_TYPES.includes(detected?.mime)) {
  /* reject */
}
```

### 10. Dependency Management

**Before installing ANY package:**

```bash
npm view <package>           # Exists?
npm audit                    # Vulnerabilities?
```

**Pin exact versions** in package.json (no `^` or `~`)

**Dependabot** handles weekly updates. See `.github/dependabot.yml`.

### 11. Discord Markdown Injection Prevention

**ALWAYS escape user-provided content** before displaying in Discord embeds:

```typescript
import { escapeMarkdown } from 'discord.js';

// ✅ CORRECT - Escape at display time
const displayName = escapeMarkdown(character.displayName);
embed.setTitle(`Character: ${displayName}`);

// ❌ WRONG - Raw user input in embed
embed.setTitle(`Character: ${character.displayName}`); // Vulnerable!
```

**Fields to always escape:**

- Guild names, channel names, usernames
- Character names, display names, persona fields
- Personality names, config names, preset names
- Any user-provided text in embeds

**Pattern:** Store raw values in data structures, escape at display time only.

## Admin Endpoint Security

Current: `X-Owner-Id` header validation
Future: HMAC signatures with `INTERNAL_SERVICE_SECRET`

```bash
# Rate limit admin endpoints
const adminRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, max: 10
});
```

## Red Flags - Consult This Skill When:

- Committing changes with credentials
- Handling user input to AI
- Processing file uploads
- Installing npm packages suggested by AI
- Implementing admin/destructive commands
- Logging anything with user data

## Related Skills

- **tzurot-observability** - Security logging without PII
- **tzurot-types** - Input validation with Zod schemas
- **tzurot-git-workflow** - Pre-commit verification checks

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Discord Bot Security](https://discord.com/developers/docs/topics/security)
- [Prompt Injection Primer](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/)
- Project post-mortems: `docs/postmortems/PROJECT_POSTMORTEMS.md`
