---
name: fullstory-travel
version: v2
description: Industry-specific guide for implementing Fullstory in travel and hospitality applications including airlines, hotels, OTAs, car rentals, and vacation packages. Covers booking funnel optimization, search and filtering UX, payment handling (PCI), loyalty programs, and multi-traveler booking flows. Includes detailed examples for search, booking, check-in, and post-trip experiences.
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-analytics-events
  - fullstory-page-properties
  - fullstory-element-properties
---

# Fullstory for Travel & Hospitality

> ⚠️ **LEGAL DISCLAIMER**: This guidance is for educational purposes only and does not constitute legal, compliance, or regulatory advice. Travel applications are subject to various regulations (PCI DSS for payments, GDPR, airline-specific requirements, TSA/DHS regulations in the US). Always consult with your legal and compliance teams before implementing any data capture solution. Your organization is responsible for ensuring compliance with all applicable regulations.

## Industry Overview

Travel and hospitality have unique characteristics for session analytics:

- **High-value conversions**: Bookings often $500-$5,000+
- **Complex search**: Multi-leg trips, date ranges, passenger counts
- **Long consideration cycles**: Users often research across multiple sessions
- **Price sensitivity**: Fare changes, comparison shopping
- **Multi-traveler flows**: Booking for groups, families
- **Loyalty programs**: Points, tiers, member benefits
- **Regulatory requirements**: PCI for payments, some PII considerations

### Key Goals for Travel Implementations

1. **Optimize search-to-book conversion** funnel
2. **Understand abandonment** at each funnel stage
3. **Improve search and filtering** UX
4. **Reduce friction** in checkout and payment
5. **Enhance loyalty program** engagement
6. **Track ancillary upsells** (bags, seats, insurance)

---

## What Can Be Captured in Travel

| Data Type | Capture? | Privacy Level | Notes |
|-----------|----------|---------------|-------|
| Search criteria (dates, destinations) | ✅ Yes | Unmask | Core analytics |
| Flight/hotel options displayed | ✅ Yes | Unmask | Pricing analytics |
| Prices and fares | ✅ Yes | Unmask | Conversion analysis |
| Selected options | ✅ Yes | Unmask | Booking analytics |
| Ancillaries (bags, seats, meals) | ✅ Yes | Unmask | Upsell analytics |
| Traveler names | ⚠️ Mask | Mask | PII |
| Passport numbers | ❌ Never | Exclude | Government ID |
| Date of birth | ⚠️ Consider | Mask/Exclude | PII, may be needed for infant fares |
| Contact email/phone | ⚠️ Mask | Mask | PII |
| Payment card details | ❌ Never | Exclude | PCI |
| Loyalty numbers | ⚠️ Consider | Mask | Could be used for account takeover |
| TSA PreCheck / Known Traveler | ❌ Exclude | Exclude | Security sensitive |

### TSA Secure Flight Requirements (US Airlines)

For airlines operating in the US, TSA Secure Flight requirements mandate specific passenger data collection. **All Secure Flight data must be EXCLUDED**:

| Secure Flight Data | Why Exclude |
|--------------------|-------------|
| **Full legal name** | Required for TSA matching |
| **Date of birth** | Required for TSA matching |
| **Gender** | Required for TSA matching |
| **Redress Number** | DHS Traveler Redress Inquiry Program |
| **Known Traveler Number** | TSA PreCheck / Global Entry |
| **Passport information** | International travel verification |

```html
<!-- Travel: TSA Secure Flight data MUST be excluded -->
<fieldset class="fs-exclude secure-flight-data">
  <legend>Secure Flight Information (Required by TSA)</legend>
  
  <!-- ALL of this data must be excluded -->
  <input name="legal_first_name" />
  <input name="legal_middle_name" />
  <input name="legal_last_name" />
  <input name="date_of_birth" type="date" />
  <select name="gender">
    <option>Male</option>
    <option>Female</option>
    <option>Undisclosed</option>
  </select>
  <input name="redress_number" placeholder="Optional" />
  <input name="known_traveler_number" placeholder="Optional" />
</fieldset>
```

> **Important**: Track that the Secure Flight form was displayed and submitted (funnel step), but NEVER capture the actual data entered.

---

## Implementation Architecture

