---
name: supplier-management
description: Manage supplier pricelists, process Excel uploads, handle product catalogs, create selections, and generate stock reports. Use when working with supplier data, pricelist uploads, product selection workflows, or inventory management.
allowed-tools: Read, Edit, Grep, Glob, Bash, Write
---

# Supplier Management & Pricelist Processing

Expert assistance for the NXT-SPP (Supplier Pricelist Processing) system in MantisNXT.

## System Overview

The NXT-SPP system handles the complete workflow:
1. **Upload** - Import supplier pricelists (Excel/CSV)
2. **Validate** - Verify data quality and completeness
3. **Merge** - Integrate products into catalog
4. **Select** - Create product selections for inventory
5. **Stock Reports** - Generate inventory stock on hand reports

## Key Components

### Pricelist Upload

```typescript
// Upload endpoint
POST /api/suppliers/pricelists/upload

// Alternative SPP upload
POST /api/spp/upload

// File types supported
- .xlsx (Excel)
- .csv (CSV)
- .xls (Legacy Excel)
```

### Supplier Dashboard

Location: `src/components/suppliers/UnifiedSupplierDashboard.tsx`

Features:
- View all suppliers
- Upload pricelists
- Manage product catalogs
- Create selections
- Generate stock reports

### Portfolio Dashboard

Location: `src/components/spp/PortfolioDashboard.tsx`

Features:
- Overview of uploads and metrics
- Recent upload history
- Active selection status
- Quick actions

## Common Tasks

### Upload a Pricelist

```bash
# Test pricelist upload
curl -X POST "http://localhost:3000/api/suppliers/pricelists/upload" \
  -F "file=@path/to/pricelist.xlsx" \
  -F "supplierId=123"
```

### Check Upload Status

Uploads go through these statuses:
- `received` - File uploaded successfully
- `validating` - Checking data quality
- `validated` - Data is valid
- `merged` - Products added to catalog
- `failed` - Upload encountered errors

### Create a Selection

A selection defines which products to stock:
1. Choose products from supplier catalogs
2. Set quantities and parameters
3. Activate selection
4. Generate stock reports

### Generate Stock Report

With an active selection:
1. Navigate to Stock Reports tab
2. Select report type (by supplier, by category, etc.)
3. Export to Excel or view in UI

## Database Schema

### Core Tables

```sql
-- Suppliers
CREATE TABLE suppliers (
  supplier_id SERIAL PRIMARY KEY,
  supplier_name VARCHAR(255),
  contact_info JSONB
);

-- Pricelist Uploads
CREATE TABLE pricelist_uploads (
  upload_id SERIAL PRIMARY KEY,
  supplier_id INTEGER REFERENCES suppliers,
  filename VARCHAR(255),
  status VARCHAR(50),
  received_at TIMESTAMP,
  row_count INTEGER
);

-- Products
CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  sku VARCHAR(100) UNIQUE,
  supplier_id INTEGER REFERENCES suppliers,
  product_name VARCHAR(500),
  unit_price DECIMAL(10,2),
  category VARCHAR(100)
);

-- Selections
CREATE TABLE selections (
  selection_id SERIAL PRIMARY KEY,
  selection_name VARCHAR(255),
  is_active BOOLEAN,
  created_at TIMESTAMP
);

-- Selection Items
CREATE TABLE selection_items (
  item_id SERIAL PRIMARY KEY,
  selection_id INTEGER REFERENCES selections,
  product_id INTEGER REFERENCES products,
  quantity INTEGER
);
```

## File Upload Processing

### Excel File Structure

Expected columns (flexible mapping):
- SKU / Part Number / Item Code
- Product Name / Description
- Unit Price / Cost / Price
- Category / Type / Group
- Supplier Part # / Supplier SKU
- UOM (Unit of Measure)
- Stock Status

### Processing Flow

1. **File Validation**
   - Check file type and size
   - Verify readable format
   - Scan for required columns

