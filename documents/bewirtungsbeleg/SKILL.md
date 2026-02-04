---
name: bewirtungsbeleg
description: Creates German tax-compliant entertainment expense receipts (Bewirtungsbelege) from restaurant receipts with automatic signature and original receipt attachment. The generated PDF contains the original receipt as page 1 and the signed Bewirtungsbeleg as page 2. Use when the user uploads a restaurant receipt/bill and wants to create a formal Bewirtungsbeleg PDF for German tax purposes, or when they mention "Bewirtungsbeleg", "Geschäftsessen", "steuerlich absetzbar", or similar business meal expense documentation needs.
---

# Bewirtungsbeleg Creator

This skill analyzes restaurant receipts and creates tax-compliant German Bewirtungsbeleg PDFs.

## Setup

Before using this skill for the first time:

1. **Configure your details:**
   ```bash
   cd skills/bewirtungsbeleg
   cp config.example.yml config.yml
   ```

2. **Edit `config.yml`** and replace the placeholder with your information:
   ```yaml
   gastgeber: "Your Name / Your Company Name"
   ```

3. **Add your signature:**
   - Place your signature image as `assets/signature.png`
   - See `assets/signature.example.png` for reference

4. **Install dependencies:**
   ```bash
   uv sync
   ```

The config file is gitignored to keep your personal information private when publishing this skill.

## Workflow

Follow this exact sequence when the user provides a restaurant receipt:

### Step 1: Analyze the Receipt

Extract the following information from the uploaded receipt image or PDF:

**Required from receipt:**
- Restaurant name and full address
- **Date of the meal (Rechnungsdatum)** - This will be used as "Datum der Bewirtung"
- **Location/City** - Extract from restaurant address, this will be used as "Ort der Bewirtung"
- Total amount including VAT (Gesamtbetrag/Bruttobetrag) - this is the only amount needed
- Receipt/register number (Registriernummer or Rechnungsnummer)

**Check carefully for tip (Trinkgeld) on receipt:**
- Look for any handwritten notes on the receipt mentioning "Trinkgeld", "Tip", "TG" or similar
- Check for a separate line item labeled "Trinkgeld" on the receipt
- Tips are often added by hand after the printed total
- If the receipt shows TWO totals, the difference is likely the tip
- Common patterns:
  - Original receipt shows €102, handwritten note "Trinkgeld €10", final amount €112
  - Receipt has printed "Summe: €102" and handwritten "Gesamt: €112"

**Important about tips:**
- If you see ANY indication of a tip on the receipt, extract that amount
- The `gesamtbetrag` in the JSON should be the FINAL total INCLUDING the tip
- The `trinkgeld` field should contain the tip amount separately
- If NO tip is visible, ask the user in Step 2

**Optional from receipt:**
- Tax ID or VAT ID (Steuer-Nr. or USt-IdNr.) of the restaurant

**Note:**
- The date and location from the receipt will be automatically used for the Bewirtungsbeleg
- You only need the total amount (Gesamtbetrag) - no need to split into net and VAT amounts
- The detailed itemization is on the original receipt which will be attached

**Tax ID Format Recognition:**

German tax IDs come in two formats:

1. **Steuernummer (Tax Number)**:
   - 10-11 digits, often with slashes: `133/8150/8159`
   - Or 13 digits without separators: `5133081508159`
   - Varies by Bundesland (federal state)

2. **Umsatzsteuer-Identifikationsnummer (VAT ID)**:
   - Always starts with "DE" followed by 9 digits
   - Format: `DE123456789`
   - Used for EU business transactions

**Important:** If no tax ID is found on the receipt, leave the field blank in the generated PDF. This is acceptable for tax purposes.

### Step 2: Gather Additional Information

Ask the user for information not available on the receipt, but only if not part of the prompt already:

**Always required:**
- **Bewirtete Personen (Guests):** Ask "Wer waren die bewirteten Personen?"
  - Collect full names
  - Company names are OPTIONAL - only ask if relevant or if the user mentions them
  - **CRITICAL**: THe host has to be added to the guest list as well

- **Anlass (Occasion):** Ask "Was war der Anlass der Bewirtung?"
  - The occasion must clearly demonstrate business context
  - Vague answers like "Geschäftsessen" are NOT sufficient for tax purposes
  - Guide the user to provide specific details, for example:
    - "Projektbesprechung zur Implementierung des CRM-Systems mit Kunde XY"
    - "Vertragsverhandlung über Cloud-Migration-Projekt"
    - "Akquisegespräch mit potenziellem Neukunden"

**Ask ONLY if not found on receipt:**
- **Trinkgeld (Tip):** If you did NOT find any indication of a tip on the receipt, ask "Wurde ein Trinkgeld gegeben? Falls ja, wie viel?"
  - If user says no tip was given, set trinkgeld to 0 in the JSON
  - If user provides a tip amount, add it to the receipt total for the final gesamtbetrag

**Note:** Date and location are automatically extracted from the receipt, so don't ask the user for these.

### Step 3: Create JSON Data Structure

Prepare a JSON file with all collected information:

