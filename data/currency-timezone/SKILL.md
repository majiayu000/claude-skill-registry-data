---
name: Currency and Timezone
description: Handling currency conversion, formatting, and timezone management for global applications to support users worldwide with local currency and time display.
---

# Currency and Timezone

> **Current Level:** Intermediate  
> **Domain:** Internationalization / Backend

---

## Overview

Currency and timezone handling is essential for global applications. Effective currency and timezone management ensures users see prices and times in their local format, supports multi-currency payments, and complies with local regulations.

## Why Currency and Timezone Matter

| Benefit | Description |
|---------|-------------|
| **Global Applications** | Support users worldwide |
| **User Expectations** | Local currency and time |
| **Business Requirements** | Multi-currency payments |
| **Compliance** | Local regulations |

## Timezone Fundamentals

### UTC (Coordinated Universal Time)

**Definition**: The primary time standard by which the world regulates clocks and time.

**Why Use UTC**:
- Timezone-independent
- No daylight saving time issues
- Standard for data storage

### Timezone Offsets

| City | Offset | UTC Time Example |
|------|--------|-----------------|
| New York | UTC-5 | 14:00 = 19:00 |
| London | UTC+0 | 14:00 = 14:00 |
| Bangkok | UTC+7 | 14:00 = 21:00 |
| Tokyo | UTC+9 | 14:00 = 23:00 |

### Daylight Saving Time (DST)

**Definition**: Clocks set forward in spring and back in autumn.

**Impact**:
- Confusing time calculations
- Schedule meetings carefully
- Store in UTC, display locally

### IANA Timezone Database

**Format**: `Area/Location`

| Timezone | Description |
|-----------|-------------|
| `America/New_York` | Eastern Time |
| `Europe/London` | UK Time |
| `Asia/Bangkok` | Indochina Time |
| `Asia/Tokyo` | Japan Time |

## Storing Dates and Times

### Always Store in UTC

```sql
-- Good: Store in UTC
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255),
    event_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Insert with explicit UTC
INSERT INTO events (event_name, event_time)
VALUES ('Meeting', '2024-01-15 14:00:00+00'::timestamp);
```

### Database Types

| Database | Type | Description |
|----------|-------|-------------|
| **PostgreSQL** | `TIMESTAMP WITH TIME ZONE` | Stores with timezone info |
| **MySQL** | `TIMESTAMP` | Stores in UTC (recommended) |
| **SQL Server** | `DATETIMEOFFSET` | Stores with timezone offset |

### PostgreSQL Timezone Handling

```sql
-- Convert to UTC
SELECT event_time AT TIME ZONE 'UTC' FROM events;

-- Convert to user timezone
SELECT event_time AT TIME ZONE 'America/New_York' FROM events;

-- Extract timezone info
SELECT
    event_time,
    EXTRACT(TIMEZONE FROM event_time) AS timezone_offset
FROM events;
```

### MySQL Timezone Handling

```sql
-- Store in UTC
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255),
    event_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Convert to UTC on insert
INSERT INTO events (event_name, event_time)
VALUES ('Meeting', CONVERT_TZ('2024-01-15 14:00:00', 'Asia/Bangkok', 'UTC'));
```

## JavaScript Timezone Handling

### Date Object

```javascript
// Date object uses browser timezone
const now = new Date();
console.log(now.toString()); // Local time
console.log(now.toISOString()); // UTC time
```

### Intl.DateTimeFormat

```javascript
// Format date for user's timezone
const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    timeZoneName: 'short'
});

console.log(formatter.format(new Date()));
// Output: January 15, 2024 at 9:00 AM EST
```

### Libraries

| Library | Description |
|----------|-------------|
| **date-fns-tz** | Timezone support for date-fns |
| **Luxon** | Modern date/time library |
| **Day.js** | Lightweight alternative to Moment.js |
| **Moment.js** | Deprecated, use alternatives |

### date-fns-tz Example