### Privacy Zones for Travel

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAVEL APPLICATION                            │
├─────────────────────────────────────────────────────────────────┤
│  FULLY VISIBLE (fs-unmask)                                       │
│  • Search form (destinations, dates, passengers)                │
│  • Search results (flights, hotels, prices)                     │
│  • Flight/room details                                          │
│  • Price breakdowns                                             │
│  • Ancillary options (bags, seats, insurance)                   │
│  • Filters and sort options                                     │
│  • Fare rules and policies                                      │
│  • Loyalty tier benefits (general)                              │
├─────────────────────────────────────────────────────────────────┤
│  MASKED (fs-mask)                                                │
│  • Traveler names                                               │
│  • Email addresses                                              │
│  • Phone numbers                                                │
│  • Billing address                                              │
│  • Loyalty member numbers                                       │
├─────────────────────────────────────────────────────────────────┤
│  EXCLUDED (fs-exclude)                                           │
│  • Passport numbers                                             │
│  • Date of birth                                                │
│  • Payment card details                                         │
│  • TSA PreCheck / Known Traveler numbers                        │
│  • Redress numbers                                              │
│  • Government ID uploads                                        │
│  • Security questions                                           │
└─────────────────────────────────────────────────────────────────┘
```

### User Identification Pattern

```javascript
// Travel: Use loyalty ID or internal customer ID
function onLogin(user) {
  FS('setIdentity', {
    uid: user.customerId,  // e.g., "CUST-12345"
    displayName: user.firstName  // Just first name
  });
  
  FS('setProperties', {
    type: 'user',
    properties: {
      // Loyalty program (valuable for segmentation)
      loyalty_tier: user.loyaltyTier,  // "blue", "silver", "gold", "platinum"
      loyalty_points_band: getPointsBand(user.points),  // "0-10k", "10k-50k", etc.
      member_since_year: new Date(user.memberSince).getFullYear(),
      
      // Booking behavior
      bookings_ytd: user.bookingsYTD,
      trips_completed: user.tripsCompleted,
      preferred_cabin: user.preferredCabin,  // "economy", "business", "first"
      preferred_seat: user.seatPreference,   // "window", "aisle"
      
      // Account features
      has_saved_travelers: user.savedTravelers > 0,
      has_saved_payment: user.hasSavedPayment,
      has_tsa_precheck: user.hasTsaPrecheck,  // Boolean only, not the number
      
      // Travel patterns
      home_airport: user.homeAirport,  // "SFO", "JFK"
      most_visited_destination: user.topDestination,
      
      // Marketing
      email_subscribed: user.emailOptIn,
      fare_alerts_enabled: user.fareAlerts
    }
  });
}
```

---

## Page-Specific Implementations

### Flight/Hotel Search

```html
<!-- Search Page - Core conversion entry point -->
<div class="search-page">
  <!-- Search form - visible (core analytics) -->
  <form class="search-form fs-unmask"
        data-fs-element="Search Form"
        data-fs-properties-schema='{"trip_type":"string","origin":"string","destination":"string","cabin_class":"string"}'>
    
    <!-- Trip type -->
    <div class="trip-type">
      <label><input type="radio" name="trip" value="roundtrip" checked /> Round Trip</label>
      <label><input type="radio" name="trip" value="oneway" /> One Way</label>
      <label><input type="radio" name="trip" value="multi" /> Multi-City</label>
    </div>
    
    <!-- Origin/Destination -->
    <div class="route-inputs">
      <div class="airport-input">
        <label>From</label>
        <input type="text" name="origin" placeholder="City or Airport" />
        <!-- Autocomplete dropdown visible -->
        <div class="autocomplete-dropdown">
          <div class="suggestion">San Francisco (SFO)</div>
          <div class="suggestion">San Jose (SJC)</div>
        </div>
      </div>
      
      <button class="swap-airports" type="button">⇄</button>
      
      <div class="airport-input">
        <label>To</label>
        <input type="text" name="destination" placeholder="City or Airport" />
      </div>
    </div>
    
    <!-- Dates -->
    <div class="date-inputs">
      <div class="date-input">
        <label>Depart</label>
        <input type="date" name="depart_date" />
      </div>
      <div class="date-input">
        <label>Return</label>
        <input type="date" name="return_date" />
      </div>
    </div>
    
    <!-- Passengers -->
    <div class="passenger-selector">
      <label>Travelers</label>
      <button type="button" class="passenger-toggle">2 Adults, 1 Child</button>
      <div class="passenger-dropdown">
        <div class="passenger-row">
          <span>Adults (18+)</span>
          <button>-</button>
          <span class="count">2</span>
          <button>+</button>
        </div>
        <div class="passenger-row">
          <span>Children (2-17)</span>
          <button>-</button>
          <span class="count">1</span>
          <button>+</button>
        </div>
        <div class="passenger-row">
          <span>Infants (under 2)</span>
          <button>-</button>
          <span class="count">0</span>
          <button>+</button>
        </div>
      </div>
    </div>
    
    <!-- Cabin class -->
    <div class="cabin-selector">
      <label>Cabin</label>
      <select name="cabin">
        <option value="economy">Economy</option>
        <option value="premium_economy">Premium Economy</option>
        <option value="business">Business</option>
        <option value="first">First Class</option>
      </select>
    </div>
    
    <!-- Search button -->
    <button type="submit" class="search-btn">Search Flights</button>
  </form>
  
  <!-- Recent searches - visible (your data about their searches) -->
  <div class="recent-searches fs-unmask">
    <h3>Recent Searches</h3>
    <div class="search-history">
      <button>SFO → JFK, Dec 20-27</button>
      <button>LAX → LHR, Jan 5-12</button>
    </div>
  </div>
  
  <!-- Deals/promotions - visible -->
  <div class="promotions fs-unmask">
    <h3>Featured Deals</h3>
    <div class="deal-card">
      <span class="route">SFO → Tokyo</span>
      <span class="price">From $599</span>
    </div>
  </div>
