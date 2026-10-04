---
name: contact-list
description: "Single source of truth for all contacts, PAs, and WhatsApp groups. Use when: looking up a phone number, email, address, PA, group JID, adding/updating a contact, or before sending any WhatsApp message. Reads and writes contact-list.md in the workspace root."
---

# Contact List Skill

## Minimum Model
Any model. This is a lookup/edit skill.

---

## Source File

All contact data lives in **`contact-list.md`** (workspace root). This is the ONLY source of truth.

❌ Do NOT use `data/contacts.md`, `PA_LIST.md`, `addresses.md`, `builders_leadership.md`, or `groups_index.md` — they are deprecated.

### File Structure

`contact-list.md` has these sections:

| Section | Content |
|---|---|
| **אנשי קשר** | Main contacts table: שם, טלפון, אימייל, כתובת, עיר, Owner Role, PA, הערות |
| **Active PAs** | PA↔Owner mapping with phones and status |
| **PA Sync List** | DM targets for pa-network-daily-sync |
| **Contacts Without PA** | Interested/pending PA contacts |
| **WhatsApp Groups** | All group JIDs (English + Hebrew) |

---

## Lookup

### Find a contact by name

```bash
grep -i "SEARCH_TERM" /path/to/workspace/contact-list.md
```

Replace `SEARCH_TERM` with the name (partial match OK, case-insensitive).

### Find a PA by owner name

```bash
grep -i "OWNER_NAME" /path/to/workspace/contact-list.md | head -5
```

The PA column in the contacts table shows `PA_NAME (+phone)`. The Active PAs section has the full mapping.

### Find a group JID

```bash
grep -i "GROUP_NAME" /path/to/workspace/contact-list.md
```

Look in the WhatsApp Groups section (bottom of file).

### Pre-send validation

Before sending any WhatsApp message:
1. `grep` the recipient's name or phone in `contact-list.md`
2. Verify the phone/JID exists
3. If not found → ask the owner. Never guess.

---

## Add a Contact

Append a new row to the **אנשי קשר** table in `contact-list.md`:

```
| Name | Phone | Email | Address | City | Owner Role | PA | Notes |
```

Rules:
- Check for duplicates first: `grep -i "NAME_OR_PHONE" contact-list.md`
- If the contact is from Builders Leadership → set `Owner Role` = `leadership`
- If they have a PA → fill the PA column with `PA_NAME (+phone)`
- Keep alphabetical order: Hebrew names (א-ת) first, then English (A-Z)
- After adding → `git add contact-list.md && git commit -m "add contact: NAME" && git push`

---

## Update a Contact

1. Read `contact-list.md`
2. Find the row to update
3. Edit the specific field (phone, address, PA, etc.)
4. After updating → `git add contact-list.md && git commit -m "update contact: NAME — FIELD" && git push`

---

## Add a New PA

When a new PA is onboarded:

1. **Add to Active PAs table** — new row with PA Name, Phone, Owner, Owner Phone, Status
2. **Update the contact row** — add PA name + phone to the PA column of the owner's entry
3. **Add to PA Sync List** — append DM target line: `- +PHONE — PA_NAME (Owner)`
4. **Git push** — `git add contact-list.md && git commit -m "add PA: PA_NAME for OWNER" && git push`

---

## Add a New Group

When joining a new WhatsApp group:

1. Add a row to the appropriate section (English or עברית) in the WhatsApp Groups table
2. Include: שם הקבוצה, Group JID, הערות
3. Git push

---

## Remove / Deactivate

- **Contact removed:** Delete the row. Git push.
- **PA deactivated:** Change status to `❌ לא פעיל` in Active PAs. Remove from PA Sync List DM targets. Keep the contact row but clear the PA column. Git push.

---

## Trigger Phrases

| If the owner says... | Action |
|---|---|
| "מי זה X" / "who is X" | Lookup by name |
| "מספר של X" / "X's number" / "phone for X" | Lookup phone |
| "כתובת של X" / "address for X" | Lookup address |
| "אימייל של X" / "email for X" | Lookup email |
| "PA של X" / "X's PA" / "find PA for X" | Lookup PA |
| "JID של X" / "group JID" | Lookup group |
| "add contact" / "הוסף איש קשר" | Add contact flow |
| "update contact" / "עדכן פרטים" | Update contact flow |
| "new PA" / "PA חדש" | Add PA flow (then also run ai-pa) |

---

## Cost Tips

- **Very cheap** — grep + file edit, any model works
- **No API calls** — everything is local markdown
- Batch multiple updates into one commit

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| Contact not found | Name spelling, partial match | Try shorter search term, check both Hebrew and English |
| Duplicate detected | Contact already exists | Update existing row instead of adding |
| File not found | `contact-list.md` missing | Check workspace root, run `git pull` |
| Git push failed | Network or auth issue | Retry, check git credentials |