```json
{
  "datum_bewirtung": "DD.MM.YYYY",  // Automatically from receipt date
  "ort_bewirtung": "City name",      // Automatically from restaurant address
  "gastgeber": "Full Name",          // Will use config.yml value if not provided in data
  "gaeste": [
    {
      "name": "Full Name",
      "unternehmen": "Company Name (optional)"
    },
    {
      "name": "Another Person"
    }
  ],
  "anlass": "Detailed business occasion",
  "restaurant_name": "Restaurant Name",
  "restaurant_adresse": "Full Address",
  "restaurant_steuernr": "Tax/VAT ID (optional)",
  "gesamtbetrag": 156.90,  // FINAL total INCLUDING tip (if any)
  "trinkgeld": 10.00       // Tip amount separately, use 0.0 if no tip
}
```

**CRITICAL - Understanding gesamtbetrag and trinkgeld:**

**Example 1: Receipt WITH tip notation**
- Receipt shows: "Rechnung: 102,00 €"
- Handwritten on receipt: "Trinkgeld: 10,00 €"
- Your JSON should be:
  ```json
  {
    "gesamtbetrag": 112.00,  // 102 + 10
    "trinkgeld": 10.00
  }
  ```

**Example 2: Receipt WITHOUT tip notation, user confirms tip**
- Receipt shows: "Summe: 102,00 €"
- User says: "Yes, I gave 10 euros tip"
- Your JSON should be:
  ```json
  {
    "gesamtbetrag": 112.00,  // Receipt + tip
    "trinkgeld": 10.00
  }
  ```

**Example 3: No tip given**
- Receipt shows: "Summe: 102,00 €"
- No tip notation, user confirms no tip
- Your JSON should be:
  ```json
  {
    "gesamtbetrag": 102.00,
    "trinkgeld": 0.0
  }
  ```

**Important notes:**
- `datum_bewirtung`: Use the date from the receipt (Rechnungsdatum)
- `ort_bewirtung`: Extract the city from the restaurant address
- `gastgeber`: You can omit this field - the script will automatically use the value from config.yml
- `gesamtbetrag`: ALWAYS the final total INCLUDING tip (if any)
- `trinkgeld`: The tip amount separately; use 0.0 if no tip was given
- Net amount and VAT are NOT needed - they're already on the restaurant receipt

### Step 4: Generate the PDF

1. Save the JSON data to a temporary file
2. Save the uploaded original receipt to a temporary file (keep original format - PDF or image)
3. Execute the PDF generation script:
   ```bash
   python3 scripts/create_bewirtungsbeleg.py \
     --json data.json \
     --output bewirtungsbeleg.pdf \
     --receipt /path/to/uploaded/receipt
   ```

   **Note:** The signature is automatically loaded from `assets/signature.png` - no need to specify `--signature` parameter

4. The script will automatically:
   - Convert the receipt image to PDF if needed
   - Apply EXIF orientation correction to ensure the image is correctly oriented
   - Add the original receipt as the first page(s)
   - Create the Bewirtungsbeleg with the attached signature pre-filled
   - Add the signed Bewirtungsbeleg as the last page
   - Result: 2-page PDF (page 1 = original receipt, page 2 = signed Bewirtungsbeleg)

5. Move the generated PDF to `/mnt/user-data/outputs/`
6. Provide the download link to the user

**Important:**
- The `--receipt` parameter must point to the uploaded receipt file from `/mnt/user-data/uploads`
- **Supported formats**: PNG, JPEG, JPG, GIF, BMP, WebP, TIFF, TIF, HEIC, HEIF, and PDF
- **All color modes supported**: RGB, RGBA, CMYK, Grayscale, Palette, LAB, YCbCr, HSV
- The receipt can be a photo, scan, or PDF
- The signature is automatically included - stored in `assets/signature.png`
- The final PDF will have 2+ pages: original receipt first, then the signed Bewirtungsbeleg

### Step 5: Provide Instructions

After creating the PDF, inform the user:

**Document structure:**
- Page 1: Original restaurant receipt
- Page 2: Signed Bewirtungsbeleg (with automatic signature)

**What's already done:**
- ✅ Signature is already included automatically
- ✅ Original receipt is attached as first page
- ✅ Date and location are filled in

**User actions:**
- Print the complete PDF and file for tax records
- No manual signature needed - it's already signed!

**Tax note:**
- Business meal expenses are only 70% tax-deductible in Germany

## Important Notes

### Tax Compliance Requirements

- The receipt must be machine-generated (not handwritten)
- Must contain a receipt/register number
- Itemization of food/beverages is required
- For receipts over €250, the company name must be on the receipt
- The occasion must clearly demonstrate business connection
- Tax ID (Steuer-Nr. or USt-IdNr.) is helpful but not mandatory if missing

For detailed tax requirements, see `references/steuerliche_anforderungen.md`.

### Common Issues

**Insufficient occasion description:**
- ❌ Bad: "Geschäftsessen", "Besprechung"
- ✅ Good: "Projektbesprechung CRM-Implementation mit XY GmbH", "Vertragsverhandlung Cloud-Migration"

**Missing information:**
- If critical information is missing from the receipt (amounts, itemization), inform the user and explain what's needed
- If the tax ID is missing, that's acceptable - the field will be left blank on the Bewirtungsbeleg

**Tips (Trinkgeld):**
- Tips must be noted separately as they're usually not on the receipt
- Should be noted on the receipt and signed by the restaurant
- Must be included in the Bewirtungsbeleg

## Resources

### Scripts
- `scripts/create_bewirtungsbeleg.py` - Generates the PDF from JSON data, merges with original receipt, and adds signature

### References
- `references/steuerliche_anforderungen.md` - Complete German tax requirements for Bewirtungsbelege

### Assets
- `assets/signature.png` - (automatically included in generated PDFs)
