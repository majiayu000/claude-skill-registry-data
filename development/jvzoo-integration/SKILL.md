---
name: jvzoo-integration
description: Expert JVZoo integration specialist for building backend systems that handle JVZoo purchases, create user accounts, manage software licenses, and process IPN notifications. Use when implementing JVZoo product licensing, account creation workflows, payment processing, refund handling, or connecting software products to JVZoo marketplace by product ID.
---

# JVZoo Integration Specialist

Expert guidance for building production-ready JVZoo integrations that handle purchases, license management, and account creation.

## Overview

JVZoo integration involves three core components:

1. **IPN (Instant Payment Notification)** - Real-time webhook from JVZoo when purchases occur
2. **License Management** - Generate, validate, and track software licenses
3. **Account Creation** - Automatically create user accounts from purchase data

## IPN Setup & Security

### IPN Endpoint Requirements

Your IPN endpoint must:
- Accept POST requests from JVZoo servers
- Respond within 10 seconds with HTTP 200
- Validate authenticity using secret key
- Handle idempotent processing (duplicates possible)
- Log all requests for debugging

### IPN Verification

Always verify IPN authenticity using SHA-1 hash:

```
Verification Hash = SHA1(secretKey + "|" + transactionId + "|" + amount + "|" + productId)
```

Compare this hash with the `cverify` parameter sent by JVZoo. Never process unverified IPNs.

### Essential IPN Parameters

**Transaction Info:**
- `ctransaction` - Transaction ID (use as idempotency key)
- `ctransaction_type` - SALE, RFND (refund), CGBK (chargeback), INSTAL (recurring), CANCEL-REBILL
- `ctransreceipt` - JVZoo receipt number
- `cproditem` - Product ID (your product identifier)
- `cprodtype` - STANDARD, RECURRING, etc.

**Customer Info:**
- `ccustemail` - Customer email (primary identifier)
- `ccustname` - Customer full name
- `ccustcc` - Customer country code
- `ccuststate` - Customer state/region

**Financial Info:**
- `ctransamount` - Sale amount
- `ctransaffiliate` - Affiliate commission
- `ctransvendor` - Your earnings

**Verification:**
- `cverify` - SHA-1 hash for verification

## Account Creation Workflow

### Step 1: Verify IPN

```javascript
function verifyIPN(ipnData, secretKey) {
  const { ctransaction, ctransamount, cproditem, cverify } = ipnData;
  const hash = crypto
    .createHash('sha1')
    .update(`${secretKey}|${ctransaction}|${ctransamount}|${cproditem}`)
    .digest('hex')
    .toUpperCase();
  
  return hash === cverify.toUpperCase();
}
```

### Step 2: Check for Duplicate Processing

```javascript
async function isDuplicateTransaction(transactionId) {
  // Query database for existing transaction
  const existing = await db.transactions.findOne({ 
    jvzoo_transaction_id: transactionId 
  });
  return !!existing;
}
```

### Step 3: Create or Update User Account

```javascript
async function processNewSale(ipnData) {
  const { ccustemail, ccustname, cproditem, ctransaction } = ipnData;
  
  // Find or create user
  let user = await db.users.findOne({ email: ccustemail });
  
  if (!user) {
    user = await db.users.create({
      email: ccustemail,
      name: ccustname,
      created_via: 'jvzoo',
      jvzoo_transaction: ctransaction
    });
  }
  
  return user;
}
```

### Step 4: Generate License Key

```javascript
function generateLicenseKey(userId, productId, transactionId) {
  const timestamp = Date.now();
  const data = `${userId}:${productId}:${transactionId}:${timestamp}`;
  const hash = crypto
    .createHash('sha256')
    .update(data + process.env.LICENSE_SECRET)
    .digest('hex');
  
  // Format: XXXX-XXXX-XXXX-XXXX
  return hash.substring(0, 16).toUpperCase().match(/.{1,4}/g).join('-');
}
```

### Step 5: Store License & Send Access

```javascript
async function createLicense(userId, productId, ipnData) {
  const licenseKey = generateLicenseKey(
    userId, 
    productId, 
    ipnData.ctransaction
  );
  
  const license = await db.licenses.create({
    user_id: userId,
    product_id: productId,
    license_key: licenseKey,
    jvzoo_transaction: ipnData.ctransaction,
    jvzoo_receipt: ipnData.ctransreceipt,
    status: 'active',
    purchase_date: new Date(),
    transaction_type: ipnData.ctransaction_type
  });
  
  // Send email with license key and login details
  await sendWelcomeEmail(userId, licenseKey);
  
  return license;
}
```