```javascript
import { format, utcToZonedTime, zonedTimeToUtc } from 'date-fns-tz';
import { utcToZonedTime } from 'date-fns-tz/utcToZonedTime';

// Convert UTC to user timezone
const utcDate = new Date('2024-01-15 14:00:00Z');
const userDate = utcToZonedTime(utcDate, 'America/New_York');
console.log(format(userDate, 'yyyy-MM-dd HH:mm:ss zzz'));

// Convert user timezone to UTC
const userDate = new Date('2024-01-15 09:00:00');
const utcDate = zonedTimeToUtc(userDate, 'America/New_York');
console.log(utcDate.toISOString());
```

### Luxon Example

```javascript
import { DateTime } from 'luxon';

// Create in UTC
const utcDate = DateTime.utc(2024, 1, 15, 14, 0, 0);
console.log(utcDate.toString()); // 2024-01-15T14:00:00.000Z

// Convert to user timezone
const userDate = utcDate.setZone('America/New_York');
console.log(userDate.toString()); // 2024-01-15T09:00:00.000-05:00

// Format for display
console.log(userDate.toFormat('yyyy-MM-dd HH:mm:ss zzz')); // 2024-01-15 09:00:00 EST
```

## Server-Side Timezone Handling

### Python (pytz)

```python
from datetime import datetime
import pytz

# Create timezone-aware datetime
utc_now = datetime.utcnow()
utc_tz = pytz.UTC.localize(utc_now)

# Convert to user timezone
user_tz = pytz.timezone('America/New_York')
user_now = utc_tz.astimezone(user_tz)

print(f"UTC: {utc_now}")
print(f"User: {user_now}")
```

### Python (dateutil)

```python
from datetime import datetime
from dateutil import tz

# Parse with timezone
user_date = datetime.strptime('2024-01-15 09:00:00', '%Y-%m-%d %H:%M:%S')
user_date = user_date.replace(tzinfo=tz.gettz('America/New_York'))

# Convert to UTC
utc_date = user_date.astimezone(tz.UTC)

print(f"User: {user_date}")
print(f"UTC: {utc_date}")
```

### Node.js (date-fns-tz)

```javascript
import { utcToZonedTime, format } from 'date-fns-tz';

// Convert UTC to user timezone
function formatForUser(utcDate, userTimezone) {
    const userDate = utcToZonedTime(utcDate, userTimezone);
    return format(userDate, 'yyyy-MM-dd HH:mm:ss zzz');
}

// Usage
const utcDate = new Date('2024-01-15 14:00:00Z');
const userTimezone = 'America/New_York';
console.log(formatForUser(utcDate, userTimezone));
```

### Java (ZonedDateTime)

```java
import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

// Create in UTC
ZonedDateTime utcDate = ZonedDateTime.of(2024, 1, 15, 14, 0, 0, ZoneId.of("UTC"));

// Convert to user timezone
ZonedDateTime userDate = utcDate.withZoneSameInstant(ZoneId.of("America/New_York"));

// Format
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss zzz");
System.out.println(userDate.format(formatter));
```

## User Timezone Detection

### Browser Detection

```javascript
// Get user's timezone
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
console.log(userTimezone); // e.g., "America/New_York"
```

### Server-Side Detection

```javascript
// Accept from client
app.get('/api/timezone', (req, res) => {
    const userTimezone = req.headers['x-user-timezone'] || req.query.timezone;
    // Store in user profile
    updateUserTimezone(req.user.id, userTimezone);
    res.json({ timezone: userTimezone });
});
```

### IP Geolocation (Fallback)

```javascript
// Use IP to guess timezone
const axios = require('axios');
const geoip = require('geoip-lite');

async function getTimezoneFromIP(ip) {
    const geo = geoip.lookup(ip);
    if (geo && geo.timezone) {
        return geo.timezone;
    }
    return 'UTC'; // Fallback
}
```

## Common Timezone Patterns

### User Sets Timezone in Profile

```
┌─────────────────────────────────────────────────────────────────┐
│  Timezone Selection                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Select your timezone:                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ (●) UTC                                              │   │
│  │ (  ) America/New_York                               │   │
│  │ (  ) Europe/London                                   │   │
│  │ (  ) Asia/Bangkok                                    │   │
│  │ (  ) Asia/Tokyo                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [Save Settings]                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Display All Dates in User's Timezone

```javascript
// Convert UTC to user timezone for display
function formatDateTime(utcDate, userTimezone) {
    return utcToZonedTime(utcDate, userTimezone)
        .toFormat('yyyy-MM-dd HH:mm:ss zzz');
}

