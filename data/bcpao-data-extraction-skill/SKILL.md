---
name: bcpao-data-extraction-skill
description: Extract property data from Brevard County Property Appraiser GIS API including photos, valuations, and parcel details
---

# BCPAO Data Extraction Skill

Extracts comprehensive property data from Brevard County Property Appraiser's GIS API.

## When to Use This Skill

- Stage 2 of Everest Ascent pipeline (Scraping)
- Getting property valuations for ARV calculations
- Retrieving property photos for reports
- Extracting parcel details for title research

## API Endpoint

**Base URL:**
```
https://gis.brevardfl.gov/gissrv/rest/services/Base_Map/Parcel_New_WKID2881/MapServer/5
```

**Operation:** `/query`

## Query Parameters

```python
params = {
    'where': f"PARCEL_ID = '{parcel_id}'",  # or SITE_ADDR LIKE '%123 Main St%'
    'outFields': '*',
    'returnGeometry': 'false',
    'f': 'json'
}
```

## Key Fields Returned

### Property Identification
- `PARCEL_ID`: Unique parcel identifier (e.g., "29-37-38-00-00000.0-000010.0")
- `ACCOUNT`: Account number for photo URLs
- `SITE_ADDR`: Full property address
- `LEGAL_DESC`: Legal description

### Ownership
- `OWNER_NAME`: Current owner of record
- `OWNER_ADDR`: Mailing address
- `MAIL_CITY`, `MAIL_STATE`, `MAIL_ZIP`

### Valuations
- `JUST_VAL`: Just (assessed) value
- `ASSESSED_VAL`: Assessed value for tax purposes
- `TAXABLE_VAL`: Taxable value after exemptions
- `LAND_VAL`: Land value only
- `BLDG_VAL`: Building value only

### Property Characteristics
- `LIV_AREA`: Living area in square feet
- `YR_BLT`: Year built
- `ZONING`: Zoning classification
- `USE_CODE`: Property use code
- `TOTAL_BEDROOMS`: Bedroom count (NOT RELIABLE - often missing)
- `TOTAL_BATHROOMS`: Bathroom count (NOT RELIABLE - often missing)

### Tax Information
- `TAX_DIST`: Tax district
- `EXEMPTIONS`: Homestead/other exemptions

## Photo URL Generation

Photos follow predictable pattern:

```python
def get_photo_url(account_number):
    # Format: https://www.bcpao.us/photos/{prefix}/{account}011.jpg
    # Account: 2934567 → prefix: 293, photo: 2934567011.jpg
    
    prefix = account_number[:3]
    photo_url = f"https://www.bcpao.us/photos/{prefix}/{account_number}011.jpg"
    return photo_url
```

**Example:**
- Account: `2934567`
- Prefix: `293`
- URL: `https://www.bcpao.us/photos/293/2934567011.jpg`

**Availability:**
- ~13/15 properties have photos (87% success rate)
- Returns 404 if photo doesn't exist
- Fallback: Use placeholder or note "No photo available"

## Data Limitations

### ❌ NOT Available in BCPAO API:
- Bedrooms (field exists but often null)
- Bathrooms (field exists but often null)
- Detailed property condition
- Recent sales comparables
- Interior features

### ✓ Available via BCPAO:
- Living area (reliable)
- Year built (reliable)
- Assessed values (reliable)
- Ownership (reliable)
- Photos (87% available)

### 🔍 Must Use Other Sources For:
- **Beds/Baths:** Zillow, Redfin, Realtor.com
- **Comps:** MLS, Zillow, recent sales
- **Condition:** Drive-by, photos, inspector
- **Rental rates:** Airbnb, Furnished Finder, Zillow

## Example Response

```json
{
  "features": [
    {
      "attributes": {
        "PARCEL_ID": "29-37-38-00-00000.0-000010.0",
        "ACCOUNT": "2934567",
        "SITE_ADDR": "123 MAIN ST",
        "OWNER_NAME": "SMITH JOHN & MARY",
        "JUST_VAL": 425000,
        "ASSESSED_VAL": 425000,
        "LAND_VAL": 125000,
        "BLDG_VAL": 300000,
        "LIV_AREA": 2150,
        "YR_BLT": 2005,
        "ZONING": "RES-1",
        "USE_CODE": "0100",
        "LEGAL_DESC": "LOT 10 BLOCK A SUBDIVISION PLAT..."
      }
    }
  ]
}
```

## ARV Calculation Strategy

Since BCPAO doesn't give comps, use multi-source approach:

### Step 1: BCPAO Baseline
```python
bcpao_value = response['JUST_VAL']  # Assessed value
```

### Step 2: Zillow/Redfin Comps
```python
# Search Zillow for recent sales within 0.5 miles
# Similar: beds, baths, sqft, year
comparable_sales = get_recent_sales(address, radius=0.5)
avg_comp_value = mean([sale['price'] for sale in comparable_sales])
```

### Step 3: Calculate ARV
```python
# Weight: 40% BCPAO, 60% comps
arv = (bcpao_value * 0.4) + (avg_comp_value * 0.6)

# Conservative adjustment
arv_conservative = arv * 0.95  # 5% haircut for safety
```

## Integration with Pipeline

```python
# Stage 2: Scraping
bcpao_data = bcpao_extraction_skill.query(parcel_id)

property_details = {
    'address': bcpao_data['SITE_ADDR'],
    'living_area': bcpao_data['LIV_AREA'],
    'year_built': bcpao_data['YR_BLT'],
    'assessed_value': bcpao_data['JUST_VAL'],
    'photo_url': get_photo_url(bcpao_data['ACCOUNT']),
    'legal_desc': bcpao_data['LEGAL_DESC']
}

# Use for ARV calculation in Stage 8
# Use photo in Stage 10 (Report Generation)
```

## Error Handling

```python
try:
    response = requests.get(api_url, params=params)
    data = response.json()
    
    if not data.get('features'):
        # Parcel not found
        return None
    
    # Extract first feature
    property_data = data['features'][0]['attributes']
    
except requests.exceptions.RequestException:
    # API timeout or error
    return None
```

## Example Usage

```
"Use bcpao-data-extraction-skill to get details for parcel 29-37-38-00-00000.0-000010.0"

"Extract BCPAO data for property at 123 Main St Melbourne FL"

"Get assessed value and photo for account 2934567"
```

## Best Practices

1. **Cache Results:** Don't query same parcel multiple times
2. **Handle Missing Photos:** 13% don't have photos, use fallback
3. **Don't Trust Bed/Bath:** BCPAO data unreliable, use Zillow/Redfin
4. **Use JUST_VAL for ARV:** Most accurate baseline value
5. **Verify Legal Desc:** Critical for title research