</div>
```

```javascript
// Search tracking
function onSearch(searchParams) {
  FS('trackEvent', {
    name: 'flight_search',
    properties: {
      // Route
      origin: searchParams.origin,
      destination: searchParams.destination,
      origin_country: getCountry(searchParams.origin),
      destination_country: getCountry(searchParams.destination),
      
      // Trip details
      trip_type: searchParams.tripType,
      depart_date: searchParams.departDate,
      return_date: searchParams.returnDate,
      days_until_departure: getDaysUntil(searchParams.departDate),
      trip_duration_days: getTripDuration(searchParams),
      
      // Passengers
      adults: searchParams.adults,
      children: searchParams.children,
      infants: searchParams.infants,
      total_travelers: searchParams.totalTravelers,
      
      // Preferences
      cabin_class: searchParams.cabin,
      flexible_dates: searchParams.flexibleDates,
      nonstop_only: searchParams.nonstopOnly,
      
      // Context
      is_repeat_search: isRepeatSearch(searchParams),
      search_source: 'homepage'  // or "results_modify", "deal_click"
    }
  });
}
```

### Search Results

```html
<!-- Search Results Page -->
<div class="search-results">
  <!-- Search summary - visible -->
  <div class="search-summary fs-unmask">
    <h1>SFO → JFK</h1>
    <p>Dec 20 - Dec 27 · 2 Adults, 1 Child · Economy</p>
    <button class="modify-search">Modify Search</button>
  </div>
  
  <!-- Filters - visible (important for UX) -->
  <aside class="filters fs-unmask">
    <h2>Filter Results</h2>
    
    <div class="filter-group">
      <h3>Stops</h3>
      <label><input type="checkbox" name="stops" value="0" /> Nonstop ($599+)</label>
      <label><input type="checkbox" name="stops" value="1" /> 1 Stop ($449+)</label>
      <label><input type="checkbox" name="stops" value="2" /> 2+ Stops ($399+)</label>
    </div>
    
    <div class="filter-group">
      <h3>Airlines</h3>
      <label><input type="checkbox" name="airline" value="UA" /> United</label>
      <label><input type="checkbox" name="airline" value="AA" /> American</label>
      <label><input type="checkbox" name="airline" value="DL" /> Delta</label>
    </div>
    
    <div class="filter-group">
      <h3>Departure Time</h3>
      <label><input type="checkbox" /> Morning (6am-12pm)</label>
      <label><input type="checkbox" /> Afternoon (12pm-6pm)</label>
      <label><input type="checkbox" /> Evening (6pm-12am)</label>
    </div>
    
    <div class="filter-group">
      <h3>Price Range</h3>
      <input type="range" min="0" max="2000" />
      <span>$0 - $2,000</span>
    </div>
  </aside>
  
  <!-- Sort options - visible -->
  <div class="sort-options fs-unmask">
    <span>Sort by:</span>
    <button class="active">Best</button>
    <button>Price</button>
    <button>Duration</button>
    <button>Departure</button>
  </div>
  
  <!-- Results count - visible -->
  <p class="results-count fs-unmask">Showing 156 flights</p>
  
  <!-- Flight results - visible (public pricing) -->
  <div class="flight-results fs-unmask">
    <div class="flight-card"
         data-fs-element="Flight Card"
         data-fs-properties-schema='{"flight_id":"string","airline":"string","price":"real","stops":"int","duration_minutes":"int"}'>
      <div class="flight-info">
        <div class="airline">
          <img src="ua-logo.svg" alt="United" />
          <span>United</span>
        </div>
        
        <div class="times">
          <span class="depart">7:00 AM</span>
          <span class="arrow">→</span>
          <span class="arrive">3:30 PM</span>
        </div>
        
        <div class="route">
          <span>SFO</span>
          <span class="duration">5h 30m</span>
          <span>JFK</span>
        </div>
        
        <div class="stops">
          <span class="nonstop">Nonstop</span>
        </div>
      </div>
      
      <div class="fare-options">
        <button class="fare" data-fare="basic">
          <span class="fare-name">Basic Economy</span>
          <span class="fare-price">$399</span>
        </button>
        <button class="fare" data-fare="economy">
          <span class="fare-name">Economy</span>
          <span class="fare-price">$449</span>
        </button>
        <button class="fare" data-fare="business">
          <span class="fare-name">Business</span>
          <span class="fare-price">$1,299</span>
        </button>
      </div>
    </div>
    
    <!-- More flights... -->
  </div>
  
  <!-- Pagination - visible -->
  <div class="pagination fs-unmask">
    <button>Load More Results</button>
  </div>