// Usage
const eventDate = new Date('2024-01-15 14:00:00Z');
const userTimezone = getUserTimezone(userId);
console.log(formatDateTime(eventDate, userTimezone));
```

### Convert User Timezone to UTC on Write

```javascript
// Convert user input to UTC before storing
function parseUserDateTime(userDate, userTimezone) {
    const parsed = new Date(userDate);
    const userTz = tz.getTimezone(userTimezone);
    const utcDate = tz.utc(parsed);
    return utcDate.toJSDate();
}

// Usage
const userInput = '2024-01-15 09:00:00';
const userTimezone = 'America/New_York';
const utcDate = parseUserDateTime(userInput, userTimezone);
// Store utcDate in database
```

## Timezone Edge Cases

### DST Transitions

```javascript
import { utcToZonedTime, format } from 'date-fns-tz';

// Handle DST transitions
function formatWithDST(utcDate, userTimezone) {
    const userDate = utcToZonedTime(utcDate, userTimezone);
    const isDST = userDate.isDST;
    const formatted = format(userDate, 'yyyy-MM-dd HH:mm:ss zzz');
    return `${formatted} ${isDST ? '(DST)' : ''}`;
}

// Example: Spring forward (2:30 AM doesn't exist)
const springDate = new Date('2024-03-10 07:00:00Z'); // 2:00 AM EST
console.log(formatWithDST(springDate, 'America/New_York'));
// Output: 2024-03-10 03:00:00 EDT (DST)
```

### Ambiguous Times

```javascript
// Handle ambiguous times (fall back)
function handleAmbiguousTime(utcDate, userTimezone) {
    const userDate = utcToZonedTime(utcDate, userTimezone);
    if (userDate.isAmbiguous) {
        // Choose the earlier occurrence
        return userDate.setZone('UTC');
    }
    return userDate;
}

// Example: Fall back (1:30 AM occurs twice)
const fallDate = new Date('2024-11-03 06:00:00Z'); // 1:00 AM EST
console.log(handleAmbiguousTime(fallDate, 'America/New_York'));
```

### Non-Existent Times

```javascript
// Handle non-existent times (spring forward)
function handleNonExistentTime(utcDate, userTimezone) {
    const userDate = utcToZonedTime(utcDate, userTimezone);
    if (!userDate.isValid) {
        // Adjust to next valid time
        return userDate.plus({ hours: 1 });
    }
    return userDate;
}

// Example: Spring forward (2:30 AM doesn't exist)
const springDate = new Date('2024-03-10 07:30:00Z'); // 2:30 AM EST
console.log(handleNonExistentTime(springDate, 'America/New_York'));
// Output: 3:30 AM EDT
```

## Currency Fundamentals

### Currency Codes (ISO 4217)

| Code | Name | Symbol | Decimal Places |
|------|------|--------|----------------|
| USD | US Dollar | $ | 2 |
| EUR | Euro | € | 2 |
| GBP | British Pound | £ | 2 |
| JPY | Japanese Yen | ¥ | 0 |
| THB | Thai Baht | ฿ | 2 |

### Currency Symbols

| Code | Symbol | Position |
|------|--------|-----------|
| USD | $ | Prefix or suffix |
| EUR | € | Prefix or suffix |
| GBP | £ | Prefix |
| JPY | ¥ | Prefix |
| THB | ฿ | Prefix |

### Decimal Precision

| Currency | Decimal Places | Example |
|----------|-----------------|---------|
| USD | 2 | 99.99 |
| EUR | 2 | 99.99 |
| JPY | 0 | 100 |
| THB | 2 | 99.99 |
| BHD | 3 | 99.999 |

## Storing Currency

### Store Amount + Currency Code

```sql
-- Good: Store amount and currency separately
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO prices (product_id, amount, currency)
VALUES (1, 99.99, 'USD');
```

### Use DECIMAL Type

```sql
-- Bad: FLOAT (precision loss)
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL  -- Precision issues!
);

-- Good: DECIMAL (exact precision)
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL  -- Exact precision!
);
```

### Example Schema

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Currency Formatting

### Intl.NumberFormat

```javascript
// Format currency for user's locale
const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
});

