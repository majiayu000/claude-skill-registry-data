---
name: spitakolus-tracking-analytics
description: Understand and work with Spitakolus shared tracking infrastructure. GTM containers, GA4 properties, BigQuery datasets, consent mode, and event naming.
dependencies: []
---

# Spitakolus Tracking & Analytics

## 🎯 Overview

All Spitakolus projects share tracking infrastructure with **project separation via hostname routing**.

**Golden Rule:** Data flows correctly when hostname conditions are set properly.

---

## 📊 Shared Infrastructure IDs

| System | ID | Purpose |
|--------|-----|---------|
| **GTM Web Container** | GTM-PD5N4GT3 | Shared, hostname routing |
| **GTM Server Container** | GTM-THB49L3K | Server-side tracking |
| **Server URL** | gtm.nastahem.com | First-party domain |
| **BigQuery Project** | nastahem-tracking | Shared data warehouse |

### GA4 Properties (per project)

| Project | Measurement ID | Domain |
|---------|----------------|--------|
| **Flocken** | G-7B1SVKL89Q | flocken.info |
| **Nästa Hem** | G-7N67P0KT0B | nastahem.com |

---

## 🔧 GTM Architecture

```
GTM-PD5N4GT3 (Shared Web Container)
├── Tags
│   ├── Google Tag - Flocken
│   │   ├── Tag ID: G-7B1SVKL89Q
│   │   └── Condition: Page Hostname = flocken.info
│   │
│   └── Google Tag - Nästa Hem
│       ├── Tag ID: G-7N67P0KT0B
│       └── Condition: Page Hostname = nastahem.com
│
└── Triggers (hostname-based)
    ├── Page View - Flocken (hostname = flocken.info)
    └── Page View - Nästa Hem (hostname = nastahem.com)
```

### Hostname Routing Rules

**ALWAYS use hostname conditions:**
- ✅ `Page Hostname equals flocken.info`
- ✅ `Page Hostname equals nastahem.com`
- ❌ Never use URL-based conditions
- ❌ Never omit conditions (causes cross-contamination)

---

## 📈 BigQuery Structure

```
nastahem-tracking/
├── flocken_raw/        # Raw GA4 export
├── flocken_curated/    # Cleaned data
├── flocken_marts/      # Business metrics
│
├── nastahem_raw/       # Raw GA4 export
├── nastahem_curated/   # Cleaned data
└── nastahem_marts/     # Business metrics
```

### Dataset Naming Convention

**Format:** `[project]_[type]`

| Type | Purpose |
|------|---------|
| `_raw` | Raw GA4 export (events_YYYYMMDD) |
| `_curated` | Cleaned, standardized events |
| `_marts` | Business intelligence metrics |

### Important: Location = EU

All datasets MUST be created with `location='EU'` for GDPR compliance.

---

## 🔐 Consent Mode v2

All projects use Consent Mode v2 with default denied:

```javascript
window.dataLayer.push({
  'event': 'consent_default',
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'functionality_storage': 'granted',
  'security_storage': 'granted'
});
```

**Cookie Banner Updates Consent:**
- User accepts → `gtag('consent', 'update', {...})`
- Tracking only fires AFTER consent granted

### GTM Tag Consent Controls

Every Google Tag must have these consent controls enabled:
- `ad_storage` ✅
- `ad_personalization` ✅
- `ad_user_data` ✅
- `analytics_storage` ✅

---

## 🏷️ Event Naming Convention

### Standard Events (GA4 Enhanced Measurement)
- `page_view` - Page loads
- `scroll` - 90% scroll depth
- `click` - Outbound links
- `file_download` - File downloads
- `video_start`, `video_progress`, `video_complete`

### Custom Events Format
**Format:** `[action]_[object]`

**Examples:**
- `sign_up` - User registration
- `app_install` - App installation
- `listing_created` - New listing
- `message_sent` - Message sent

### UTM Parameters
Always include for attribution:
- `utm_source` - Traffic source
- `utm_medium` - Marketing medium
- `utm_campaign` - Campaign name (use cid!)
- `utm_content` - Ad variation

---

## 🚀 Adding New Project to Tracking

### Step 1: Create GA4 Property
1. Google Analytics → Create Property
2. Save Measurement ID (G-XXXXXXXXXX)

### Step 2: Add to GTM
1. GTM → Container GTM-PD5N4GT3
2. Create new Google Tag with Measurement ID
3. **CRITICAL:** Add hostname trigger condition

### Step 3: Create BigQuery Datasets
```sql
CREATE SCHEMA `nastahem-tracking.[project]_raw` OPTIONS(location='EU');
CREATE SCHEMA `nastahem-tracking.[project]_curated` OPTIONS(location='EU');
CREATE SCHEMA `nastahem-tracking.[project]_marts` OPTIONS(location='EU');
```

### Step 4: Link GA4 → BigQuery
1. GA4 → Admin → BigQuery Linking
2. Project: nastahem-tracking
3. Location: EU
4. Dataset: [project]_raw

---

## ⚠️ Common Mistakes to Avoid

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Missing hostname condition | Data goes to wrong GA4 | Always add hostname trigger |
| Wrong Measurement ID | Data lost | Double-check ID |
| Dataset location != EU | GDPR violation | Always use EU |
| Consent not implemented | Legal issues | Use Consent Mode v2 |
| Hardcoded tracking IDs | Works in dev, fails in prod | Use environment variables |

---

## 🔍 Debugging Checklist

When tracking isn't working:

1. **GTM Preview Mode:** Is the right tag firing?
2. **Hostname check:** Is the condition correct?
3. **Consent check:** Did user accept cookies?
4. **Network tab:** Are requests going to google-analytics.com?
5. **GA4 Realtime:** Is data appearing?
6. **BigQuery:** Is export enabled and working?

---

## 📊 Growth Loop Integration

**Tracking is the foundation of the AI Growth Loop:**

1. **Data Collection** ← GTM + GA4 + BigQuery
2. **Analysis** ← Query BigQuery for patterns
3. **AI Generation** ← Use insights for new ads
4. **Optimization** ← Track performance, pause losers

**Every event you track becomes data for the Growth Loop.**

---

## 🔗 Detailed Documentation

- [GTM_SHARED_CONTAINER.md](../../tracking/GTM_SHARED_CONTAINER.md)
- [BIGQUERY_SHARED_PROJECT.md](../../tracking/BIGQUERY_SHARED_PROJECT.md)
- Project-specific: See each project's `docs/tracking/` folder