</div>
```

```javascript
// Search results tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'flight_results',
    
    // Search parameters
    origin: searchParams.origin,
    destination: searchParams.destination,
    trip_type: searchParams.tripType,
    cabin_class: searchParams.cabin,
    total_travelers: searchParams.totalTravelers,
    
    // Results
    total_results: results.length,
    has_nonstop: results.some(r => r.stops === 0),
    lowest_price: Math.min(...results.map(r => r.price)),
    highest_price: Math.max(...results.map(r => r.price)),
    airlines_available: [...new Set(results.map(r => r.airline))].length
  }
});

// Filter usage tracking
function onFilterApply(filters) {
  FS('trackEvent', {
    name: 'search_filter_applied',
    properties: {
      filter_type: filters.type,  // "stops", "airline", "time", "price"
      filter_values: filters.values,
      results_after_filter: filteredResults.length,
      results_change: filteredResults.length - previousResults.length
    }
  });
}

// Flight selection
function onFlightSelect(flight, fare) {
  FS('trackEvent', {
    name: 'flight_selected',
    properties: {
      flight_id: flight.id,
      airline: flight.airline,
      origin: flight.origin,
      destination: flight.destination,
      departure_time: flight.departureTime,
      duration_minutes: flight.duration,
      stops: flight.stops,
      fare_class: fare.class,
      fare_price: fare.price,
      position_in_results: flight.resultPosition,
      is_cheapest: flight.isCheapest,
      is_fastest: flight.isFastest
    }
  });
}
```

### Passenger Information

```html
<!-- Passenger Details - Mix of visible and masked/excluded -->
<div class="passenger-details">
  <h1 class="fs-unmask">Traveler Information</h1>
  
  <!-- Trip summary - visible -->
  <aside class="trip-summary fs-unmask">
    <h2>Your Trip</h2>
    <div class="flight-summary">
      <p>SFO → JFK</p>
      <p>Dec 20, 2024</p>
      <p>United 123 · Economy</p>
    </div>
    <div class="price-summary">
      <p>Base Fare: $449 x 3</p>
      <p>Taxes & Fees: $156</p>
      <p class="total">Total: $1,503</p>
    </div>
  </aside>
  
  <!-- Passenger forms -->
  <div class="passengers">
    <div class="passenger-form">
      <h2 class="fs-unmask">Adult 1 (Primary Contact)</h2>
      
      <!-- Name fields - MASK -->
      <div class="name-fields fs-mask">
        <div class="field">
          <label>First Name (as on ID)</label>
          <input type="text" name="firstName" />
        </div>
        <div class="field">
          <label>Middle Name</label>
          <input type="text" name="middleName" />
        </div>
        <div class="field">
          <label>Last Name</label>
          <input type="text" name="lastName" />
        </div>
      </div>
      
      <!-- Date of birth - EXCLUDE (when combined with name = PII risk) -->
      <div class="dob-field fs-exclude">
        <label>Date of Birth</label>
        <input type="date" name="dob" />
      </div>
      
      <!-- Gender - visible (for booking, common data) -->
      <div class="gender-field fs-unmask">
        <label>Gender (as on ID)</label>
        <select name="gender">
          <option>Male</option>
          <option>Female</option>
          <option>X / Unspecified</option>
        </select>
      </div>
      
      <!-- Contact info - MASK -->
      <div class="contact-fields fs-mask">
        <div class="field">
          <label>Email Address</label>
          <input type="email" name="email" />
        </div>
        <div class="field">
          <label>Phone Number</label>
          <input type="tel" name="phone" />
        </div>
      </div>
      
      <!-- Government IDs - EXCLUDE completely -->
      <div class="id-fields fs-exclude">
        <h3>Travel Documents (International Flights)</h3>
        <div class="field">
          <label>Passport Number</label>
          <input type="text" name="passportNumber" />
        </div>
        <div class="field">
          <label>Passport Expiry</label>
          <input type="date" name="passportExpiry" />
        </div>
        <div class="field">
          <label>Country of Issue</label>
          <select name="passportCountry"><!-- Countries --></select>
        </div>
      </div>
      
      <!-- TSA info - EXCLUDE -->
      <div class="tsa-fields fs-exclude">
        <h3>TSA Information (Optional)</h3>
        <div class="field">
          <label>Known Traveler Number (TSA PreCheck/Global Entry)</label>
          <input type="text" name="knownTraveler" />
        </div>
        <div class="field">
          <label>Redress Number</label>
          <input type="text" name="redress" />
        </div>
      </div>
      
      <!-- Loyalty number - MASK (could be used for account access) -->
      <div class="loyalty-field fs-mask">
        <label>Frequent Flyer Number (Optional)</label>
        <input type="text" name="loyaltyNumber" />
      </div>
    </div>
    
    <!-- Additional passengers... -->
  </div>
  
  <!-- Continue button - visible -->
  <div class="form-actions fs-unmask">
    <button type="button">Back</button>
    <button type="submit">Continue to Seats</button>
  </div>
