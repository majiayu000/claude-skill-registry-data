---
name: vendor-management
description: Manage wedding vendors including registration, profiles, services, and communication. Use when working with vendors, vendor data, vendor services, vendor onboarding, vendor listings, or vendor-related database operations.
---

# Vendor Management Skill

This skill helps manage wedding vendors in TheFesta Events platform, including vendor registration, profile management, service listings, and communication.

## Core Vendor Operations

### 1. Vendor Registration & Onboarding

When adding a new vendor to the platform:

**Required Information:**
- Business name and legal entity
- Contact details (email, phone, address)
- Vendor category (venue, catering, photography, etc.)
- Business registration/license numbers
- Tax information (if applicable)
- Service areas/locations covered
- Years in business
- Portfolio/previous work samples

**Database Fields to Consider:**
```typescript
{
  name: string;
  email: string;
  phone: string;
  category: VendorCategory;
  description: string;
  services: Service[];
  location: Location;
  pricing: PricingInfo;
  availability: Availability;
  portfolio: Media[];
  reviews: Review[];
  status: 'pending' | 'active' | 'suspended';
}
```

### 2. Vendor Profile Management

**Profile Components:**
- Business overview and description
- Service offerings and packages
- Pricing tiers and packages
- Availability calendar
- Portfolio/gallery (images, videos)
- Reviews and ratings
- Certifications and awards
- Social media links
- Terms and conditions

**Best Practices:**
- Validate all contact information
- Ensure high-quality portfolio images
- Verify business credentials
- Set clear service descriptions
- Include transparent pricing

### 3. Service & Package Management

**Service Listing Structure:**
```typescript
{
  serviceName: string;
  description: string;
  category: string;
  basePrice: number;
  pricingType: 'fixed' | 'hourly' | 'package' | 'custom';
  features: string[];
  addOns?: AddOn[];
  maxCapacity?: number;
  duration?: string;
  customizable: boolean;
}
```

**Package Types:**
- Basic/Standard/Premium tiers
- Custom packages
- Seasonal offers
- Bundle deals
- Add-on services

### 4. Vendor Categories

Common vendor categories for wedding events:

**Venues:**
- Wedding venues
- Reception halls
- Outdoor spaces
- Destination venues

**Catering:**
- Full-service catering
- Dessert/cake specialists
- Bar services
- Food trucks

**Photography & Videography:**
- Wedding photographers
- Videographers
- Drone operators
- Photo booth services

**Decor & Flowers:**
- Florists
- Event decorators
- Lighting specialists
- Rental companies

**Entertainment:**
- DJs
- Bands/musicians
- MCs/hosts
- Dancers/performers

**Planning & Coordination:**
- Wedding planners
- Day-of coordinators
- Event designers

**Beauty & Fashion:**
- Hair stylists
- Makeup artists
- Bridal boutiques
- Tuxedo rentals

**Other Services:**
- Transportation
- Invitations/stationery
- Favors/gifts
- Honeymoon planning

## Vendor Communication

### Email Templates

**Welcome Email:**
```
Subject: Welcome to TheFesta Events - Vendor Partnership

Dear [Vendor Name],

Welcome to TheFesta Events! We're excited to have you join our platform
connecting couples with exceptional wedding vendors.

Your vendor profile is now live at: [Profile URL]

Next steps:
1. Complete your profile with portfolio images
2. Set up your service packages and pricing
3. Configure your availability calendar
4. Review and respond to inquiries promptly

Our team is here to support you. Contact us at vendor-support@thefestaevents.com

Best regards,
The TheFesta Team
```

**Inquiry Response Template:**
```
Subject: New Event Inquiry - [Event Date]

Dear [Vendor Name],

You have a new inquiry for:
- Event Type: [Wedding/Reception]
- Date: [Event Date]
- Location: [Location]
- Guest Count: [Number]
- Budget: [Budget Range]

Client Message:
[Message]

Please respond within 24 hours to maintain good response metrics.

[Respond to Inquiry Button]
```

### Communication Best Practices

- Respond to inquiries within 24 hours
- Maintain professional tone
- Provide clear pricing and availability
- Ask relevant questions to understand needs
- Send follow-up communications
- Request reviews after completed events

## Data Validation

### Required Validations

**Email Validation:**
- Valid email format
- Domain verification
- Unique email per vendor

**Phone Validation:**
- Valid phone format
- Country code verification
- SMS verification (optional)

**Business Validation:**
- Business license verification
- Tax ID validation
- Insurance verification
- Background checks (if applicable)

**Content Validation:**
- Portfolio images: max size, proper format
- Descriptions: minimum/maximum length
- Pricing: valid ranges
- Availability: valid date ranges

## Database Operations

### Common Queries