console.log(formatter.format(99.99)); // $99.99

// Different locale
const formatterEUR = new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR'
});

console.log(formatterEUR.format(99.99)); // 99,99 €
```

### Different Formats by Locale

| Locale | Format | Example |
|--------|---------|---------|
| en-US | 1,000.00 | $1,000.00 |
| de-DE | 1.000,00 | 1.000,00 € |
| fr-FR | 1 000,00 | 1 000,00 € |
| th-TH | 1,000.00 | ฿1,000.00 |

### Symbol Position

```javascript
// Symbol position varies by locale
const formatterUS = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
});
console.log(formatterUS.format(100)); // $100.00

const formatterEU = new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR'
});
console.log(formatterEU.format(100)); // 100,00 €
```

## Multi-Currency Support

### Display Prices in User's Currency

```javascript
// Exchange rate cache
const exchangeRates = {
    USD: 1.0,
    EUR: 0.85,
    GBP: 0.75,
    THB: 35.0
};

function convertCurrency(amount, fromCurrency, toCurrency) {
    const rate = exchangeRates[toCurrency] / exchangeRates[fromCurrency];
    return amount * rate;
}

function formatCurrency(amount, currency, locale) {
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Usage
const priceUSD = 99.99;
const userCurrency = 'THB';
const userLocale = 'th-TH';
const priceTHB = convertCurrency(priceUSD, 'USD', userCurrency);
console.log(formatCurrency(priceTHB, userCurrency, userLocale)); // ฿3,499.65
```

### Store Prices in Base Currency

```sql
-- Store in base currency (USD)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price_usd DECIMAL(10,2) NOT NULL
);

-- Convert on display
SELECT
    name,
    price_usd,
    price_usd * 35.0 AS price_thb
FROM products;
```

### Exchange Rate API

```javascript
// Fetch exchange rates
async function getExchangeRates(baseCurrency) {
    const response = await fetch(`https://api.exchangerate.host/latest?base=${baseCurrency}`);
    const rates = await response.json();
    return rates;
}

// Usage
const rates = await getExchangeRates('USD');
console.log(rates.rates.THB); // 35.0
```

### Cache Exchange Rates

```javascript
// Simple in-memory cache
const exchangeRateCache = {
    rates: null,
    timestamp: null,
    ttl: 3600000 // 1 hour
};

async function getCachedExchangeRates(baseCurrency) {
    const now = Date.now();
    
    if (exchangeRateCache.timestamp && 
        now - exchangeRateCache.timestamp < exchangeRateCache.ttl) {
        return exchangeRateCache.rates;
    }
    
    const rates = await getExchangeRates(baseCurrency);
    exchangeRateCache.rates = rates;
    exchangeRateCache.timestamp = now;
    return rates;
}
```

## Currency Conversion

### Base Currency

```javascript
const BASE_CURRENCY = 'USD';

function convertToBase(amount, fromCurrency) {
    const rate = exchangeRates[BASE_CURRENCY] / exchangeRates[fromCurrency];
    return amount * rate;
}

function convertFromBase(amount, toCurrency) {
    const rate = exchangeRates[toCurrency] / exchangeRates[BASE_CURRENCY];
    return amount * rate;
}
```

### Show Original Currency

```javascript
// Tooltip with original currency
function formatPriceWithOriginal(amount, fromCurrency, toCurrency, locale) {
    const converted = convertCurrency(amount, fromCurrency, toCurrency);
    const formatted = formatCurrency(converted, toCurrency, locale);
    const original = formatCurrency(amount, fromCurrency, locale);
    
    return {
        formatted,
        original,
        tooltip: `Original: ${original} (${fromCurrency})`
    };
}
```

### Let User Switch Currency

```javascript
// Currency selector
function setCurrency(currency) {
    localStorage.setItem('userCurrency', currency);
    // Refresh page or update prices
}

function getUserCurrency() {
    return localStorage.getItem('userCurrency') || 'USD';
}

// Usage
<select onchange="setCurrency(this.value)">
    <option value="USD">USD ($)</option>
    <option value="EUR">EUR (€)</option>
    <option value="THB">THB (฿)</option>
