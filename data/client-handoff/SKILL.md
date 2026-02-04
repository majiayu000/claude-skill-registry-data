---
name: client-handoff
description: Project handover process for lead generation websites. Documentation, training, credentials, maintenance. Use when project complete.
---

# Client Handoff Skill

## Purpose

Produces handoff package for completed lead generation website. Documentation + training + access transfer.

## Scope

| ✅ Supported | ❌ Out of Scope |
|-------------|----------------|
| Lead gen sites | E-commerce/webshops |
| Static Astro sites | CMS with multi-editor |
| Single client | Agency white-label |
| Cloudflare Pages | Custom hosting |

## Skill Output

This skill produces:

| Artefact | Format | Required |
|----------|--------|----------|
| Site Documentation | PDF/Notion | ✅ |
| Credentials Document | Secure doc | ✅ |
| Training Recording | Loom video | ✅ |
| Analytics Access | GA4 Admin invite | ✅ |
| Maintenance Agreement | PDF | ✅ |

## Core Rules

1. **Documentation before handoff** — Nothing verbal-only
2. **Training session required** — Screen-recorded minimum
3. **Client sets all passwords** — Never store client passwords
4. **30-day support included** — Post-launch bug fixes
5. **Analytics access = Admin** — Client owns their data
6. **Search Console = Owner** — Full control to client

## Blocking Conditions (STOP)

Handoff BLOCKED if any:

| Condition | Check |
|-----------|-------|
| Site not approved | Written client approval |
| Documentation missing | All 5 artefacts ready |
| Training not done | Recording exists |
| Analytics not shared | Client has Admin |
| Search Console not shared | Client has Owner |
| No maintenance terms | Agreement signed |

**If blocked → FIX first, do not handoff.**

## Credentials Responsibility

| Item | Who Sets Password | Who Stores |
|------|-------------------|------------|
| Cloudflare | Client | Client |
| Domain registrar | Client | Client |
| GA4 | Google account | Client |
| Search Console | Google account | Client |
| CookieYes | Client | Client |

**Rule:** Developer NEVER stores client passwords. Client sets own passwords during handoff.

## Checklists

### Before Handoff Meeting

- [ ] Site fully tested and approved
- [ ] All content finalized
- [ ] Analytics confirmed working
- [ ] Documentation prepared
- [ ] Training agenda ready
- [ ] Loom/recording ready

### During Meeting

- [ ] Walk through site live
- [ ] Test form submission together
- [ ] Show analytics dashboard
- [ ] Explain maintenance terms
- [ ] Record entire session
- [ ] Client sets their passwords

### After Meeting (Same Day)

- [ ] Send documentation package
- [ ] Share recording link
- [ ] Add client to GA4 (Admin)
- [ ] Add client to Search Console (Owner)
- [ ] Send final invoice
- [ ] Schedule 30-day check-in

## Training Session

**Duration:** 30-45 minutes  
**Format:** Video call + screen share + recording

| Topic | Time | Covers |
|-------|------|--------|
| Site tour | 5 min | Live site, mobile, key pages |
| Forms | 5 min | Test submit, where leads go |
| Analytics | 10 min | GA4 dashboard, key metrics |
| Search Console | 5 min | Indexing, common issues |
| Content updates | 5 min | How to request, what's included |
| Q&A | 10 min | Questions, next steps |

## 30-Day Support Period

| Included | Not Included |
|----------|--------------|
| Bug fixes | New features |
| Form issues | Design changes |
| Analytics setup fixes | Content writing |
| Broken links | SEO campaigns |

After 30 days → Maintenance agreement terms apply.

## Forbidden

- ❌ Verbal-only handoff
- ❌ No documentation
- ❌ Storing client passwords
- ❌ Locking client out of accounts
- ❌ Unclear maintenance terms
- ❌ No training recording
- ❌ Handoff with blocking conditions

## References

- [documentation-template.md](references/documentation-template.md) — Site docs template
- [credentials-template.md](references/credentials-template.md) — Access doc template
- [maintenance-template.md](references/maintenance-template.md) — Agreement template
- [email-templates.md](references/email-templates.md) — Handoff emails

## Definition of Done

- [ ] All 5 artefacts delivered
- [ ] Training recorded and shared
- [ ] Client has GA4 Admin access
- [ ] Client has Search Console Owner
- [ ] Client set own passwords
- [ ] Maintenance agreement signed
- [ ] 30-day check-in scheduled
