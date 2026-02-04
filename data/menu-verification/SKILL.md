---
name: menu-verification
description: Use this skill to verify whether restaurants actually have Planted products on their current menu. Crawls restaurant websites, parses PDF menus, and updates venue verification status in Firestore.
---

# Menu Verification Skill

This skill verifies whether discovered venues actually have Planted products on their current menus. It's essential for maintaining data quality - press releases and discovery don't guarantee ongoing availability.

## When This Skill Activates

**Triggers on:**
- Verifying newly discovered venues
- Re-checking venues marked as `unverified`
- Validating venues from press releases
- Auditing existing venue data quality

## Quick Start

### Run the Verification Agent

```bash
cd planted-availability-db/packages/scrapers

# Verify all unverified venues with websites
node verify-menu-agent.cjs

# Verify a specific venue by ID
node verify-menu-agent.cjs --venue-id=VENUE_ID_HERE
```

### What the Agent Does

1. **Finds unverified venues** with websites in Firestore
2. **Crawls the website** including subpages (/restaurant, /en, /de, etc.)
3. **Discovers PDF links** on the pages
4. **Tries common PDF paths** directly (/media/menu.pdf, /speisekarte.pdf, etc.)
5. **Parses PDF content** using pdf-parse library
6. **Searches for Planted keywords** (planted, plant-based, geschnetzeltes, etc.)
7. **Updates Firestore** with verification status and any dishes found

## Verification Statuses

| Status | Meaning |
|--------|---------|
| `verified_on_menu` | Planted products confirmed on current menu |
| `not_found_on_menu` | No Planted products found after thorough check |
| `unverified` | Not yet checked |
| `needs_manual_check` | Website couldn't be crawled, needs human verification |

## Manual Verification Workflow

For venues the agent can't verify automatically:

### 1. Check the Website Directly

```bash
# Get venue details
node -e "
const admin = require('firebase-admin');
admin.initializeApp({ credential: admin.credential.cert('../../service-account.json') });
const db = admin.firestore();
db.collection('venues').doc('VENUE_ID').get().then(d => console.log(JSON.stringify(d.data(), null, 2)));
"
```

### 2. Look for PDF Menus

Common PDF locations to check:
- `/media/menu.pdf`, `/media/speisekarte.pdf`
- `/downloads/menu.pdf`
- `/restaurant/menu.pdf`
- Language variants: `_en.pdf`, `_de.pdf`, `_d.pdf`

### 3. Search for Planted Keywords

In PDFs or HTML, search for:
- `planted` (brand name)
- `plant-based`, `plant based`, `pflanzenbasiert`
- `geschnetzeltes` (common planted dish)
- `planted chicken`, `planted kebab`, `planted steak`

### 4. Update the Venue

```bash
# Mark as verified with planted products
node -e "
const admin = require('firebase-admin');
admin.initializeApp({ credential: admin.credential.cert('../../service-account.json') });
const db = admin.firestore();
db.collection('venues').doc('VENUE_ID').update({
  status: 'active',
  verification_status: 'verified_on_menu',
  verification_date: new Date(),
  verification_method: 'manual',
  verification_note: 'Found X planted dishes on menu PDF',
  updated_at: new Date()
});
"

# Or mark as not found
node -e "
const admin = require('firebase-admin');
admin.initializeApp({ credential: admin.credential.cert('../../service-account.json') });
const db = admin.firestore();
db.collection('venues').doc('VENUE_ID').update({
  status: 'unverified',
  verification_status: 'not_found_on_menu',
  verification_date: new Date(),
  verification_method: 'manual',
  verification_note: 'No planted products found on menu',
  updated_at: new Date()
});
"
```

## Adding Dishes from Verified Menus

When planted products are found:

