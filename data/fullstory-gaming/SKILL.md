---
name: fullstory-gaming
version: v2
description: Industry-specific guide for implementing Fullstory in gaming applications. Covers regulatory requirements (responsible gaming, KYC/AML), privacy controls for sensitive gaming data, deposit/withdrawal flows, player protection features, and self-exclusion compliance. Includes detailed examples for sportsbooks, casinos, poker, and lottery applications.
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-user-consent
  - fullstory-identify-users
  - fullstory-analytics-events
---

# Fullstory for Gaming

> ⚠️ **LEGAL DISCLAIMER**: This guidance is for educational purposes only and does not constitute legal, compliance, or regulatory advice. Gaming regulations vary significantly by jurisdiction and are subject to strict licensing requirements. Always consult with your legal, compliance, and responsible gaming teams before implementing any data capture solution. Your organization is responsible for ensuring compliance with all applicable gaming regulations and licensing requirements.

## Industry Overview

Gaming platforms have unique requirements due to:

- **Heavy regulation**: Jurisdiction-specific licensing requirements
- **Responsible gaming**: Mandatory player protection features
- **KYC/AML compliance**: Identity verification requirements
- **Financial sensitivity**: Deposits, withdrawals, bet amounts
- **Addiction concerns**: Behavior patterns may indicate problem gaming
- **Age verification**: Must ensure 18+/21+ compliance

### Key Goals for Gaming Implementations

1. **Optimize conversion funnels** from registration to first bet/deposit
2. **Improve user experience** across gaming flows
3. **Monitor responsible gaming features** (limits, timeouts, self-exclusion)
4. **Ensure compliance** with regulatory requirements
5. **Reduce friction** in deposit/withdrawal processes
6. **Understand player engagement** without enabling surveillance

---

## Regulatory Framework

### Key Regulations by Jurisdiction

| Jurisdiction | Key Regulations | Fullstory Implications |
|--------------|-----------------|------------------------|
| **UK** | UKGC License Conditions | Responsible gaming tracking, self-exclusion |
| **Malta** | MGA Requirements | Player protection, data localization |
| **US (NJ, PA, etc.)** | State Gaming Commissions | KYC data handling, geolocation |
| **EU** | GDPR + Local Gaming Laws | Consent, data minimization |
| **Australia** | Interactive Gaming Act | Responsible gaming features |

### Fraud Detection and Prevention