</div>
```

```javascript
// Passenger info tracking - generic only
FS('trackEvent', {
  name: 'passenger_info_completed',
  properties: {
    total_travelers: travelers.length,
    adults: travelers.filter(t => t.type === 'adult').length,
    children: travelers.filter(t => t.type === 'child').length,
    infants: travelers.filter(t => t.type === 'infant').length,
    has_loyalty_numbers: travelers.some(t => t.loyaltyNumber),
    has_tsa_info: travelers.some(t => t.knownTraveler),
    is_international: trip.isInternational,
    time_to_complete_seconds: getFormDuration()
    // Never: names, DOB, passport numbers
  }
});
```

### Seat Selection

```html
<!-- Seat Selection - Good analytics opportunity -->
<div class="seat-selection">
  <h1 class="fs-unmask">Choose Your Seats</h1>
  
  <!-- Flight segment tabs - visible -->
  <div class="segment-tabs fs-unmask">
    <button class="active">SFO → JFK (Dec 20)</button>
    <button>JFK → SFO (Dec 27)</button>
  </div>
  
  <!-- Seat map - visible (public cabin layout) -->
  <div class="seat-map fs-unmask"
       data-fs-element="Seat Map"
       data-fs-properties-schema='{"aircraft_type":"string","cabin_class":"string"}'>
    <div class="cabin-legend">
      <span class="legend-item available">Available</span>
      <span class="legend-item selected">Selected</span>
      <span class="legend-item premium">Extra Legroom ($45)</span>
      <span class="legend-item occupied">Occupied</span>
    </div>
    
    <div class="aircraft-cabin">
      <!-- Seat rows -->
      <div class="seat-row">
        <span class="row-number">1</span>
        <button class="seat premium" data-seat="1A">A</button>
        <button class="seat premium" data-seat="1B">B</button>
        <span class="aisle"></span>
        <button class="seat premium" data-seat="1C">C</button>
        <button class="seat premium" data-seat="1D">D</button>
      </div>
      <!-- More rows... -->
    </div>
  </div>
  
  <!-- Seat selection summary - visible -->
  <div class="seat-summary fs-unmask">
    <h2>Selected Seats</h2>
    <div class="selected-seats">
      <div class="seat-assignment">
        <span class="traveler">Adult 1</span>
        <span class="seat">12A (Window)</span>
        <span class="price">Included</span>
      </div>
      <div class="seat-assignment">
        <span class="traveler">Adult 2</span>
        <span class="seat">12B (Middle)</span>
        <span class="price">Included</span>
      </div>
    </div>
  </div>
  
  <!-- Upgrade offer - visible -->
  <div class="upgrade-offer fs-unmask">
    <h3>Upgrade to Extra Legroom</h3>
    <p>More space for just $45 per seat</p>
    <button>View Available</button>
  </div>
  
  <!-- Actions - visible -->
  <div class="form-actions fs-unmask">
    <button>Skip Seat Selection</button>
    <button type="submit">Continue to Bags</button>
  </div>