```bash
node -e "
const admin = require('firebase-admin');
admin.initializeApp({ credential: admin.credential.cert('../../service-account.json') });
const db = admin.firestore();

const dish = {
  venue_id: 'VENUE_ID',
  name: 'Planted Geschnetzeltes mit Rösti',
  description: 'Swiss-style planted strips with hash browns',
  price: { amount: 32.00, currency: 'CHF' },
  planted_products: ['planted.geschnetzeltes'],
  status: 'active',
  source: 'menu_verification',
  created_at: new Date(),
  updated_at: new Date()
};

db.collection('dishes').add(dish).then(ref => console.log('Added dish:', ref.id));
"
```

## Planted Product SKUs

Common product identifiers:
- `planted.chicken` - Planted Chicken
- `planted.geschnetzeltes` - Planted Geschnetzeltes (strips)
- `planted.kebab` - Planted Kebab
- `planted.steak` - Planted Steak
- `planted.pulled` - Planted Pulled
- `planted.schnitzel` - Planted Schnitzel

## Removing Invalid Venues

If a venue doesn't have planted products and was added in error:

```bash
# Delete venue (and its dishes)
node -e "
const admin = require('firebase-admin');
admin.initializeApp({ credential: admin.credential.cert('../../service-account.json') });
const db = admin.firestore();

const venueId = 'VENUE_ID';

// Delete dishes first
db.collection('dishes').where('venue_id', '==', venueId).get()
  .then(snap => {
    const batch = db.batch();
    snap.docs.forEach(doc => batch.delete(doc.ref));
    return batch.commit();
  })
  .then(() => db.collection('venues').doc(venueId).delete())
  .then(() => console.log('Deleted venue and dishes'));
"
```

## Agent Configuration

The verify-menu-agent.cjs searches for these patterns:

### Subpages Crawled
```javascript
const SUBPAGE_PATTERNS = [
  '/restaurant', '/en', '/de', '/bar', '/cuisine', '/kulinarik'
];
```

### PDF Paths Tried
```javascript
const COMMON_PDF_PATHS = [
  '/media/menu.pdf', '/media/speisekarte.pdf',
  '/media/restaurant_mo_-_fr_d.pdf', // Kronenhalle pattern
  '/downloads/menu.pdf', '/menu.pdf'
];
```

### Keywords Searched
```javascript
const PLANTED_KEYWORDS = [
  'planted', 'plant-based', 'plant based', 'pflanzenbasiert',
  'planted chicken', 'planted kebab', 'planted geschnetzeltes'
];
```

## Dependencies

The agent requires:
```bash
npm install pdf-parse  # For PDF text extraction
```

## Example Session

```
$ node verify-menu-agent.cjs

=== Menu Verification Agent ===
Found 3 unverified venues with websites

Checking: Kronenhalle (https://www.kronenhalle.com)
  Crawling homepage...
  Found 2 PDF links
  Parsing: restaurant_mo_-_fr_d.pdf (12 pages)
  FOUND: "Planted Geschnetzeltes «Kronenhalle» mit Rösti"
  FOUND: "Planted Steak mit Sanddorn"
  Status: verified_on_menu (2 dishes added)

Checking: Lindenhofkeller (https://www.lindenhofkeller.ch)
  Crawling homepage + subpages...
  Found 3 PDF links
  Parsing: drinks.pdf (31 pages) - no planted
  Parsing: lunch.pdf (4 pages) - no planted
  Parsing: dinner.pdf (6 pages) - no planted
  Status: not_found_on_menu

=== Summary ===
Verified: 1
Not found: 1
Errors: 0
```

## Troubleshooting

### PDF Not Parsing
- Check if pdf-parse is installed: `npm ls pdf-parse`
- Some PDFs are image-based (scanned) - need manual check
- Compressed PDFs may fail - try downloading manually

### Website Blocking
- Some sites block automated crawlers
- Try with different User-Agent
- May need manual verification

### No Menu Found
- Check if restaurant uses third-party menu systems
- Look for iframe embeds
- Check delivery platform listings instead