**Find vendors by category:**
```sql
SELECT * FROM vendors
WHERE category = ?
AND status = 'active'
AND location IN (?)
ORDER BY rating DESC;
```

**Find available vendors:**
```sql
SELECT v.* FROM vendors v
LEFT JOIN bookings b ON v.id = b.vendor_id
WHERE b.event_date != ?
OR b.id IS NULL
AND v.category = ?;
```

**Get vendor statistics:**
```sql
SELECT
  COUNT(*) as total_bookings,
  AVG(rating) as avg_rating,
  SUM(revenue) as total_revenue
FROM vendor_metrics
WHERE vendor_id = ?;
```

### Prisma Schema Examples

```prisma
model Vendor {
  id          String   @id @default(cuid())
  email       String   @unique
  name        String
  category    VendorCategory
  description String?
  phone       String?
  location    Location?
  services    Service[]
  bookings    Booking[]
  reviews     Review[]
  portfolio   Media[]
  status      VendorStatus @default(PENDING)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model Service {
  id          String   @id @default(cuid())
  vendorId    String
  vendor      Vendor   @relation(fields: [vendorId], references: [id])
  name        String
  description String
  basePrice   Float
  category    String
  features    String[]
  bookings    Booking[]
}
```

## Vendor Metrics & Analytics

### Key Performance Indicators (KPIs)

**Response Metrics:**
- Average response time
- Response rate
- Conversion rate (inquiries to bookings)

**Performance Metrics:**
- Total bookings
- Revenue generated
- Average booking value
- Repeat customer rate

**Quality Metrics:**
- Average rating
- Number of reviews
- Customer satisfaction score
- Complaint rate

**Engagement Metrics:**
- Profile views
- Inquiry volume
- Portfolio engagement
- Social media following

### Reports to Generate

1. **Monthly Performance Report**
   - Total bookings and revenue
   - New vs. returning customers
   - Top-performing services
   - Rating trends

2. **Vendor Comparison Report**
   - Performance vs. category average
   - Pricing competitiveness
   - Response time benchmarks

3. **Availability Report**
   - Upcoming availability
   - Peak booking periods
   - Capacity utilization

## Vendor Portal Features

### Dashboard Components

**Overview Section:**
- Total inquiries (pending/active)
- Upcoming bookings
- Recent reviews
- Revenue summary

**Calendar Section:**
- Availability calendar
- Booked dates
- Pending bookings
- Blocked dates

**Messages Section:**
- Inbox (client inquiries)
- Sent messages
- Automated notifications

**Analytics Section:**
- Performance metrics
- Booking trends
- Revenue analytics
- Rating history

## File Structure for Vendor Data

```
vendors/
├── {vendorId}/
│   ├── profile.json
│   ├── services.json
│   ├── portfolio/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── videos/
│   ├── contracts/
│   │   └── agreement.pdf
│   └── documents/
│       ├── license.pdf
│       └── insurance.pdf
```

## Error Handling

**Common Error Scenarios:**

1. **Duplicate Vendor Registration**
   - Check: Email already exists
   - Action: Prompt to log in or recover account

2. **Invalid Business Information**
   - Check: Business license validation
   - Action: Request manual verification

3. **Portfolio Upload Issues**
   - Check: File size, format, content
   - Action: Provide clear error messages and guidelines

4. **Availability Conflicts**
   - Check: Double bookings
   - Action: Alert vendor and suggest alternatives

5. **Payment/Pricing Errors**
   - Check: Valid pricing ranges
   - Action: Validate before saving

## Security Considerations

**Authentication:**
- Secure password requirements
- Two-factor authentication (optional)
- Session management

**Authorization:**
- Role-based access control
- Vendor can only access own data
- Admin override capabilities

**Data Protection:**
- Encrypt sensitive information
- Secure file uploads
- Audit logs for data changes
- GDPR compliance for personal data

## Integration Points

**Payment Processing:**
- Vendor commission calculation
- Payout schedules
- Transaction history

**Calendar Integration:**
- Google Calendar sync
- iCal export
- Availability sync

**Communication:**
- Email notifications
- SMS alerts
- In-app messaging

**Analytics:**
- Google Analytics integration
- Custom tracking events
- Performance dashboards

## Quick Reference Commands

**Add new vendor:**
Check for required fields, validate business info, create vendor record

**Update vendor profile:**
Validate changes, update database, notify vendor of changes

**List vendors by category:**
Query database with filters, apply sorting, return paginated results

**Generate vendor report:**
Aggregate metrics, calculate KPIs, format report, export as PDF/Excel

**Send vendor notification:**
Select template, personalize content, queue for delivery, track status

**Manage vendor availability:**
Update calendar, check conflicts, send confirmations, sync with external calendars