</div>
```

```javascript
// Seat selection tracking
function onSeatSelected(seat, traveler) {
  FS('trackEvent', {
    name: 'seat_selected',
    properties: {
      seat_type: seat.type,  // "standard", "extra_legroom", "preferred"
      seat_position: seat.position,  // "window", "middle", "aisle"
      seat_row_zone: getSeatZone(seat.row),  // "front", "middle", "back", "exit_row"
      seat_price: seat.price,
      is_paid_seat: seat.price > 0,
      traveler_number: traveler.index,
      aircraft_type: flight.aircraft
    }
  });
}

// Seat selection summary
FS('trackEvent', {
  name: 'seat_selection_completed',
  properties: {
    total_travelers: travelers.length,
    seats_selected: selectedSeats.length,
    seats_skipped: travelers.length - selectedSeats.length,
    paid_seats: selectedSeats.filter(s => s.price > 0).length,
    seat_revenue: selectedSeats.reduce((sum, s) => sum + s.price, 0),
    upgrade_offered: upgradeWasOffered,
    upgrade_accepted: upgradeAccepted
  }
});
```

### Bags and Ancillaries

```html
<!-- Bags and Extras - Major revenue tracking -->
<div class="bags-extras">
  <h1 class="fs-unmask">Add Bags & Extras</h1>
  
  <!-- Bag selection - visible (pricing data) -->
  <section class="bags-section fs-unmask"
           data-fs-element="Bag Selection">
    <h2>Checked Bags</h2>
    
    <div class="traveler-bags">
      <h3>Adult 1</h3>
      
      <div class="bag-options">
        <div class="bag-option">
          <span class="bag-type">Carry-on</span>
          <span class="included">✓ Included</span>
        </div>
        
        <div class="bag-option">
          <span class="bag-type">1st Checked Bag</span>
          <div class="bag-selector">
            <button class="active">No Bag ($0)</button>
            <button>Add Bag ($35)</button>
          </div>
        </div>
        
        <div class="bag-option">
          <span class="bag-type">2nd Checked Bag</span>
          <div class="bag-selector">
            <button class="active">No Bag ($0)</button>
            <button>Add Bag ($45)</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- More travelers... -->
  </section>
  
  <!-- Travel extras - visible -->
  <section class="extras-section fs-unmask">
    <h2>Travel Extras</h2>
    
    <div class="extra-option">
      <div class="extra-info">
        <h3>Travel Insurance</h3>
        <p>Trip cancellation, medical coverage, baggage protection</p>
        <span class="price">$49 per traveler</span>
      </div>
      <button>Add Insurance</button>
    </div>
    
    <div class="extra-option">
      <div class="extra-info">
        <h3>Priority Boarding</h3>
        <p>Board early and secure overhead bin space</p>
        <span class="price">$15 per traveler</span>
      </div>
      <button>Add Priority</button>
    </div>
    
    <div class="extra-option">
      <div class="extra-info">
        <h3>WiFi Bundle</h3>
        <p>Stay connected on all your flights</p>
        <span class="price">$25</span>
      </div>
      <button>Add WiFi</button>
    </div>
  </section>
  
  <!-- Summary - visible -->
  <div class="extras-summary fs-unmask">
    <h2>Extras Added</h2>
    <div class="summary-items">
      <div class="item">
        <span>Checked Bags (2)</span>
        <span>$70</span>
      </div>
      <div class="item">
        <span>Travel Insurance (3)</span>
        <span>$147</span>
      </div>
    </div>
    <p class="total">Extras Total: $217</p>
  </div>
  
  <!-- Actions - visible -->
  <div class="form-actions fs-unmask">
    <button>Skip Extras</button>
    <button type="submit">Continue to Payment</button>
  </div>
</div>
```

```javascript
// Ancillary tracking - very valuable
function onBagAdded(bag, traveler) {
  FS('trackEvent', {
    name: 'ancillary_added',
    properties: {
      ancillary_type: 'checked_bag',
      bag_number: bag.number,  // 1st, 2nd
      price: bag.price,
      traveler_number: traveler.index,
      flight_segment: bag.segment
    }
  });
}