</select>
```

## Payment Processing

### Charge in Customer's Currency

```javascript
// Stripe example
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

async function createPayment(amount, currency) {
    const paymentIntent = await stripe.paymentIntents.create({
        amount: Math.round(amount * 100), // Convert to cents
        currency: currency.toLowerCase(),
        payment_method_types: ['card'],
    });
    
    return paymentIntent;
}

// Usage
createPayment(99.99, 'USD'); // Charge $99.99 USD
createPayment(3499.65, 'THB'); // Charge ฿3,499.65 THB
```

### Payment Processor Support

| Processor | Currencies Supported |
|-----------|---------------------|
| **Stripe** | 135+ currencies |
| **PayPal** | 100+ currencies |
| **Braintree** | 130+ currencies |
| **Square** | 135+ currencies |

## Accounting Considerations

### Precision

```javascript
// Use DECIMAL for calculations
function calculateTotal(items) {
    return items.reduce((total, item) => {
        // Use precise arithmetic
        return total + (item.price * item.quantity);
    }, 0);
}
```

### Rounding

```javascript
// Banker's rounding (round to nearest even)
function roundBankers(amount) {
    return Math.round(amount * 2) / 2;
}

// Standard rounding
function roundStandard(amount) {
    return Math.round(amount);
}

// Currency-specific rounding
function roundCurrency(amount, currency) {
    const decimals = currency === 'JPY' ? 0 : 2;
    const multiplier = Math.pow(10, decimals);
    return Math.round(amount * multiplier) / multiplier;
}
```

## Libraries

### JavaScript

| Library | Description |
|----------|-------------|
| **Intl API** | Built-in browser/Node.js |
| **dinero.js** | Currency calculations |
| **currency.js** | Currency formatting |
| **accounting.js** | Precise financial calculations |

### Python

| Library | Description |
|----------|-------------|
| **Babel** | Internationalization |
| **forex-python** | Currency conversion |
| **py-moneyed** | Currency handling |

### Java

| Library | Description |
|----------|-------------|
| **Joda-Money** | Currency calculations |
| **JSR 354** | Java currency API |
| **ICU4J** | Internationalization |

## Common Mistakes

### Using FLOAT for Currency

```javascript
// Bad: Float precision loss
const price = 0.1 + 0.2; // 0.30000000000000004

// Good: Use decimal library
const { Dinero } = require('dinero.js');
const price = Dinero({ amount: 100, currency: 'USD' })
    .add(Dinero({ amount: 200, currency: 'USD' }));
```

### Not Storing Timezone with Dates

```sql
-- Bad: No timezone info
CREATE TABLE events (
    event_time TIMESTAMP NOT NULL  -- Ambiguous!
);

-- Good: Store in UTC
CREATE TABLE events (
    event_time TIMESTAMP WITH TIME ZONE NOT NULL  -- Explicit UTC
);
```

### Assuming User is in Server Timezone

```javascript
// Bad: Server timezone assumption
const eventDate = new Date('2024-01-15 14:00:00');

// Good: Convert to user timezone
const userTimezone = getUserTimezone(userId);
const eventDate = utcToZonedTime(new Date('2024-01-15 14:00:00Z'), userTimezone);
```

### Hardcoding Currency Symbols

```javascript
// Bad: Hardcoded symbol
const formatted = `$${price}`;

// Good: Use Intl API
const formatted = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
}).format(price);
```

## Implementation Examples

### Timezone Conversion Function

```javascript
import { utcToZonedTime, format } from 'date-fns-tz';

function formatDateTime(utcDate, userTimezone, userLocale) {
    const userDate = utcToZonedTime(utcDate, userTimezone);
    return format(userDate, 'PPP', {
        locale: userLocale
    });
}

// Usage
const utcDate = new Date('2024-01-15 14:00:00Z');
const userTimezone = 'America/New_York';
const userLocale = 'en-US';
console.log(formatDateTime(utcDate, userTimezone, userLocale));
// Output: January 15, 2024
```

### Currency Formatter Component

```javascript
import React, { useState, useEffect } from 'react';