Fullstory enables real-time detection of fraudulent behavior in gaming applications. In 2024 alone, gaming sites lost more than $1B to fraud, with rates rising 64% since 2022 ([Source](https://www.fullstory.com/blog/prevent-online-gambling-fraud/)).

**Common Fraud Types to Detect:**

| Fraud Type | Behavioral Signals | Fullstory Detection |
|------------|-------------------|---------------------|
| **Bonus Abuse** | Multiple accounts claiming welcome offers; VPN/TOR usage | Track signup patterns, browser fingerprints, IP inconsistencies |
| **Multi-Accounting** | Same user operating multiple accounts to bypass limits | Session replay, behavioral fingerprinting |
| **Gnoming** | Coordinated accounts manipulating outcomes | Cross-account behavior correlation |
| **Bot-like Behavior** | Automated scripts placing bets | Interaction timing, mouse movements, click patterns |
| **Chargeback Fraud** | Deposit → wager → dispute cycle | Payment flow tracking, dispute pattern analysis |
| **Money Laundering** | Low-margin bets, rapid transactions across accounts | Transaction velocity, wagering pattern analysis |
| **KYC/AML Evasion** | False documents, account cycling | Verification flow tracking, document upload patterns |

```javascript
// Track fraud risk indicators
FS('trackEvent', {
  name: 'fraud_signal_detected',
  properties: {
    signal_type: 'multi_account_indicator',
    signal_source: 'behavioral',
    risk_level: 'high',
    session_id: sessionId,
    indicators: [
      'rapid_account_creation',
      'bonus_claim_pattern',
      'vpn_detected'
    ],
    // Fullstory captures mouse movements, timing, interaction patterns automatically
  }
});

// Track KYC verification flow for fraud detection
FS('trackEvent', {
  name: 'kyc_verification_step',
  properties: {
    step: 'document_upload',
    document_type: 'id_card',
    attempt_number: 2,
    time_on_step_seconds: 45,
    previous_failures: 1,
    // Track patterns: multiple failed attempts = potential fraud signal
  }
});
```

**Building Fraud Detection Dashboards:**

```javascript
// Track suspicious deposit patterns
FS('trackEvent', {
  name: 'deposit_pattern_analysis',
  properties: {
    deposit_amount: 500.00,
    deposits_last_hour: 3,
    deposits_last_24h: 8,
    unique_payment_methods_24h: 4,
    average_time_between_deposits_minutes: 12,
    matches_bonus_abuse_pattern: true,
  }
});

// Track unusual session behavior
FS('trackEvent', {
  name: 'session_anomaly',
  properties: {
    anomaly_type: 'rapid_navigation',
    pages_per_minute: 45,
    click_pattern: 'automated',
    mouse_movement_score: 0.2,  // Low score = bot-like
    time_to_first_bet_seconds: 3,
  }
});
```

> **Reference**: [Online Gaming Fraud Prevention](https://www.fullstory.com/blog/prevent-online-gambling-fraud/)

---

### High-Value Player Engagement

Fullstory enables real-time identification and engagement of high-value players:

```javascript
// Track high-value player moments
FS('trackEvent', {
  name: 'high_value_moment',
  properties: {
    moment_type: 'big_win',
    player_value_tier: 'vip',
    session_duration_minutes: 45,
    engagement_score: 'high',
    eligible_for_reward: true,
    reward_type: 'loyalty_bonus',
  }
});

// Set high-value player properties
FS('setProperties', {
  type: 'user',
  properties: {
    player_value_tier: 'platinum',
    lifetime_deposits_band: '$10k-$50k',
    preferred_game_type: 'live_casino',
    churn_risk_score: 'low',
    last_vip_contact_days: 7,
    eligible_promotions: ['reload_bonus', 'cashback'],
  }
});
```

> **Key Stat**: Casumo achieved 87% reduction in time to resolution using Fullstory for player experience issues ([Source](https://www.fullstory.com/industries/gaming/)).

---

### AI/ML Fairness Considerations

Many gaming platforms use AI/ML for odds calculation, player risk assessment, and promotional targeting. Fullstory can help audit these systems for fairness:

| AI/ML Application | What to Track | Privacy Note |
|-------------------|---------------|--------------|
| **Dynamic odds** | Odds displayed (not wager amounts) | Track changes, not player-specific |
| **Bonus allocation** | Bonus offered (type, not amount) | Audit for fair distribution |
| **Risk scoring** | Features shown/hidden | Never capture the score itself |
| **Promotional targeting** | Promo impressions, clicks | Audit for bias patterns |
| **Responsible gaming intervention** | Intervention shown | Never track individual triggers |

```javascript
// Track AI/ML feature distribution for fairness auditing
FS('trackEvent', {
  name: 'ai_feature_impression',
  properties: {
    feature_type: 'dynamic_promo',
    variant_shown: 'B',
    player_segment: 'standard',   // Generic segment only
    // NEVER: AI risk scores, predicted behaviors, or individual targeting reasons
  }
});
```

> **Important**: Never capture AI/ML decision rationale that could reveal player profiling. Track what was shown, not why.

### Data Handling by Purpose

| Data Type | General UX Analytics | Compliance Monitoring | Notes |
|-----------|---------------------|----------------------|-------|
| Identity documents | ❌ Never | ❌ Never | Never capture images |
| SSN/Tax ID | ❌ fs-exclude | ❌ fs-exclude | Government ID |
| Bank account details | ❌ fs-exclude | ❌ fs-exclude | Financial security |
| Card details | ❌ fs-exclude | ❌ fs-exclude | PCI compliance |
| **Wager amounts** | ⚠️ Use bands | ✅ Capture for RG | Needed for responsible gaming |
| **Win/loss amounts** | ⚠️ Use bands | ✅ Capture for RG | Pattern detection |
| **Deposit amounts** | ⚠️ Use bands | ✅ Capture for RG | Velocity monitoring |
| Account balance | ⚠️ Use bands | ⚠️ Consider | May aid pattern detection |
| Gaming history | ⚠️ Consider | ✅ Track | Session patterns |
| Self-exclusion status | ❌ Never expose | ⚠️ Internal only | Privacy sensitive |
| Responsible gaming limits | ⚠️ Track changes | ✅ Track | Compliance requirement |
| Intervention triggers | N/A | ✅ Track | Required for audit |

> **Key Insight**: For **responsible gaming compliance**, capturing actual amounts is often **required** to identify at-risk players. Use bands for general UX analytics, actual values for compliance monitoring.

### Responsible Gaming Monitoring with Fullstory

**Regulatory requirements** (UKGC, MGA, US state commissions) mandate that operators monitor player behavior to identify and protect at-risk players. **Fullstory can serve as a powerful tool for responsible gaming compliance**, combining behavioral analytics with session replay for comprehensive player protection.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FULLSTORY FOR RESPONSIBLE GAMING COMPLIANCE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  What Fullstory enables:                                                     │
│  ├── Behavioral pattern analysis across sessions                            │
│  ├── Session replay for compliance review and audit                         │
│  ├── Real-time event tracking for intervention triggers                     │
│  ├── Segment creation for at-risk player identification                     │
│  ├── Data export for regulatory reporting                                   │
│  └── Cross-device journey tracking                                          │
│                                                                             │
│  Key capabilities:                                                           │
│  • Track wagering patterns to identify escalating behavior                  │
│  • Monitor session duration and frequency                                   │
│  • Capture deposit velocity and amounts                                     │
│  • Track responsible gaming feature engagement                              │
│  • Create alerts based on behavioral thresholds                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Capturing Wagering Data for Compliance:**

```javascript
// Track wager events for responsible gaming monitoring
FS('trackEvent', {
  name: 'wager_placed',
  properties: {
    wager_amount: 50.00,              // Actual amount for compliance monitoring
    wager_amount_band: '$25-$100',    // Band for general analytics
    game_type: 'slots',
    game_id: 'starburst',
    currency: 'GBP',
    session_wager_total: 150.00,      // Running total this session
    session_wager_count: 5,           // Number of wagers this session
    time_since_last_wager_seconds: 45,
  }
});

// Track wins/losses for pattern analysis
FS('trackEvent', {
  name: 'wager_result',
  properties: {
    result: 'loss',                   // 'win' or 'loss'
    amount: 50.00,                    // Amount won or lost
    net_session_position: -75.00,    // Running P&L this session
    consecutive_losses: 3,            // Pattern indicator
    game_type: 'slots',
  }
});

// Track deposit behavior
FS('trackEvent', {
  name: 'deposit_completed',
  properties: {
    deposit_amount: 100.00,
    deposit_method: 'debit_card',
    deposits_today: 2,
    deposits_this_week: 5,
    total_deposited_today: 200.00,
    approaching_limit: true,          // Flag for compliance
    limit_percentage_used: 80,
  }
});
```

**User Properties for Player Risk Monitoring:**

```javascript
// Set player profile properties for segmentation and monitoring
FS('setProperties', {
  type: 'user',
  properties: {
    // Responsible gaming profile
    has_deposit_limit: true,
    has_loss_limit: true,
    has_session_limit: false,
    reality_check_interval_minutes: 60,
    
    // Risk indicators (updated in real-time)
    current_risk_tier: 'elevated',     // 'low', 'moderate', 'elevated', 'high'
    days_since_last_rg_interaction: 14,
    lifetime_deposit_total_band: '$1k-$5k',
    
    // Engagement patterns
    avg_session_duration_minutes: 45,
    sessions_per_week: 8,
    preferred_game_category: 'slots',
  }
});
```

**Session-Level Monitoring:**

```javascript
// Page properties for session context
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Casino - Slots',
    session_start_time: new Date().toISOString(),
    session_wager_count: 0,
    session_deposit_count: 0,
    reality_check_due_at: '2024-01-15T15:30:00Z',
  }
});

// Track reality check interactions
FS('trackEvent', {
  name: 'reality_check_displayed',
  properties: {
    session_duration_minutes: 60,
    session_wagered: 250.00,
    session_net_position: -75.00,
    user_action: 'continue',          // 'continue', 'take_break', 'set_limit', 'quit'
    time_to_respond_seconds: 8,
  }
});

// Track responsible gaming tool usage
FS('trackEvent', {
  name: 'responsible_gaming_action',
  properties: {
    action: 'deposit_limit_set',
    limit_type: 'daily',
    limit_amount: 50.00,
    previous_limit: 100.00,           // Track if reducing limits
    self_initiated: true,             // vs triggered by intervention
  }
});
```

**Creating Compliance Segments in Fullstory:**

| Segment | Criteria | Action |
|---------|----------|--------|
| **High Risk - Chasing Losses** | 5+ consecutive losses AND increased wager amounts | Immediate review |
| **Deposit Velocity Concern** | 3+ deposits in 24hrs | Compliance flag |
| **Extended Session** | Session > 3hrs without break | Trigger reality check review |
| **Approaching Limits** | >80% of any limit used | Proactive outreach |
| **Limit Reduction** | Player reduced their own limits | Positive indicator, monitor |
| **Declined Deposit** | Deposit blocked by limit | Review if multiple attempts |

**Intervention Tracking:**

```javascript
// Track when interventions are triggered and their outcomes
FS('trackEvent', {
  name: 'intervention_triggered',
  properties: {
    intervention_type: 'mandatory_break',
    trigger_reason: 'session_duration_exceeded',
    session_duration_minutes: 180,
    session_wagered: 500.00,
    player_risk_tier: 'elevated',
  }
});

FS('trackEvent', {
  name: 'intervention_outcome',
  properties: {
    intervention_type: 'mandatory_break',
    outcome: 'completed',             // 'completed', 'extended', 'self_excluded'
    break_duration_minutes: 15,
    returned_to_play: true,
    time_until_return_minutes: 45,
  }
});
```

**Best Practices for Compliance Use:**

| Practice | Implementation |
|----------|----------------|
| **Data retention** | Configure Fullstory retention to meet regulatory requirements |
| **Access controls** | Limit access to wagering data to compliance team |
| **Audit trail** | Use Data Export for regulatory reporting |
| **Real-time monitoring** | Set up alerts for high-risk patterns |
| **Session replay** | Use for manual review of flagged sessions |
| **Cross-reference** | Combine with CRM data for complete player view |

> **Important**: When using Fullstory for compliance, ensure your data retention, access controls, and export capabilities meet the specific requirements of your gaming license jurisdictions.


---

## Implementation Architecture

### Privacy Zones for Gaming

```
┌─────────────────────────────────────────────────────────────────┐
│                     GAMING APPLICATION                           │
├─────────────────────────────────────────────────────────────────┤
│  FULLY VISIBLE (fs-unmask)                                       │
│  • Sports events, odds display                                   │
│  • Casino game selection                                         │
│  • Navigation and UI                                            │
│  • Promotional banners                                          │
│  • General error messages                                       │
│  • Feature buttons (not amounts)                                │
├─────────────────────────────────────────────────────────────────┤
│  MASKED (fs-mask)                                                │
│  • Player name                                                  │
│  • Email address                                                │
│  • Phone number                                                 │
│  • Partial address (city/state OK)                              │
│  • Username (if not full name)                                  │
├─────────────────────────────────────────────────────────────────┤
│  EXCLUDED (fs-exclude)                                           │
│  • Account balance                                              │
│  • Bet slips (amounts)                                          │
│  • Transaction history amounts                                  │
│  • Deposit/withdrawal amounts                                   │
│  • Win/loss totals                                              │
│  • ID verification screens                                      │
│  • Payment card details                                         │
│  • SSN/Tax ID                                                   │
│  • Bank account details                                         │
│  • Self-exclusion settings                                      │
│  • Responsible gaming limits                                  │
│  • Problem gaming questionnaires                              │
└─────────────────────────────────────────────────────────────────┘
```

### Game Iframe Semantic Decoration

Most gaming operators embed third-party game provider iframes (e.g., Evolution, NetEnt, Pragmatic Play). Since Fullstory cannot capture content inside cross-origin iframes, you must decorate the **wrapper elements** to track which games players interact with.

```html
<!-- IMPORTANT: Decorate the WRAPPER around the iframe, not the iframe itself -->

<!-- Slot Game Launcher -->
<div 
  class="game-container"
  data-fs-element="GameLauncher"
  data-fs-properties-schema='{
    "data-game-id": {"type": "str", "name": "gameId"},
    "data-game-name": {"type": "str", "name": "gameName"},
    "data-game-provider": {"type": "str", "name": "gameProvider"},
    "data-game-category": {"type": "str", "name": "gameCategory"},
    "data-game-rtp": {"type": "real", "name": "gameRTP"}
  }'
  data-game-id="starburst_xxxtreme"
  data-game-name="Starburst XXXtreme"
  data-game-provider="netent"
  data-game-category="slots"
  data-game-rtp="96.26"
>
  <!-- Game iframe (content not captured, but wrapper interactions are) -->
  <iframe 
    src="https://game-provider.com/launch/starburst_xxxtreme" 
    title="Starburst XXXtreme"
  ></iframe>
  
  <!-- Game controls OUTSIDE iframe (captured) -->
  <div class="game-controls fs-unmask">
    <button data-fs-element="FullscreenButton">Fullscreen</button>
    <button data-fs-element="FavoriteButton">Add to Favorites</button>
    <button data-fs-element="ExitGameButton">Exit Game</button>
  </div>
</div>
```

**Track game launch events:**

```javascript
// Track when a game is launched
function launchGame(game) {
  FS('trackEvent', {
    name: 'game_launched',
    properties: {
      game_id: game.id,
      game_name: game.name,
      game_provider: game.provider,       // "netent", "evolution", "pragmatic"
      game_category: game.category,       // "slots", "table_games", "live_casino"
      game_subcategory: game.subcategory, // "megaways", "jackpot", "classic"
      game_rtp: game.rtp,                 // 96.26
      launch_source: game.source,         // "lobby", "favorites", "search", "recommendation"
      is_demo_mode: game.isDemoMode,
    }
  });
}

// Track game session duration (when game is closed)
function exitGame(game, sessionStart) {
  FS('trackEvent', {
    name: 'game_session_ended',
    properties: {
      game_id: game.id,
      game_name: game.name,
      game_provider: game.provider,
      session_duration_seconds: Math.floor((Date.now() - sessionStart) / 1000),
      exit_reason: game.exitReason,       // "user_exit", "session_timeout", "error"
    }
  });
}
```

**Page properties for game sessions:**

```javascript
// Set page context when game is active
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Game - Slots',
    active_game_id: 'starburst_xxxtreme',
    active_game_name: 'Starburst XXXtreme',
    active_game_provider: 'netent',
    active_game_category: 'slots',
    game_session_start: new Date().toISOString(),
  }
});
```

**Game lobby decoration:**

```html
<!-- Game Lobby with semantic decoration -->
<div 
  class="game-lobby"
  data-fs-element="GameLobby"
>
  <!-- Category filters (captured) -->
  <nav class="category-filters fs-unmask">
    <button 
      data-fs-element="CategoryFilter"
      data-fs-properties-schema='{"data-category": {"type": "str", "name": "filterCategory"}}'
      data-category="slots"
    >Slots</button>
    <button 
      data-fs-element="CategoryFilter"
      data-category="live-casino"
    >Live Casino</button>
    <button 
      data-fs-element="CategoryFilter"
      data-category="table-games"
    >Table Games</button>
  </nav>

  <!-- Game grid -->
  <div class="game-grid">
    <!-- Each game tile is decorated -->
    <article 
      class="game-tile"
      data-fs-element="GameTile"
      data-fs-properties-schema='{
        "data-game-id": {"type": "str", "name": "gameId"},
        "data-game-provider": {"type": "str", "name": "provider"}
      }'
      data-game-id="starburst_xxxtreme"
      data-game-provider="netent"
    >
      <img src="/thumbnails/starburst.jpg" alt="Starburst XXXtreme" />
      <h3 class="fs-unmask">Starburst XXXtreme</h3>
      <span class="provider fs-unmask">NetEnt</span>
      <button data-fs-element="PlayButton">Play Now</button>
      <button data-fs-element="DemoButton">Try Demo</button>
    </article>
    
    <!-- More game tiles... -->
  </div>
</div>
```

> **Key Insight**: While Fullstory cannot see inside third-party game iframes, you can capture ALL context about which games are played by decorating the wrapper elements and firing events on launch/exit.

### User Identification Pattern

```javascript
// Gaming: Use player ID, never use PII
function onLogin(player) {
  FS('setIdentity', {
    uid: player.playerId,  // e.g., "PLR-789456"
    displayName: `Player ${player.playerId.slice(-4)}`
  });
  
  FS('setProperties', {
    type: 'user',
    properties: {
      // Segmentation (non-sensitive)
      account_type: player.accountType,  // "standard", "vip", "high_roller"
      account_age_days: daysSince(player.registeredAt),
      verification_status: player.kycStatus,  // "pending", "verified", "restricted"
      preferred_product: player.topProduct,  // "sports", "casino", "poker"
      
      // Engagement (generic)
      days_since_last_bet: daysSince(player.lastBetAt),
      active_days_30d: player.activeDays30d,
      
      // Jurisdiction
      jurisdiction: player.jurisdiction,  // "UK", "NJ", "Malta"
      currency: player.currency,
      
      // Feature access
      has_deposit_limit: player.limits.depositLimit !== null,
      has_loss_limit: player.limits.lossLimit !== null,
      has_session_limit: player.limits.sessionLimit !== null,
      
      // Marketing
      bonus_eligible: player.bonusEligible,
      email_opted_in: player.emailOptIn,
      
      // NEVER include:
      // balance, lifetime_deposits, lifetime_losses, gaming_history
    }
  });
}
```

---

## Page-Specific Implementations

### Registration / KYC Flow

```html
<!-- Registration Page -->
<div class="registration-page">
  <h1 class="fs-unmask">Create Your Account</h1>
  
  <!-- Step indicator - visible -->
  <div class="progress fs-unmask">
    <span class="active">1. Details</span>
    <span>2. Verify</span>
    <span>3. Deposit</span>
  </div>
  
  <!-- Personal details - MASK -->
  <section class="personal-details">
    <h2 class="fs-unmask">Personal Information</h2>
    
    <div class="form-fields fs-mask">
      <input type="text" name="firstName" placeholder="First Name" />
      <input type="text" name="lastName" placeholder="Last Name" />
      <input type="email" name="email" placeholder="Email" />
      <input type="tel" name="phone" placeholder="Phone" />
      <input type="date" name="dob" placeholder="Date of Birth" />
    </div>
  </section>
  
  <!-- Address - MASK -->
  <section class="address-details fs-mask">
    <h2 class="fs-unmask">Address</h2>
    <input type="text" name="address1" placeholder="Street Address" />
    <input type="text" name="city" placeholder="City" />
    <select name="state"><!-- States --></select>
    <input type="text" name="zip" placeholder="ZIP Code" />
  </section>
  
  <!-- ID verification - EXCLUDE completely -->
  <section class="id-verification">
    <h2 class="fs-unmask">Identity Verification</h2>
    
    <div class="id-upload fs-exclude">
      <!-- ID document upload - NEVER capture -->
      <p>Upload a photo of your ID</p>
      <input type="file" name="idDocument" />
      <img id="id-preview" />
    </div>
    
    <div class="ssn-field fs-exclude">
      <label>Last 4 of SSN (US only)</label>
      <input type="text" name="ssn4" maxlength="4" />
    </div>
  </section>
  
  <!-- Terms - visible -->
  <section class="terms fs-unmask">
    <label>
      <input type="checkbox" name="terms" />
      I am 21+ and agree to the Terms of Service
    </label>
    <label>
      <input type="checkbox" name="gaming_aware" />
      I acknowledge the responsible gaming information
    </label>
  </section>
  
  <!-- Actions - visible -->
  <div class="form-actions fs-unmask">
    <button type="submit">Create Account</button>
  </div>
</div>
```

```javascript
// Registration tracking
function trackRegistrationStep(step, data) {
  FS('trackEvent', {
    name: 'registration_step_completed',
    properties: {
      step_number: step,
      step_name: data.stepName,  // "details", "verification", "deposit"
      jurisdiction: data.jurisdiction,
      // Never include PII
    }
  });
}

function onRegistrationComplete(player) {
  FS('trackEvent', {
    name: 'registration_completed',
    properties: {
      registration_method: 'email',  // "email", "social", "sso"
      jurisdiction: player.jurisdiction,
      verification_method: player.kycMethod,  // "document", "instant"
      time_to_complete_minutes: getRegistrationDuration()
    }
  });
}
```

### Sports Gaming - Event Browsing

```html
<!-- Sportsbook - Event List -->
<div class="sportsbook">
  <!-- Navigation - visible -->
  <nav class="sport-nav fs-unmask">
    <a href="/football">Football</a>
    <a href="/basketball">Basketball</a>
    <a href="/tennis">Tennis</a>
    <a href="/soccer">Soccer</a>
  </nav>
  
  <!-- Live/upcoming toggle - visible -->
  <div class="event-filter fs-unmask">
    <button class="active">Live</button>
    <button>Today</button>
    <button>This Week</button>
  </div>
  
  <!-- Event list - visible (public sports data) -->
  <div class="events-list fs-unmask">
    <div class="event-card"
         data-fs-element="Event Card"
         data-fs-properties-schema='{"event_id":"string","sport":"string","competition":"string","is_live":"bool"}'>
      <div class="event-header">
        <span class="sport-icon">🏈</span>
        <span class="competition">NFL - Week 14</span>
        <span class="live-badge">LIVE</span>
      </div>
      
      <div class="event-matchup">
        <div class="team home">
          <span class="name">Kansas City Chiefs</span>
          <span class="score">21</span>
        </div>
        <div class="team away">
          <span class="name">Buffalo Bills</span>
          <span class="score">17</span>
        </div>
      </div>
      
      <!-- Odds display - visible (public data) -->
      <div class="odds-display">
        <button class="odd" data-selection="home_ml">
          Chiefs -150
        </button>
        <button class="odd" data-selection="spread">
          -3.5 (-110)
        </button>
        <button class="odd" data-selection="away_ml">
          Bills +130
        </button>
      </div>
    </div>
    <!-- More events... -->
  </div>
</div>
```

```javascript
// Sports browsing tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'sportsbook',
    sport: 'football',
    competition: 'NFL',
    event_view: 'live',
    event_count: 12
  }
});

// Event view
function onEventView(event) {
  FS('trackEvent', {
    name: 'event_viewed',
    properties: {
      event_id: event.id,
      sport: event.sport,
      competition: event.competition,
      is_live: event.isLive,
      market_count: event.markets.length
    }
  });
}

// Odds click (selection added to bet slip)
function onOddsClick(selection) {
  FS('trackEvent', {
    name: 'selection_added',
    properties: {
      event_id: selection.eventId,
      sport: selection.sport,
      market_type: selection.marketType,  // "moneyline", "spread", "total"
      selection_type: selection.type,  // "home", "away", "over", "under"
      // Don't include odds values - they change
    }
  });
}
```

### Bet Slip

```html
<!-- Bet Slip -->
<div class="bet-slip">
  <h2 class="fs-unmask">Bet Slip</h2>
  
  <!-- Selections - visible (public event data) -->
  <div class="selections fs-unmask">
    <div class="selection">
      <button class="remove">×</button>
      <div class="selection-info">
        <span class="event">Chiefs vs Bills</span>
        <span class="pick">Kansas City Chiefs -3.5</span>
        <span class="odds">-110</span>
      </div>
    </div>
    <!-- More selections... -->
  </div>
  
  <!-- Bet type - visible -->
  <div class="bet-type fs-unmask">
    <button class="active">Single</button>
    <button>Parlay</button>
  </div>
  
  <!-- Stake input - EXCLUDE (financial) -->
  <div class="stake-section fs-exclude">
    <label>Stake</label>
    <input type="number" name="stake" placeholder="$0.00" />
    
    <!-- Quick stake buttons - visible pattern, not amounts -->
    <div class="quick-stakes fs-unmask">
      <button data-amount="10">$10</button>
      <button data-amount="25">$25</button>
      <button data-amount="50">$50</button>
      <button data-amount="100">$100</button>
    </div>
  </div>
  
  <!-- Potential payout - EXCLUDE -->
  <div class="payout-display fs-exclude">
    <span class="label">To Win:</span>
    <span class="amount">$90.91</span>
    <span class="label">Total Payout:</span>
    <span class="amount">$190.91</span>
  </div>
  
  <!-- Place bet button - visible for funnel -->
  <button class="place-bet fs-unmask">Place Bet</button>
</div>
```

```javascript
// Bet slip tracking
FS('trackEvent', {
  name: 'bet_slip_viewed',
  properties: {
    selection_count: selections.length,
    bet_type: 'single',  // "single", "parlay", "teaser"
    sports: [...new Set(selections.map(s => s.sport))],
    // Never: stake amount, potential payout
  }
});

// Bet placement (use ranges for amounts)
function onBetPlaced(bet) {
  FS('trackEvent', {
    name: 'bet_placed',
    properties: {
      bet_id: bet.id,
      bet_type: bet.type,
      selection_count: bet.selections.length,
      sports: bet.sports,
      stake_range: getStakeRange(bet.stake),  // "$1-$10", "$10-$50", etc.
      is_live_bet: bet.isLive,
      // Never: exact stake, potential win
    }
  });
}

function getStakeRange(stake) {
  if (stake <= 10) return '$1-$10';
  if (stake <= 50) return '$10-$50';
  if (stake <= 100) return '$50-$100';
  if (stake <= 500) return '$100-$500';
  return '$500+';
}
```

### Casino Game Lobby

```html
<!-- Casino Lobby -->
<div class="casino-lobby">
  <h1 class="fs-unmask">Casino Games</h1>
  
  <!-- Category nav - visible -->
  <nav class="game-categories fs-unmask">
    <a href="#slots">Slots</a>
    <a href="#table">Table Games</a>
    <a href="#live">Live Casino</a>
    <a href="#jackpots">Jackpots</a>
  </nav>
  
  <!-- Game grid - visible (game names are public) -->
  <div class="game-grid fs-unmask">
    <div class="game-card"
         data-fs-element="Game Card"
         data-fs-properties-schema='{"game_id":"string","game_name":"string","game_type":"string","provider":"string"}'>
      <img src="slot-thumbnail.jpg" alt="Starburst" />
      <h3>Starburst</h3>
      <p class="provider">NetEnt</p>
      <button class="play-btn">Play Now</button>
      <button class="demo-btn">Demo</button>
    </div>
    <!-- More games... -->
  </div>
  
  <!-- Jackpot displays - values can be visible (they're promotional) -->
  <div class="jackpot-tickers fs-unmask">
    <div class="jackpot">
      <span class="name">Mega Moolah</span>
      <span class="amount">$15,234,567.89</span>
    </div>
  </div>
</div>
```

```javascript
// Casino lobby tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'casino_lobby',
    game_category: 'all',
    game_count: 250,
    featured_game_count: 12
  }
});

// Game launch
function onGameLaunch(game, mode) {
  FS('trackEvent', {
    name: 'game_launched',
    properties: {
      game_id: game.id,
      game_name: game.name,
      game_type: game.type,  // "slot", "table", "live"
      provider: game.provider,
      play_mode: mode,  // "real", "demo"
      is_mobile: isMobile()
    }
  });
}
```

### Deposit Flow

```html
<!-- Deposit Page -->
<div class="deposit-page">
  <h1 class="fs-unmask">Deposit</h1>
  
  <!-- Current balance - EXCLUDE -->
  <div class="current-balance fs-exclude">
    <span>Current Balance: $250.00</span>
  </div>
  
  <!-- Payment method selection - visible -->
  <div class="payment-methods fs-unmask">
    <h2>Select Payment Method</h2>
    <button class="method" data-method="card">
      <img src="card-icon.svg" alt="" />
      Credit/Debit Card
    </button>
    <button class="method" data-method="paypal">
      <img src="paypal-icon.svg" alt="" />
      PayPal
    </button>
    <button class="method" data-method="skrill">
      <img src="skrill-icon.svg" alt="" />
      Skrill
    </button>
    <button class="method" data-method="bank">
      <img src="bank-icon.svg" alt="" />
      Bank Transfer
    </button>
  </div>
  
  <!-- Amount selection - EXCLUDE specific amounts -->
  <div class="amount-section">
    <h2 class="fs-unmask">Select Amount</h2>
    
    <!-- Quick amounts - can show buttons, not selections -->
    <div class="quick-amounts fs-unmask">
      <button data-amount="20">$20</button>
      <button data-amount="50">$50</button>
      <button data-amount="100">$100</button>
      <button data-amount="200">$200</button>
    </div>
    
    <!-- Custom amount - EXCLUDE -->
    <div class="custom-amount fs-exclude">
      <input type="number" name="amount" placeholder="Custom amount" />
    </div>
    
    <!-- Deposit limits display - EXCLUDE (sensitive) -->
    <div class="limit-info fs-exclude">
      <p>Daily limit: $500 (remaining: $300)</p>
    </div>
  </div>
  
  <!-- Card form - EXCLUDE -->
  <div class="card-form fs-exclude">
    <input type="text" name="cardNumber" placeholder="Card Number" />
    <input type="text" name="expiry" placeholder="MM/YY" />
    <input type="text" name="cvv" placeholder="CVV" />
  </div>
  
  <!-- Submit - visible -->
  <button class="submit-deposit fs-unmask">Deposit</button>
</div>
```

```javascript
// Deposit tracking
function onDepositInitiated(method) {
  FS('trackEvent', {
    name: 'deposit_initiated',
    properties: {
      payment_method: method,  // "card", "paypal", "skrill", "bank"
      is_first_deposit: player.depositCount === 0,
      // Never: amount
    }
  });
}

function onDepositCompleted(deposit) {
  FS('trackEvent', {
    name: 'deposit_completed',
    properties: {
      payment_method: deposit.method,
      amount_range: getAmountRange(deposit.amount),
      is_first_deposit: deposit.isFirst,
      time_to_complete_seconds: deposit.processingTime
      // Never: exact amount
    }
  });
}

function onDepositFailed(error) {
  FS('trackEvent', {
    name: 'deposit_failed',
    properties: {
      payment_method: error.method,
      error_category: categorizeDepositError(error),  // "declined", "limit_exceeded", "technical"
      // Never: exact amount, card details
    }
  });
}
```

### Responsible Gaming Features

This is extremely sensitive - track usage patterns for UX but NEVER track specific limits or self-exclusion details.

```html
<!-- Responsible Gaming Page - VERY SENSITIVE -->
<div class="responsible-gaming">
  <h1 class="fs-unmask">Responsible Gaming Tools</h1>
  
  <!-- Feature overview - visible -->
  <div class="rg-tools-overview fs-unmask">
    <p>We provide tools to help you stay in control.</p>
  </div>
  
  <!-- All limit settings - EXCLUDE completely -->
  <section class="limits-section fs-exclude">
    <h2>Deposit Limits</h2>
    <div class="limit-setting">
      <label>Daily Limit</label>
      <input type="number" name="dailyLimit" />
    </div>
    <div class="limit-setting">
      <label>Weekly Limit</label>
      <input type="number" name="weeklyLimit" />
    </div>
    <div class="limit-setting">
      <label>Monthly Limit</label>
      <input type="number" name="monthlyLimit" />
    </div>
  </section>
  
  <!-- Session limits - EXCLUDE -->
  <section class="session-limits fs-exclude">
    <h2>Session Limits</h2>
    <div class="limit-setting">
      <label>Session Time Limit</label>
      <select name="sessionLimit">
        <option>No limit</option>
        <option>1 hour</option>
        <option>2 hours</option>
      </select>
    </div>
  </section>
  
  <!-- Self-exclusion - EXCLUDE completely -->
  <section class="self-exclusion fs-exclude">
    <h2>Take a Break</h2>
    <button>24-hour cool-off</button>
    <button>7-day break</button>
    <button>30-day break</button>
    <button>Self-exclude (6+ months)</button>
  </section>
  
  <!-- Reality check settings - EXCLUDE -->
  <section class="reality-check fs-exclude">
    <h2>Reality Check</h2>
    <p>Get reminders about your session length</p>
    <select name="realityCheck">
      <option>Every 30 minutes</option>
      <option>Every 60 minutes</option>
    </select>
  </section>
  
  <!-- Help resources - visible (important for users) -->
  <section class="help-resources fs-unmask">
    <h2>Get Help</h2>
    <a href="tel:1-800-522-4700">National Problem Gaming Helpline</a>
    <a href="https://www.gamblersanonymous.org">Gamblers Anonymous</a>
  </section>
</div>
```

```javascript
// Responsible gaming page tracking - BE VERY CAREFUL
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'responsible_gaming',
    // Only track that they visited, not what they set
  }
});

// Track only that RG features were accessed (for UX research on feature discoverability)
// NEVER track specific limits, self-exclusion requests, or problem gaming indicators

function onRGPageView() {
  FS('trackEvent', {
    name: 'responsible_gaming_page_viewed',
    properties: {
      referrer_type: getReferrerType()  // "menu", "footer", "prompt"
      // NEVER: what limits they have, what they're changing
    }
  });
}

// You might track if help resources were clicked (to ensure they work)
function onHelpResourceClick(resource) {
  FS('trackEvent', {
    name: 'help_resource_clicked',
    properties: {
      resource_type: resource.type  // "helpline", "external_site"
      // Don't track which specific resource
    }
  });
}
```

### Account / Transaction History

```html
<!-- Transaction History -->
<div class="transaction-history">
  <h1 class="fs-unmask">Transaction History</h1>
  
  <!-- Filters - visible -->
  <div class="filters fs-unmask">
    <select name="type">
      <option>All</option>
      <option>Deposits</option>
      <option>Withdrawals</option>
      <option>Bets</option>
      <option>Wins</option>
    </select>
    <select name="period">
      <option>Last 7 days</option>
      <option>Last 30 days</option>
      <option>Last 90 days</option>
    </select>
    <button>Apply</button>
  </div>
  
  <!-- Transaction list - EXCLUDE amounts -->
  <div class="transaction-list fs-exclude">
    <!-- All transaction details are sensitive:
         - Amounts reveal gaming activity
         - Win/loss patterns
         - Deposit frequency
    -->
    <div class="transaction">
      <span class="date">Dec 1, 2024</span>
      <span class="type">Deposit</span>
      <span class="method">Visa ****1234</span>
      <span class="amount">+$100.00</span>
    </div>
    <div class="transaction">
      <span class="date">Dec 1, 2024</span>
      <span class="type">Bet - NFL</span>
      <span class="details">Chiefs vs Bills</span>
      <span class="amount">-$25.00</span>
    </div>
  </div>
  
  <!-- Pagination - visible -->
  <div class="pagination fs-unmask">
    <button>Previous</button>
    <button>Next</button>
  </div>
</div>
```

---

## Player Behavior Considerations

### What NOT to Analyze in Fullstory

Some analyses could facilitate problem gaming identification or discrimination:

❌ **Never analyze or segment by:**
- Session duration patterns (could indicate addiction)
- Loss chasing behavior
- Deposit frequency
- Late-night gaming patterns
- Wagering amount trends
- Win/loss ratios

✅ **OK to analyze:**
- Feature usability (did they find the bet slip?)
- Navigation paths (how do users find games?)
- Error rates (are deposits failing?)
- Mobile vs desktop usage
- A/B test results for UX changes

---

## Jurisdiction-Specific Considerations

### UK (UKGC)

```javascript
// UK-specific: Track interaction with affordability checks
// But NEVER track the actual amounts or outcomes
FS('trackEvent', {
  name: 'affordability_check_shown',
  properties: {
    trigger: 'deposit_threshold',  // Why it was shown
    // Never: deposit amount, check result
  }
});
```

### US State-by-State

```javascript
// Track geolocation verification
FS('trackEvent', {
  name: 'geolocation_verification',
  properties: {
    state: geoResult.state,
    success: geoResult.success,
    method: geoResult.method  // "gps", "ip", "manual"
    // Never: exact coordinates
  }
});
```

---

## Common Gaming Patterns

### Amount Range Helper

```javascript
function getAmountRange(amount) {
  if (amount <= 10) return '$1-$10';
  if (amount <= 25) return '$10-$25';
  if (amount <= 50) return '$25-$50';
  if (amount <= 100) return '$50-$100';
  if (amount <= 250) return '$100-$250';
  if (amount <= 500) return '$250-$500';
  if (amount <= 1000) return '$500-$1000';
  return '$1000+';
}
```

### Session Duration (Generic)

```javascript
// Track session duration in bands, not exact times
function getSessionDurationBand(minutes) {
  if (minutes < 15) return '<15min';
  if (minutes < 30) return '15-30min';
  if (minutes < 60) return '30-60min';
  if (minutes < 120) return '1-2hours';
  return '2hours+';  // Don't get more specific - could indicate problem gaming
}
```

---

## KEY TAKEAWAYS FOR AGENT

When helping gaming clients with Fullstory:

1. **Regulatory awareness**: Different jurisdictions have different requirements
2. **Financial data is highly sensitive**: Always exclude or use ranges
3. **Responsible gaming features**: NEVER analyze specific limit settings or self-exclusion
4. **Behavior patterns**: Be careful about what patterns you enable - could indicate addiction
5. **KYC/AML data**: ID documents, SSN must never be captured
6. **Public data is OK**: Odds, game names, sports events are fine

### Questions to Ask Gaming Clients

1. "What jurisdictions do you operate in?"
2. "How do you handle responsible gaming feature tracking?"
3. "Is your session replay access audited?"
4. "How do you ensure self-exclusion data isn't exposed?"
5. "Are ID verification screens properly excluded?"

### Red Flags to Watch For

- Tracking specific bet/deposit amounts
- Analyzing session duration patterns
- Segmenting users by gaming frequency
- Capturing ID verification screens
- Exposing self-exclusion or limit settings
- Tracking reality check dismissals

### Ethical Considerations

Remember: Fullstory in gaming should help improve UX, NOT enable:
- Problem gaming identification for marketing
- Surveillance of player behavior
- Discrimination based on gaming patterns

The goal is better UX for all players, not optimizing revenue extraction.

---

## REFERENCE LINKS

### Fullstory Gaming Resources
- **Fullstory Gaming Industry Page**: https://www.fullstory.com/industries/gaming/
- **Responsible Gaming Compliance**: https://www.fullstory.com/blog/identify-high-risk-gambling-behavior/
- **Fraud Prevention Guide**: https://www.fullstory.com/blog/prevent-online-gambling-fraud/
- **High-Value Player Retention**: https://www.fullstory.com/blog/high-value-player-retention-igaming/

### Regulatory Resources
- **UK Gambling Commission (UKGC)**: https://www.gamblingcommission.gov.uk/
- **Malta Gaming Authority**: https://www.mga.org.mt/
- **Responsible Gaming Council**: https://www.responsiblegaming.org/

### Related Skills
- **Fullstory Privacy Controls**: ../core/fullstory-privacy-controls/SKILL.md
- **Fullstory Privacy Strategy**: ../meta/fullstory-privacy-strategy/SKILL.md

---

*This skill document is specific to gaming implementations. Always consult your compliance team and legal counsel regarding jurisdiction-specific requirements.*

