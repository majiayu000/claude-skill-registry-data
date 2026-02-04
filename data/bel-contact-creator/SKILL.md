---
name: bel-contact-creator
description: This skill should be used when the user asks to create a contact in Outlook from freeform text data (e.g., business cards, email signatures, addresses). It handles parsing contact information and creating properly structured Outlook contacts that sync to mobile devices.
---

# Contact Creator

## Purpose

This skill enables creating Outlook contacts from freeform text input (business cards, email signatures, address blocks). It extracts contact information, structures it according to Microsoft 365 API requirements, and creates contacts that automatically sync to the user's mobile devices.

## When to Use

Use this skill when:
- User provides contact information in freeform text
- User asks to "create a contact" or "add to contacts"
- User provides business card information
- User wants contact information saved to Outlook

## Workflow

### Step 1: Verify MS365 Login

Before creating contacts, verify the user is logged into Microsoft 365:

```
mcp__ms365__login
```

If already logged in, the response will indicate success with user details.

### Step 2: Extract Contact Information

Parse the freeform text to extract:

**Required fields:**
- `displayName` - Full name (e.g., "Dr. Mathias Bach")
- `emailAddresses` - Array of email objects with `name` and `address`

**Common optional fields:**
- `givenName` - First name
- `surname` - Last name
- `title` - Title (e.g., "Dr.", "Prof.")
- `jobTitle` - Position (e.g., "Leiter Forschung & Entwicklung")
- `companyName` - Company name
- `businessPhones` - Array of phone numbers
- `businessAddress` - Object with `street`, `city`, `postalCode`, `countryOrRegion`
- `businessHomePage` - Website URL

**Field mapping guidelines:**
- Extract titles (Dr., Prof., etc.) to both `title` and include in `displayName`
- Mobile numbers go in `businessPhones` array (MS365 API doesn't always expose separate mobile field)
- Format addresses as objects with separate street, city, postal code, country
- Include website without protocol (e.g., "www.example.com")

Refer to `references/contact_fields.md` for complete field specifications.

### Step 3: Create Contact

Call the MS365 API to create the contact:

```
mcp__ms365__create-outlook-contact
```

Pass the structured contact data as JSON in the `body` parameter.

### Step 4: Confirm Creation

Display a confirmation to the user with:
- Contact name
- Key details (position, company, phone, email)
- Note about mobile sync

**Example confirmation:**

```
✅ Dr. Mathias Bach wurde zu Ihren Outlook-Kontakten hinzugefügt

Gespeicherte Daten:
- Name: Dr. Mathias Bach
- Position: Leiter Forschung & Entwicklung
- Firma: Herrmann Ultraschalltechnik GmbH & Co. KG
- Telefon: +49 175 2043181
- E-Mail: mathias.bach@herrmannultraschall.com
- Adresse: Descostr. 3-11, 76307 Karlsbad, Germany

Der Kontakt wird automatisch mit Ihrem Handy synchronisiert.
```

## Error Handling

**MS365 not logged in:**
- Run `mcp__ms365__login` and follow authentication flow
- Retry contact creation after successful login

**Missing required fields:**
- At minimum, `displayName` and one email address are required
- If missing, ask user for clarification

**API errors:**
- Display error message to user
- Suggest checking MS365 connection or permissions

## Tips

- German business contacts often have titles (Dr., Prof.) - include these
- Phone numbers can be stored with formatting (e.g., "+49 (7248) 79 1097")
- Fax numbers are not supported in the standard contact fields via API
- Website URLs work with or without "http://" prefix
- The skill handles both individual contacts and can be used multiple times for batch import

## Resources

### references/

This skill includes detailed documentation of Microsoft 365 contact fields in `references/contact_fields.md`. Refer to this file for complete API specifications and field mapping details.