## Transaction Type Handling

### SALE (New Purchase)

```javascript
case 'SALE':
  await processNewSale(ipnData);
  await createLicense(user.id, ipnData.cproditem, ipnData);
  break;
```

### RFND (Refund)

```javascript
case 'RFND':
  await db.licenses.update(
    { jvzoo_transaction: ipnData.ctransaction },
    { status: 'refunded', refunded_at: new Date() }
  );
  await revokeAccess(user.id);
  break;
```

### CGBK (Chargeback)

```javascript
case 'CGBK':
  await db.licenses.update(
    { jvzoo_transaction: ipnData.ctransaction },
    { status: 'chargeback', chargeback_at: new Date() }
  );
  await revokeAccess(user.id);
  break;
```

### INSTAL (Recurring Payment)

```javascript
case 'INSTAL':
  await db.licenses.update(
    { jvzoo_transaction: ipnData.ctransaction },
    { 
      status: 'active',
      last_payment: new Date(),
      payment_count: { $inc: 1 }
    }
  );
  break;
```

### CANCEL-REBILL (Subscription Cancelled)

```javascript
case 'CANCEL-REBILL':
  await db.licenses.update(
    { jvzoo_transaction: ipnData.ctransaction },
    { 
      status: 'cancelled',
      cancelled_at: new Date()
    }
  );
  // Grace period before revoking access
  await scheduleAccessRevocation(user.id, 30); // 30 days
  break;
```

## License Validation API

Build an API endpoint your software calls to validate licenses:

```javascript
// POST /api/validate-license
async function validateLicense(req, res) {
  const { license_key, email } = req.body;
  
  const license = await db.licenses.findOne({
    license_key: license_key,
    status: 'active'
  });
  
  if (!license) {
    return res.json({ valid: false, error: 'Invalid license' });
  }
  
  const user = await db.users.findById(license.user_id);
  
  if (user.email !== email) {
    return res.json({ valid: false, error: 'Email mismatch' });
  }
  
  // Update last validation timestamp
  await db.licenses.update(
    { _id: license._id },
    { last_validated: new Date() }
  );
  
  return res.json({
    valid: true,
    license: {
      product_id: license.product_id,
      expiry_date: license.expiry_date,
      features: license.features
    }
  });
}
```

## Database Schema Recommendations

### Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_via VARCHAR(50),
  jvzoo_transaction VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Licenses Table