function onExtraAdded(extra) {
  FS('trackEvent', {
    name: 'ancillary_added',
    properties: {
      ancillary_type: extra.type,  // "insurance", "priority_boarding", "wifi"
      price: extra.price,
      quantity: extra.quantity
    }
  });
}

// Summary tracking
FS('trackEvent', {
  name: 'ancillary_selection_completed',
  properties: {
    total_bags_added: bagsAdded,
    bag_revenue: bagTotal,
    
    has_insurance: hasInsurance,
    insurance_revenue: insuranceTotal,
    
    has_priority: hasPriority,
    has_wifi: hasWifi,
    
    total_ancillary_revenue: totalAncillaryRevenue,
    ancillary_per_traveler: totalAncillaryRevenue / travelers.length,
    
    extras_skipped: skippedAll
  }
});
```

### Payment

```html
<!-- Payment Page - PCI considerations -->
<div class="payment-page">
  <h1 class="fs-unmask">Complete Your Booking</h1>
  
  <!-- Booking summary - visible -->
  <aside class="booking-summary fs-unmask">
    <h2>Trip Summary</h2>
    
    <div class="flight-details">
      <div class="segment">
        <p class="date">Dec 20, 2024</p>
        <p class="route">SFO → JFK</p>
        <p class="flight">United 123 · Economy</p>
      </div>
      <div class="segment">
        <p class="date">Dec 27, 2024</p>
        <p class="route">JFK → SFO</p>
        <p class="flight">United 456 · Economy</p>
      </div>
    </div>
    
    <div class="price-breakdown">
      <div class="line-item">
        <span>Flights (3 travelers)</span>
        <span>$1,347</span>
      </div>
      <div class="line-item">
        <span>Seats</span>
        <span>$90</span>
      </div>
      <div class="line-item">
        <span>Bags</span>
        <span>$70</span>
      </div>
      <div class="line-item">
        <span>Travel Insurance</span>
        <span>$147</span>
      </div>
      <div class="line-item">
        <span>Taxes & Fees</span>
        <span>$156</span>
      </div>
      <div class="line-item total">
        <span>Total</span>
        <span>$1,810</span>
      </div>
    </div>
    
    <!-- Promo code - can track usage -->
    <div class="promo-section fs-unmask">
      <input type="text" placeholder="Promo Code" />
      <button>Apply</button>
    </div>
  </aside>
  
  <!-- Payment form -->
  <div class="payment-form">
    <!-- Payment method selection - visible -->
    <div class="payment-methods fs-unmask">
      <h2>Payment Method</h2>
      <label>
        <input type="radio" name="payment" value="card" checked />
        Credit/Debit Card
      </label>
      <label>
        <input type="radio" name="payment" value="paypal" />
        PayPal
      </label>
      <label>
        <input type="radio" name="payment" value="points" />
        Use Miles (45,000 available)
      </label>
    </div>
    
    <!-- Card form - EXCLUDE -->
    <div class="card-form fs-exclude">
      <div class="field">
        <label>Card Number</label>
        <input type="text" name="cardNumber" autocomplete="cc-number" />
      </div>
      <div class="field">
        <label>Expiration</label>
        <input type="text" name="expiry" autocomplete="cc-exp" />
      </div>
      <div class="field">
        <label>CVV</label>
        <input type="text" name="cvv" autocomplete="cc-csc" />
      </div>
      <div class="field">
        <label>Name on Card</label>
        <input type="text" name="cardName" />
      </div>
    </div>
    
    <!-- Billing address - MASK -->
    <div class="billing-address fs-mask">
      <h2 class="fs-unmask">Billing Address</h2>
      <input type="text" name="address1" placeholder="Address" />
      <input type="text" name="city" placeholder="City" />
      <select name="state"><!-- States --></select>
      <input type="text" name="zip" placeholder="ZIP Code" />
    </div>
    
    <!-- Terms - visible -->
    <div class="terms fs-unmask">
      <label>
        <input type="checkbox" name="terms" required />
        I agree to the fare rules, terms and conditions
      </label>
    </div>
    
    <!-- Submit - visible for funnel -->
    <button type="submit" class="book-btn fs-unmask">
      Complete Booking - $1,810
    </button>
  </div>