function CurrencyDisplay({ amount, currency, locale }) {
    const [formatted, setFormatted] = useState('');
    
    useEffect(() => {
        const formatter = new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency
        });
        setFormatted(formatter.format(amount));
    }, [amount, currency, locale]);
    
    return <span>{formatted}</span>;
}

// Usage
<CurrencyDisplay amount={99.99} currency="USD" locale="en-US" />
```

### Multi-Currency Price Display

```javascript
import React, { useState, useEffect } from 'react';

function PriceDisplay({ priceUSD, userCurrency, userLocale }) {
    const [localPrice, setLocalPrice] = useState(null);
    
    useEffect(() => {
        async function fetchAndConvert() {
            const rates = await getCachedExchangeRates('USD');
            const converted = priceUSD * rates.rates[userCurrency];
            const formatted = new Intl.NumberFormat(userLocale, {
                style: 'currency',
                currency: userCurrency
            }).format(converted);
            setLocalPrice(formatted);
        }
        fetchAndConvert();
    }, [priceUSD, userCurrency, userLocale]);
    
    return (
        <div>
            <span title={`$${priceUSD.toFixed(2)} USD`}>
                {localPrice}
            </span>
        </div>
    );
}
```

## Summary Checklist

### Timezone

- [ ] Store all dates in UTC
- [ ] Convert to user timezone for display
- [ ] Handle DST transitions
- [ ] Handle ambiguous times
- [ ] Handle non-existent times
- [ ] Allow user to set timezone

### Currency

- [ ] Store amount + currency code
- [ ] Use DECIMAL type (not FLOAT)
- [ ] Format with Intl API
- [ ] Support multiple currencies
- [ ] Cache exchange rates
- [ ] Handle rounding correctly
- [ ] Allow user to switch currency
```

---

## Quick Start

### Currency Formatting

```javascript
const formatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
})

formatter.format(1234.56)  // "$1,234.56"
```

### Timezone Conversion

```javascript
const date = new Date('2024-01-15T10:00:00Z')

// Convert to user timezone
const userTimezone = 'America/New_York'
const formatter = new Intl.DateTimeFormat('en-US', {
  timeZone: userTimezone,
  dateStyle: 'full',
  timeStyle: 'long'
})

formatter.format(date)  // "Monday, January 15, 2024 at 5:00:00 AM EST"
```

---

## Production Checklist

- [ ] **Currency Storage**: Store prices in base currency
- [ ] **Currency Conversion**: Real-time or cached conversion rates
- [ ] **Currency Formatting**: Format according to locale
- [ ] **Timezone Storage**: Store all times in UTC
- [ ] **Timezone Conversion**: Convert to user timezone for display
- [ ] **Date Formatting**: Format dates according to locale
- [ ] **User Preferences**: Allow users to set currency and timezone
- [ ] **API Integration**: Integrate with currency exchange APIs
- [ ] **Caching**: Cache exchange rates
- [ ] **Testing**: Test with various locales
- [ ] **Documentation**: Document currency and timezone handling
- [ ] **Compliance**: Comply with local regulations

---

## Anti-patterns

### ❌ Don't: Store in User Currency

```javascript
// ❌ Bad - Store in user currency
const price = { amount: 100, currency: 'USD' }  // User changes currency!
```

```javascript
// ✅ Good - Store in base currency
const price = { amount: 100, currency: 'USD' }  // Base currency
// Convert on display
const displayPrice = convertCurrency(price, userCurrency)
```

### ❌ Don't: Store Local Time

```javascript
// ❌ Bad - Store local time
const createdAt = new Date('2024-01-15 10:00:00')  // Which timezone?
```

```javascript
// ✅ Good - Store UTC
const createdAt = new Date('2024-01-15T10:00:00Z')  // UTC
// Convert on display
const displayTime = convertToUserTimezone(createdAt, userTimezone)
```

---

## Integration Points

- **i18n Setup** (`25-internationalization/i18n-setup/`) - Internationalization
- **Localization** (`25-internationalization/localization/`) - Content localization
- **Payment Gateways** (`30-ecommerce/payment-gateways/`) - Multi-currency payments

---

## Further Reading

- [Intl API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl)
- [Currency Exchange APIs](https://www.exchangerate-api.com/)
- [Timezone Database](https://www.iana.org/time-zones)