```sql
CREATE TABLE licenses (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  product_id VARCHAR(100) NOT NULL,
  license_key VARCHAR(50) UNIQUE NOT NULL,
  jvzoo_transaction VARCHAR(255) UNIQUE NOT NULL,
  jvzoo_receipt VARCHAR(255),
  status VARCHAR(50) NOT NULL, -- active, refunded, chargeback, cancelled
  purchase_date TIMESTAMP NOT NULL,
  expiry_date TIMESTAMP,
  last_validated TIMESTAMP,
  transaction_type VARCHAR(50),
  refunded_at TIMESTAMP,
  chargeback_at TIMESTAMP,
  cancelled_at TIMESTAMP,
  payment_count INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Transactions Table (Audit Log)

```sql
CREATE TABLE jvzoo_transactions (
  id UUID PRIMARY KEY,
  jvzoo_transaction_id VARCHAR(255) UNIQUE NOT NULL,
  transaction_type VARCHAR(50) NOT NULL,
  product_id VARCHAR(100) NOT NULL,
  customer_email VARCHAR(255) NOT NULL,
  amount DECIMAL(10,2),
  raw_ipn_data JSONB,
  processed BOOLEAN DEFAULT FALSE,
  processed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Product ID Mapping

Map JVZoo product IDs to your internal product identifiers:

```javascript
const PRODUCT_MAPPING = {
  '123456': {
    name: 'AI Ranker Pro - Basic',
    features: ['feature1', 'feature2'],
    internal_id: 'ai-ranker-basic'
  },
  '123457': {
    name: 'AI Ranker Pro - Premium',
    features: ['feature1', 'feature2', 'feature3', 'feature4'],
    internal_id: 'ai-ranker-premium'
  },
  '123458': {
    name: 'Callfluent AI - Starter',
    features: ['100-calls', 'basic-voices'],
    internal_id: 'callfluent-starter'
  }
};

function getProductConfig(jvzooProductId) {
  return PRODUCT_MAPPING[jvzooProductId] || null;
}
```

## Security Best Practices

### Environment Variables

Never hardcode credentials:

```bash
JVZOO_SECRET_KEY=your_secret_key_here
LICENSE_SECRET=separate_key_for_license_generation
DATABASE_URL=your_database_connection
SMTP_API_KEY=email_service_key
```

### Rate Limiting

Protect your IPN endpoint from abuse:

```javascript
const rateLimit = require('express-rate-limit');

const ipnLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requests per IP
  message: 'Too many requests from this IP'
});

app.post('/ipn', ipnLimiter, handleIPN);
```

### Input Validation

Always validate and sanitize IPN data:

```javascript
function sanitizeIPNData(data) {
  return {
    ctransaction: String(data.ctransaction || '').trim(),
    ccustemail: String(data.ccustemail || '').toLowerCase().trim(),
    ccustname: String(data.ccustname || '').trim(),
    cproditem: String(data.cproditem || '').trim(),
    ctransamount: parseFloat(data.ctransamount || 0),
    // ... sanitize all fields
  };
}
```

### Error Handling

Always return 200 OK to prevent retries, but log errors:

```javascript
app.post('/ipn', async (req, res) => {
  try {
    // Always acknowledge receipt
    res.status(200).send('OK');
    
    // Process asynchronously
    await processIPN(req.body);
  } catch (error) {
    // Log error but don't tell JVZoo about it
    console.error('IPN Processing Error:', error);
    await logError(error, req.body);
  }
});
```

## Testing Your Integration

### Test Mode

JVZoo provides test IPNs. Look for test indicators:

```javascript
function isTestTransaction(ipnData) {
  return ipnData.ctransaction.toLowerCase().includes('test') ||
         ipnData.ccustemail.toLowerCase().includes('test');
}
```

### Manual IPN Testing

Send test IPN to your endpoint:

```bash
curl -X POST https://yoursite.com/ipn \
  -d "ctransaction=TEST123456" \
  -d "ccustemail=test@example.com" \
  -d "ccustname=Test User" \
  -d "cproditem=123456" \
  -d "ctransamount=97.00" \
  -d "ctransaction_type=SALE" \
  -d "cverify=YOUR_CALCULATED_HASH"
```

### Validation Checklist

- [ ] IPN verification working correctly
- [ ] Duplicate transactions prevented
- [ ] User accounts created successfully
- [ ] License keys generated and stored
- [ ] Welcome emails sent
- [ ] Refunds revoke access
- [ ] Chargebacks logged
- [ ] Recurring payments extend access
- [ ] All transactions logged for audit
- [ ] Error handling returns 200 OK

## Common Implementation Frameworks

### Node.js + Express

See `references/nodejs-implementation.md` for complete Express.js example with middleware, error handling, and database integration.

### Python + FastAPI

See `references/python-implementation.md` for FastAPI implementation with async handling and Pydantic validation.

### Next.js API Routes

See `references/nextjs-implementation.md` for serverless implementation using Next.js API routes with Supabase.

## Troubleshooting

**IPN not being received:**
- Check JVZoo IPN URL configuration in product settings
- Verify endpoint is publicly accessible (not localhost)
- Check firewall/server logs
- Ensure endpoint responds within 10 seconds

**Hash verification failing:**
- Verify secret key matches JVZoo dashboard
- Check parameter order in hash calculation
- Ensure string concatenation uses pipes (|)
- Convert hash to uppercase for comparison

**Duplicate accounts created:**
- Implement idempotency check using `ctransaction`
- Use database constraints on transaction ID
- Log all IPN requests to audit table

**License validation failing:**
- Check license status in database
- Verify email matches purchase email
- Ensure license hasn't been refunded/charged back
- Check for expiry dates on time-limited licenses

## Quick Start Template

For fastest implementation, use `scripts/setup_ipn_endpoint.js` to generate boilerplate IPN handler with your framework of choice (Express, FastAPI, Next.js).

See `references/deployment-guide.md` for production deployment considerations including SSL, monitoring, logging, and backup strategies.