2. **Data Extraction**
   - Parse Excel/CSV rows
   - Map columns to schema
   - Clean and normalize data

3. **Product Matching**
   - Match by SKU
   - Check for duplicates
   - Create new products or update existing

4. **Merge to Catalog**
   - Insert new products
   - Update prices
   - Track price changes
   - Log all modifications

## Service Layer

### PricelistService

Location: `src/lib/services/PricelistService.ts`

Key methods:
- `uploadPricelist()` - Handle file upload
- `validatePricelist()` - Validate data
- `processPricelist()` - Parse and extract data
- `mergePricelist()` - Merge into catalog

## React Query Hooks

Location: `src/hooks/useNeonSpp.ts`

Available hooks:
- `useDashboardMetrics()` - Get overview metrics
- `usePricelistUploads()` - List recent uploads
- `useActiveSelection()` - Get active selection
- `useSuppliers()` - List all suppliers
- `useProducts()` - Query product catalog

## Common Issues & Solutions

### Upload Fails

**Check:**
1. File format is supported (.xlsx, .csv)
2. File size is within limits
3. File has required columns
4. Data types match expectations
5. No duplicate SKUs within file

### Products Not Appearing

**Check:**
1. Upload status is "merged"
2. Products aren't filtered out
3. Supplier_id is correct
4. SKUs don't have validation errors

### Selection Not Activating

**Check:**
1. Only one selection can be active
2. Selection has items
3. Referenced products exist
4. Database constraints are met

### Stock Reports Empty

**Check:**
1. Active selection exists
2. Selection has items
3. Products are in inventory
4. Correct filters applied

## API Endpoints

```typescript
// Suppliers
GET    /api/suppliers                    // List suppliers
POST   /api/suppliers                    // Create supplier
GET    /api/suppliers/:id                // Get supplier details

// Pricelists
POST   /api/suppliers/pricelists/upload  // Upload pricelist
GET    /api/suppliers/pricelists         // List uploads
GET    /api/suppliers/pricelists/:id     // Upload details

// Products
GET    /api/products                     // Query products
GET    /api/products/:id                 // Product details

// Selections
GET    /api/selections                   // List selections
POST   /api/selections                   // Create selection
PUT    /api/selections/:id/activate      // Activate selection
GET    /api/selections/active            // Get active selection

// Reports
GET    /api/stock-reports                // Generate reports
GET    /api/stock-reports/export         // Export to Excel
```

## Best Practices

1. **Validate uploads** before merging to prevent data quality issues
2. **Test with small files first** to verify column mapping
3. **Keep one active selection** at a time for clarity
4. **Use consistent SKU format** across suppliers
5. **Review price changes** before activating selections
6. **Export stock reports regularly** for record keeping
7. **Monitor upload status** for errors
8. **Clean supplier data** for better matching

## Testing Workflow

```bash
# 1. Check suppliers exist
curl "http://localhost:3000/api/suppliers"

# 2. Upload test pricelist
curl -X POST "http://localhost:3000/api/suppliers/pricelists/upload" \
  -F "file=@test-pricelist.xlsx" \
  -F "supplierId=1"

# 3. Monitor upload status
curl "http://localhost:3000/api/suppliers/pricelists"

# 4. Verify products merged
curl "http://localhost:3000/api/products?supplierId=1"

# 5. Create selection
curl -X POST "http://localhost:3000/api/selections" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Selection", "items": [...]}'

# 6. Generate stock report
curl "http://localhost:3000/api/stock-reports"
```

## Performance Considerations

- Large pricelists (>10,000 rows) process in background
- Use batch operations for bulk product updates
- Index SKU columns for faster lookups
- Cache frequently accessed supplier data
- Paginate product lists for better UX

## Data Integrity

- Foreign keys enforce supplier-product relationships
- Unique constraints prevent duplicate SKUs
- Validation rules ensure data quality
- Audit logs track all changes
- Soft deletes preserve history