</div>
```

```javascript
// Payment tracking
function onPaymentMethodSelected(method) {
  FS('trackEvent', {
    name: 'payment_method_selected',
    properties: {
      method: method,  // "card", "paypal", "points", "points_plus_card"
      points_used: method === 'points' ? pointsUsed : 0,
      remaining_balance: method === 'points' ? remainingBalance : totalAmount
    }
  });
}

function onBookingComplete(booking) {
  FS('trackEvent', {
    name: 'booking_completed',
    properties: {
      booking_id: booking.confirmationNumber,
      
      // Trip details
      origin: booking.origin,
      destination: booking.destination,
      trip_type: booking.tripType,
      
      // Pricing
      base_fare: booking.baseFare,
      taxes_fees: booking.taxesFees,
      ancillary_revenue: booking.ancillaryTotal,
      total_price: booking.total,
      
      // Travelers
      total_travelers: booking.travelers,
      
      // Payment
      payment_method: booking.paymentMethod,
      points_redeemed: booking.pointsUsed,
      
      // Funnel metrics
      time_to_book_minutes: getBookingDuration(),
      sessions_to_book: getSessionCount(),
      
      // Cabin
      cabin_class: booking.cabin,
      
      // Upsells accepted
      has_paid_seats: booking.hasPaidSeats,
      has_bags: booking.hasBags,
      has_insurance: booking.hasInsurance
    }
  });
}
```

---

## Hotel-Specific Patterns

```javascript
// Hotel search tracking
FS('trackEvent', {
  name: 'hotel_search',
  properties: {
    destination: search.destination,
    check_in: search.checkIn,
    check_out: search.checkOut,
    nights: search.nights,
    rooms: search.rooms,
    guests: search.guests,
    star_rating_filter: search.starRating
  }
});

// Hotel selection
FS('trackEvent', {
  name: 'hotel_selected',
  properties: {
    hotel_id: hotel.id,
    hotel_name: hotel.name,
    star_rating: hotel.stars,
    price_per_night: hotel.price,
    total_price: hotel.totalPrice,
    room_type: room.type,
    is_refundable: room.isRefundable,
    includes_breakfast: room.hasBreakfast,
    position_in_results: hotel.resultPosition
  }
});
```

---

## Loyalty Program Tracking

```javascript
// Loyalty-specific tracking
FS('setProperties', {
  type: 'user',
  properties: {
    loyalty_tier: user.tier,
    points_balance_band: getPointsBand(user.points),
    status_miles_ytd_band: getMilesBand(user.statusMiles),
    miles_to_next_tier: user.milesToNextTier,
    tier_expiry_days: user.tierExpiryDays
  }
});

// Points earning
FS('trackEvent', {
  name: 'points_earned',
  properties: {
    earning_type: 'flight',  // "flight", "card_spend", "partner", "promo"
    points_earned: points,
    booking_id: booking.id
  }
});

// Points redemption
FS('trackEvent', {
  name: 'points_redeemed',
  properties: {
    redemption_type: 'flight',  // "flight", "upgrade", "merchandise"
    points_redeemed: points,
    cash_equivalent: cashValue
  }
});
```

---

## KEY TAKEAWAYS FOR AGENT

When helping travel clients with Fullstory:

1. **Search and pricing data is valuable**: Dates, destinations, prices can all be captured
2. **PCI compliance for payments**: Always exclude card details
3. **Government IDs are sensitive**: Passport numbers, TSA numbers must be excluded
4. **Ancillary tracking is crucial**: Bags, seats, insurance are major revenue
5. **Traveler names should be masked**: Not excluded, but masked
6. **Multi-session journeys**: Users often research across multiple sessions

### Questions to Ask Travel Clients

1. "Are you tracking the full search-to-book funnel?"
2. "How are you tracking ancillary upsells?"
3. "Is passport/government ID entry properly excluded?"
4. "How do you handle loyalty program member data?"
5. "Are you tracking abandonment at each step?"

### Key Metrics to Track

- Search-to-results conversion
- Results-to-selection conversion
- Passenger info completion rate
- Seat/bag/insurance attachment rates
- Payment success rate
- Booking value (base + ancillary)

---

## REFERENCE LINKS

- **PCI Compliance**: https://www.pcisecuritystandards.org/
- **Fullstory Privacy Controls**: ../core/fullstory-privacy-controls/SKILL.md
- **Analytics Events**: ../core/fullstory-analytics-events/SKILL.md
- **Element Properties**: ../core/fullstory-element-properties/SKILL.md

---

*This skill document is specific to travel and hospitality implementations. Adjust based on your specific business requirements.*

