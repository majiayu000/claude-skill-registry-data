---
name: fullstory-media-entertainment
version: v2
description: Industry-specific guide for implementing Fullstory in media, entertainment, and streaming applications. Covers subscription funnel optimization, content engagement tracking, video player UX, paywall optimization, and ad-supported vs subscription models. Includes detailed examples for streaming services, news sites, gaming platforms, and content creators.
related_skills:
  - fullstory-privacy-controls
  - fullstory-privacy-strategy
  - fullstory-analytics-events
  - fullstory-user-properties
  - fullstory-element-properties
---

# Fullstory for Media & Entertainment

> ⚠️ **LEGAL DISCLAIMER**: This guidance is for educational purposes only and does not constitute legal, compliance, or regulatory advice. Media applications may be subject to various regulations (GDPR, CCPA, COPPA for children's content, accessibility requirements). Always consult with your legal and compliance teams before implementing any data capture solution. Your organization is responsible for ensuring compliance with all applicable regulations.

## Industry Overview

Media and entertainment have unique characteristics for session analytics:

- **Engagement focus**: Time spent, content consumed, completion rates
- **Subscription models**: Free vs. paid, trial conversions, churn prevention
- **Content discovery**: Recommendations, search, browsing patterns
- **Ad-supported models**: Ad viewability, skip rates, revenue optimization
- **Multi-device**: TV, mobile, web, tablet experiences
- **Personalization**: Recommendation effectiveness, preference learning

### Key Goals for Media Implementations

1. **Optimize subscription conversion** and reduce churn
2. **Understand content engagement** patterns
3. **Improve content discovery** and recommendations
4. **Reduce friction** in video playback experience
5. **Optimize paywall** placement and messaging
6. **Track cross-device** user journeys

---

## What Can Be Captured in Media

| Data Type | Capture? | Privacy Level | Notes |
|-----------|----------|---------------|-------|
| Content viewed (titles) | ✅ Yes | Unmask | Core analytics |
| Watch time / progress | ✅ Yes | Unmask | Engagement metrics |
| Search queries | ✅ Yes | Unmask | Content discovery |
| Browse behavior | ✅ Yes | Unmask | Recommendation analysis |
| Subscription plan | ✅ Yes | Unmask | Segmentation |
| User preferences | ✅ Yes | Unmask | Product data |
| Ratings/reviews | ⚠️ Consider | Mask if user visible | User-generated |
| User names | ⚠️ Mask | Mask | PII |
| Email | ⚠️ Consider | Hash/Mask | For identification |
| Payment details | ❌ Never | Exclude | PCI |
| Children's data | ❌ Never | Exclude | COPPA |

### Special Consideration: COPPA Compliance

If your platform serves children under 13:
- ❌ Do NOT use Fullstory on children's profiles
- ❌ Do NOT capture any data about children's viewing habits
- ✅ Only capture data for verified adult accounts

### Accessibility Feature Tracking

Media platforms must track accessibility feature usage to ensure compliance with WCAG/ADA requirements and improve experiences for all users:

| Accessibility Feature | Track? | Why |
|----------------------|--------|-----|
| **Closed captions/subtitles** | ✅ Yes | Engagement with CC content |
| **Audio descriptions** | ✅ Yes | Usage rates, content coverage |
| **Playback speed** | ✅ Yes | Accessibility and preference |
| **Screen reader compatibility** | ⚠️ Consider | May need special implementation |
| **Keyboard navigation** | ✅ Yes | Identifies non-mouse users |
| **Font size/contrast settings** | ✅ Yes | Accessibility preference adoption |
| **Disability status** | ❌ Never | Sensitive PII |

```javascript
// Track accessibility feature usage
FS('trackEvent', {
  name: 'accessibility_feature_enabled',
  properties: {
    feature: 'closed_captions',
    language: 'en',
    content_type: 'movie',
    content_id: 'mov_12345',
    first_time: true,   // Is this the first time this user enabled CC?
    // Helps identify accessibility feature adoption and content gaps
  }
});

// Track accessibility journey patterns
FS('setProperties', {
  type: 'user',
  properties: {
    uses_captions: true,
    uses_audio_descriptions: false,
    preferred_playback_speed: 1.0,
    // Never track WHY they use these features, only THAT they do
  }
});
```

> **Important**: Track accessibility feature usage to improve coverage and experience, but NEVER ask or infer why users need these features.

---

## Implementation Architecture

### Privacy Zones for Media

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEDIA APPLICATION                             │
├─────────────────────────────────────────────────────────────────┤
│  FULLY VISIBLE (fs-unmask)                                       │
│  • Content catalog and browse UI                                 │
│  • Video player controls                                         │
│  • Search interface and results                                  │
│  • Content details (titles, descriptions)                        │
│  • Subscription plans and pricing                               │
│  • Recommendation carousels                                      │
│  • Navigation and menus                                          │
│  • Error messages                                               │
├─────────────────────────────────────────────────────────────────┤
│  MASKED (fs-mask)                                                │
│  • User display names                                           │
│  • Profile names                                                │
│  • User-generated content (reviews, comments)                   │
│  • Email addresses                                              │
│  • Custom playlist names                                        │
├─────────────────────────────────────────────────────────────────┤
│  EXCLUDED (fs-exclude)                                           │
│  • Payment card details                                         │
│  • Billing address                                              │
│  • Password fields                                              │
│  • Children's profiles                                          │
│  • Private messages                                             │
│  • Gift card codes                                              │
└─────────────────────────────────────────────────────────────────┘
```

### User Identification Pattern

```javascript
// Media: Identify by account, track viewing behavior
function onLogin(user) {
  // Check for children's profile - DO NOT track
  if (user.profile.isKids) {
    FS('shutdown');
    return;
  }
  
  FS('setIdentity', {
    uid: user.accountId,
    displayName: user.profile.name  // Profile name, not real name
  });
  
  FS('setProperties', {
    type: 'user',
    properties: {
      // Subscription info
      subscription_plan: user.subscription.plan,  // "free", "basic", "standard", "premium"
      subscription_status: user.subscription.status,  // "active", "trial", "cancelled", "paused"
      is_trial: user.subscription.isTrial,
      trial_days_remaining: user.subscription.trialDaysRemaining,
      subscription_tenure_months: getMonthsSince(user.subscription.startDate),
      
      // Account info
      account_age_days: daysSince(user.createdAt),
      profiles_count: user.profilesCount,
      is_family_plan: user.isFamilyPlan,
      
      // Engagement metrics
      content_watched_30d: user.contentWatched30d,
      hours_watched_30d: user.hoursWatched30d,
      days_active_30d: user.daysActive30d,
      
      // Preferences
      preferred_genres: user.topGenres.slice(0, 3),  // Top 3 genres
      preferred_content_type: user.preferredType,  // "movies", "series", "documentaries"
      language: user.preferredLanguage,
      
      // Platform usage
      primary_device: user.primaryDevice,  // "tv", "mobile", "web"
      download_enabled: user.hasDownloads,
      
      // Marketing
      email_subscribed: user.emailOptIn
    }
  });
}
```

---

## Page-Specific Implementations

### Browse / Home Page

```html
<!-- Home/Browse Page -->
<div class="browse-page">
  <!-- Hero content - visible -->
  <section class="hero fs-unmask"
           data-fs-element="Hero Banner"
           data-fs-properties-schema='{"content_id":"string","content_title":"string","content_type":"string"}'>
    <div class="hero-content">
      <img src="hero-bg.jpg" alt="" class="hero-bg" />
      <div class="hero-info">
        <h1>Stranger Things</h1>
        <p class="metadata">TV-14 · 4 Seasons · Sci-Fi, Horror</p>
        <p class="description">When a young boy vanishes...</p>
        <div class="hero-actions">
          <button class="play-btn">▶ Play</button>
          <button class="info-btn">More Info</button>
          <button class="list-btn">+ My List</button>
        </div>
      </div>
    </div>
  </section>
  
  <!-- Continue Watching - visible (your data about their viewing) -->
  <section class="content-row fs-unmask">
    <h2>Continue Watching</h2>
    <div class="content-carousel"
         data-fs-element="Content Carousel"
         data-fs-properties-schema='{"row_type":"string","row_position":"int"}'>
      <div class="content-card"
           data-fs-element="Content Card"
           data-fs-properties-schema='{"content_id":"string","content_title":"string","progress_percent":"int"}'>
        <img src="thumbnail.jpg" alt="Breaking Bad" />
        <div class="progress-bar">
          <div class="progress" style="width: 65%"></div>
        </div>
        <h3>Breaking Bad</h3>
        <p class="episode">S2 E5 · 35 min remaining</p>
      </div>
      <!-- More cards... -->
    </div>
    <button class="carousel-prev">‹</button>
    <button class="carousel-next">›</button>
  </section>
  
  <!-- Recommendations - visible -->
  <section class="content-row fs-unmask">
    <h2>Because You Watched "Breaking Bad"</h2>
    <div class="content-carousel">
      <div class="content-card">
        <img src="thumbnail.jpg" alt="Better Call Saul" />
        <h3>Better Call Saul</h3>
        <p class="match">98% Match</p>
      </div>
      <!-- More recommendations... -->
    </div>
  </section>
  
  <!-- Trending - visible -->
  <section class="content-row fs-unmask">
    <h2>Trending Now</h2>
    <div class="content-carousel">
      <div class="content-card ranked">
        <span class="rank">1</span>
        <img src="thumbnail.jpg" alt="New Release" />
      </div>
      <!-- More trending... -->
    </div>
  </section>
  
  <!-- Genre rows - visible -->
  <section class="content-row fs-unmask">
    <h2>Action & Adventure</h2>
    <div class="content-carousel">
      <!-- Content cards... -->
    </div>
  </section>
</div>
```

```javascript
// Browse page tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'browse_home',
    profile_type: 'adult',  // never "kids"
    content_rows_visible: 8,
    has_continue_watching: continueWatching.length > 0,
    hero_content_id: heroContent.id,
    hero_content_type: heroContent.type
  }
});

// Content row visibility (scroll tracking)
function onRowVisible(row) {
  FS('trackEvent', {
    name: 'content_row_viewed',
    properties: {
      row_title: row.title,
      row_type: row.type,  // "continue_watching", "recommendation", "trending", "genre"
      row_position: row.position,
      cards_in_row: row.contentCount,
      cards_visible: row.visibleCount
    }
  });
}

// Carousel interaction
function onCarouselScroll(row, direction) {
  FS('trackEvent', {
    name: 'carousel_scrolled',
    properties: {
      row_title: row.title,
      row_type: row.type,
      direction: direction,  // "left", "right"
      cards_scrolled: cardsScrolled
    }
  });
}

// Content hover (shows engagement)
function onContentHover(content) {
  FS('trackEvent', {
    name: 'content_hover',
    properties: {
      content_id: content.id,
      content_title: content.title,
      content_type: content.type,
      row_type: content.rowType,
      position_in_row: content.position,
      hover_duration_ms: hoverDuration
    }
  });
}
```

### Content Detail Page

```html
<!-- Content Detail Page -->
<div class="content-detail">
  <!-- Hero section - visible -->
  <section class="detail-hero fs-unmask">
    <img src="backdrop.jpg" alt="" class="backdrop" />
    <div class="detail-info"
         data-fs-element="Content Detail"
         data-fs-properties-schema='{"content_id":"string","content_title":"string","content_type":"string","genre":"string"}'>
      <h1>Breaking Bad</h1>
      <div class="metadata">
        <span class="match">98% Match</span>
        <span class="year">2008</span>
        <span class="rating">TV-MA</span>
        <span class="seasons">5 Seasons</span>
      </div>
      
      <div class="actions">
        <button class="play-btn">▶ Play S2:E5</button>
        <button class="trailer-btn">Watch Trailer</button>
        <button class="list-btn">+ My List</button>
        <button class="like-btn">👍</button>
        <button class="dislike-btn">👎</button>
      </div>
      
      <p class="description">
        A high school chemistry teacher turned methamphetamine manufacturer...
      </p>
      
      <div class="cast-crew">
        <p><strong>Starring:</strong> Bryan Cranston, Aaron Paul, Anna Gunn</p>
        <p><strong>Creator:</strong> Vince Gilligan</p>
      </div>
      
      <div class="tags">
        <span>Dark</span>
        <span>Suspenseful</span>
        <span>Crime Drama</span>
      </div>
    </div>
  </section>
  
  <!-- Episode selector - visible -->
  <section class="episodes-section fs-unmask">
    <div class="season-selector">
      <label>Season</label>
      <select name="season">
        <option value="1">Season 1</option>
        <option value="2" selected>Season 2</option>
        <option value="3">Season 3</option>
        <option value="4">Season 4</option>
        <option value="5">Season 5</option>
      </select>
    </div>
    
    <div class="episode-list">
      <div class="episode-card"
           data-fs-element="Episode Card"
           data-fs-properties-schema='{"episode_id":"string","season":"int","episode":"int"}'>
        <img src="episode-thumb.jpg" alt="" />
        <div class="episode-info">
          <h3>1. Seven Thirty-Seven</h3>
          <p class="duration">47 min</p>
          <p class="synopsis">Walt and Jesse face the deadly consequences...</p>
        </div>
        <button class="play-episode">▶</button>
      </div>
      <!-- More episodes... -->
    </div>
  </section>
  
  <!-- Related content - visible -->
  <section class="related-content fs-unmask">
    <h2>More Like This</h2>
    <div class="content-grid">
      <!-- Content cards... -->
    </div>
  </section>
</div>
```

```javascript
// Content detail tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'content_detail',
    content_id: content.id,
    content_title: content.title,
    content_type: content.type,  // "movie", "series"
    genre: content.primaryGenre,
    release_year: content.year,
    rating: content.rating,  // "TV-MA", "PG-13"
    seasons: content.seasons,
    is_in_my_list: content.inMyList,
    user_progress_percent: content.userProgress
  }
});

// Content detail interactions
function onAddToList(content) {
  FS('trackEvent', {
    name: 'content_added_to_list',
    properties: {
      content_id: content.id,
      content_title: content.title,
      content_type: content.type,
      source: 'detail_page'
    }
  });
}

function onRating(content, rating) {
  FS('trackEvent', {
    name: 'content_rated',
    properties: {
      content_id: content.id,
      content_title: content.title,
      rating_type: rating  // "like", "dislike", "love"
    }
  });
}

function onEpisodeSelect(episode) {
  FS('trackEvent', {
    name: 'episode_selected',
    properties: {
      content_id: episode.seriesId,
      season: episode.season,
      episode: episode.episode,
      selection_method: 'episode_list'
    }
  });
}
```

### Video Player

```html
<!-- Video Player - Careful with overlay UI -->
<div class="video-player">
  <!-- Video container - visible for interaction tracking -->
  <div class="player-container fs-unmask"
       data-fs-element="Video Player"
       data-fs-properties-schema='{"content_id":"string","content_title":"string","playback_quality":"string"}'>
    <video id="video-element"></video>
    
    <!-- Player controls - visible -->
    <div class="player-controls">
      <button class="play-pause">▶</button>
      
      <div class="progress-bar">
        <div class="progress" style="width: 45%"></div>
        <div class="buffer" style="width: 60%"></div>
      </div>
      
      <span class="time-display">23:45 / 52:10</span>
      
      <button class="skip-intro">Skip Intro</button>
      <button class="skip-recap">Skip Recap</button>
      
      <button class="volume">🔊</button>
      <button class="subtitles">CC</button>
      <button class="audio-tracks">🔈</button>
      <button class="quality">HD</button>
      <button class="fullscreen">⛶</button>
    </div>
    
    <!-- Skip buttons - visible (important UX) -->
    <button class="skip-back-10">⟲ 10</button>
    <button class="skip-forward-10">10 ⟳</button>
    
    <!-- Next episode prompt - visible -->
    <div class="next-episode-prompt">
      <p>Next Episode in 5 seconds</p>
      <button class="play-next">Play Next</button>
      <button class="cancel-autoplay">Cancel</button>
    </div>
  </div>
</div>
```

```javascript
// Video player tracking - Rich engagement data
function onPlaybackStart(content) {
  FS('trackEvent', {
    name: 'playback_started',
    properties: {
      content_id: content.id,
      content_title: content.title,
      content_type: content.type,
      season: content.season,
      episode: content.episode,
      
      start_position_seconds: startPosition,
      is_resume: startPosition > 0,
      playback_quality: quality,
      device_type: deviceType,
      
      source: playbackSource  // "browse", "search", "continue_watching", "recommendation"
    }
  });
}

// Periodic progress tracking (every 25%)
function onPlaybackProgress(content, progress) {
  FS('trackEvent', {
    name: 'playback_progress',
    properties: {
      content_id: content.id,
      progress_percent: progress,  // 25, 50, 75, 100
      watch_time_seconds: watchTime,
      playback_quality: currentQuality
    }
  });
}

function onPlaybackComplete(content) {
  FS('trackEvent', {
    name: 'playback_completed',
    properties: {
      content_id: content.id,
      content_title: content.title,
      total_watch_time_seconds: totalWatchTime,
      content_duration_seconds: duration,
      completion_percent: (totalWatchTime / duration) * 100,
      
      skipped_intro: skippedIntro,
      skipped_recap: skippedRecap,
      
      quality_changes: qualityChanges,
      buffering_events: bufferingCount,
      total_buffering_seconds: totalBufferTime
    }
  });
}

// Player interactions
function onSkipIntro() {
  FS('trackEvent', {
    name: 'player_interaction',
    properties: {
      action: 'skip_intro',
      content_id: content.id,
      timestamp_seconds: currentTime
    }
  });
}

function onSeek(fromTime, toTime) {
  FS('trackEvent', {
    name: 'player_interaction',
    properties: {
      action: 'seek',
      content_id: content.id,
      seek_from_seconds: fromTime,
      seek_to_seconds: toTime,
      seek_direction: toTime > fromTime ? 'forward' : 'backward'
    }
  });
}

function onQualityChange(oldQuality, newQuality, manual) {
  FS('trackEvent', {
    name: 'player_interaction',
    properties: {
      action: 'quality_change',
      content_id: content.id,
      from_quality: oldQuality,
      to_quality: newQuality,
      is_manual: manual,  // vs adaptive
      timestamp_seconds: currentTime
    }
  });
}

function onSubtitlesToggle(enabled, language) {
  FS('trackEvent', {
    name: 'player_interaction',
    properties: {
      action: enabled ? 'subtitles_on' : 'subtitles_off',
      content_id: content.id,
      subtitle_language: language
    }
  });
}

// Playback issues
function onBuffering(duration) {
  FS('trackEvent', {
    name: 'playback_issue',
    properties: {
      issue_type: 'buffering',
      content_id: content.id,
      buffering_duration_ms: duration,
      timestamp_seconds: currentTime,
      current_quality: quality
    }
  });
}

function onPlaybackError(error) {
  FS('trackEvent', {
    name: 'playback_issue',
    properties: {
      issue_type: 'error',
      error_category: categorizePlaybackError(error),
      content_id: content.id,
      timestamp_seconds: currentTime
    }
  });
}
```

### Search

```html
<!-- Search Page -->
<div class="search-page">
  <!-- Search input - visible -->
  <div class="search-bar fs-unmask">
    <input 
      type="text" 
      placeholder="Search for titles, people, genres" 
      value="bryan cranston"
    />
    <button class="clear-search">×</button>
  </div>
  
  <!-- Search suggestions - visible -->
  <div class="search-suggestions fs-unmask">
    <h3>Top Searches</h3>
    <ul>
      <li>Breaking Bad</li>
      <li>Stranger Things</li>
      <li>The Office</li>
    </ul>
  </div>
  
  <!-- Search results - visible -->
  <div class="search-results fs-unmask">
    <h2>Results for "bryan cranston"</h2>
    
    <section class="result-group">
      <h3>Titles</h3>
      <div class="results-grid">
        <div class="content-card">
          <img src="breaking-bad.jpg" alt="Breaking Bad" />
          <h4>Breaking Bad</h4>
        </div>
        <div class="content-card">
          <img src="malcolm.jpg" alt="Malcolm in the Middle" />
          <h4>Malcolm in the Middle</h4>
        </div>
      </div>
    </section>
    
    <section class="result-group">
      <h3>People</h3>
      <div class="people-results">
        <div class="person-card">
          <img src="bryan.jpg" alt="Bryan Cranston" />
          <h4>Bryan Cranston</h4>
          <p>Actor, Producer</p>
        </div>
      </div>
    </section>
  </div>
</div>
```

```javascript
// Search tracking
function onSearch(query, results) {
  FS('trackEvent', {
    name: 'content_search',
    properties: {
      search_query: query,
      search_type: 'text',  // or "voice"
      result_count: results.total,
      title_results: results.titles,
      people_results: results.people,
      genre_results: results.genres,
      has_results: results.total > 0
    }
  });
}

function onSearchResultClick(result, query) {
  FS('trackEvent', {
    name: 'search_result_clicked',
    properties: {
      search_query: query,
      content_id: result.id,
      content_title: result.title,
      result_type: result.type,  // "title", "person", "genre"
      result_position: result.position
    }
  });
}
```

### Subscription / Paywall

```html
<!-- Subscription Page - Important conversion point -->
<div class="subscription-page">
  <!-- Plan selection - visible -->
  <div class="plans-section fs-unmask"
       data-fs-element="Plan Selection"
       data-fs-properties-schema='{"plan_displayed":"string"}'>
    <h1>Choose Your Plan</h1>
    <p>Watch on any device. Cancel anytime.</p>
    
    <div class="plan-toggle">
      <button class="active">Monthly</button>
      <button>Annual (Save 20%)</button>
    </div>
    
    <div class="plan-cards">
      <div class="plan-card" data-plan="basic">
        <h2>Basic</h2>
        <p class="price">$8.99<span>/month</span></p>
        <ul class="features">
          <li>✓ Unlimited movies & TV</li>
          <li>✓ Watch on 1 device</li>
          <li>✗ HD not available</li>
          <li>✗ No downloads</li>
        </ul>
        <button>Choose Basic</button>
      </div>
      
      <div class="plan-card featured" data-plan="standard">
        <span class="badge">Most Popular</span>
        <h2>Standard</h2>
        <p class="price">$13.99<span>/month</span></p>
        <ul class="features">
          <li>✓ Unlimited movies & TV</li>
          <li>✓ Watch on 2 devices</li>
          <li>✓ HD available</li>
          <li>✓ Download on 2 devices</li>
        </ul>
        <button>Choose Standard</button>
      </div>
      
      <div class="plan-card" data-plan="premium">
        <h2>Premium</h2>
        <p class="price">$19.99<span>/month</span></p>
        <ul class="features">
          <li>✓ Unlimited movies & TV</li>
          <li>✓ Watch on 4 devices</li>
          <li>✓ 4K + HDR available</li>
          <li>✓ Download on 6 devices</li>
        </ul>
        <button>Choose Premium</button>
      </div>
    </div>
  </div>
  
  <!-- Payment form -->
  <div class="payment-section">
    <h2 class="fs-unmask">Payment Details</h2>
    
    <!-- Payment method - visible -->
    <div class="payment-methods fs-unmask">
      <label>
        <input type="radio" name="payment" value="card" checked />
        Credit/Debit Card
      </label>
      <label>
        <input type="radio" name="payment" value="paypal" />
        PayPal
      </label>
      <label>
        <input type="radio" name="payment" value="giftcard" />
        Gift Card
      </label>
    </div>
    
    <!-- Card form - EXCLUDE -->
    <div class="card-form fs-exclude">
      <input type="text" name="cardNumber" placeholder="Card Number" />
      <input type="text" name="expiry" placeholder="MM/YY" />
      <input type="text" name="cvv" placeholder="CVV" />
    </div>
    
    <!-- Gift card - EXCLUDE (could be valuable code) -->
    <div class="giftcard-form fs-exclude">
      <input type="text" name="giftCardCode" placeholder="Gift Card Code" />
    </div>
    
    <!-- Terms - visible -->
    <div class="terms fs-unmask">
      <p>By clicking below, you agree to our Terms of Service and Privacy Policy.</p>
      <p>Your subscription will auto-renew monthly until cancelled.</p>
    </div>
    
    <!-- Submit - visible -->
    <button type="submit" class="subscribe-btn fs-unmask">
      Start Membership
    </button>
  </div>
</div>
```

```javascript
// Subscription tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'subscription',
    current_status: user.subscription.status,  // "free", "trial", "cancelled"
    referrer: subscriptionReferrer  // "paywall", "settings", "trial_end"
  }
});

function onPlanSelect(plan) {
  FS('trackEvent', {
    name: 'subscription_plan_selected',
    properties: {
      plan_name: plan.name,
      plan_price: plan.price,
      billing_cycle: billingCycle,
      is_upgrade: isUpgrade(currentPlan, plan)
    }
  });
}

function onSubscriptionComplete(subscription) {
  FS('trackEvent', {
    name: 'subscription_started',
    properties: {
      plan_name: subscription.plan,
      plan_price: subscription.price,
      billing_cycle: subscription.billingCycle,
      payment_method: subscription.paymentMethod,
      is_trial: subscription.isTrial,
      conversion_source: conversionSource,  // "paywall", "homepage_cta", "trial_end"
      
      // Journey info
      sessions_before_conversion: sessionsBeforeConversion,
      days_since_signup: daysSinceSignup,
      content_viewed_before_conversion: contentViewedCount
    }
  });
}

// Paywall tracking
function onPaywallShown(context) {
  FS('trackEvent', {
    name: 'paywall_shown',
    properties: {
      paywall_type: context.type,  // "hard", "soft", "trial_end"
      content_blocked: context.content?.title,
      trigger: context.trigger  // "content_limit", "feature_access", "trial_expired"
    }
  });
}

function onPaywallDismiss(context) {
  FS('trackEvent', {
    name: 'paywall_dismissed',
    properties: {
      paywall_type: context.type,
      dismiss_method: context.method  // "close_button", "back_navigation", "click_outside"
    }
  });
}
```

---

## News/Publishing Patterns

For news and publishing sites:

```javascript
// Article tracking
FS('setProperties', {
  type: 'page',
  properties: {
    page_type: 'article',
    article_id: article.id,
    article_title: article.title,
    article_category: article.category,
    article_author: article.author,
    publish_date: article.publishDate,
    word_count: article.wordCount,
    has_paywall: article.isPremium,
    is_premium_content: article.isPremium
  }
});

// Reading progress
function onReadingProgress(percent) {
  FS('trackEvent', {
    name: 'article_read_progress',
    properties: {
      article_id: article.id,
      progress_percent: percent,  // 25, 50, 75, 100
      read_time_seconds: readTime
    }
  });
}

// Metered paywall
function onArticleLimitReached() {
  FS('trackEvent', {
    name: 'article_limit_reached',
    properties: {
      articles_read_this_month: articlesRead,
      limit: articleLimit
    }
  });
}
```

---

## Ad-Supported Model Patterns

For ad-supported streaming/content:

```javascript
// Ad tracking (for your analytics, not ad tracking)
function onAdStart(ad) {
  FS('trackEvent', {
    name: 'ad_started',
    properties: {
      ad_position: ad.position,  // "pre_roll", "mid_roll", "post_roll"
      ad_duration_seconds: ad.duration,
      content_id: currentContent.id,
      content_timestamp: contentTimestamp,
      is_skippable: ad.skippable
    }
  });
}

function onAdSkipped(ad) {
  FS('trackEvent', {
    name: 'ad_skipped',
    properties: {
      ad_position: ad.position,
      seconds_watched_before_skip: watchedBeforeSkip,
      content_id: currentContent.id
    }
  });
}

function onAdCompleted(ad) {
  FS('trackEvent', {
    name: 'ad_completed',
    properties: {
      ad_position: ad.position,
      ad_duration_seconds: ad.duration,
      content_id: currentContent.id
    }
  });
}

// Upgrade prompt (for ad-supported to paid)
function onUpgradeToAdFreePrompt() {
  FS('trackEvent', {
    name: 'upgrade_prompt_shown',
    properties: {
      prompt_type: 'ad_free',
      trigger: 'ad_frequency',  // after X ads
      content_id: currentContent.id
    }
  });
}
```

---

## Churn Prevention Signals

```javascript
// Engagement signals for churn prediction
FS('setProperties', {
  type: 'user',
  properties: {
    // Activity metrics
    days_since_last_watch: daysSinceLastWatch,
    watch_frequency: getWatchFrequency(),  // "daily", "weekly", "monthly", "rare"
    hours_watched_7d: hoursWatched7d,
    hours_watched_30d: hoursWatched30d,
    
    // Content engagement
    titles_started_30d: titlesStarted,
    titles_completed_30d: titlesCompleted,
    completion_rate: titlesCompleted / titlesStarted,
    
    // Feature usage
    uses_downloads: hasDownloads,
    uses_profiles: profilesCount > 1,
    uses_my_list: myListCount > 0,
    
    // Subscription health
    payment_failures_90d: paymentFailures,
    contacted_support_30d: contactedSupport
  }
});

// Cancellation flow tracking
function onCancellationInitiated(reason) {
  FS('trackEvent', {
    name: 'cancellation_initiated',
    properties: {
      cancellation_reason: reason,  // "price", "not_using", "content", "switching"
      subscription_tenure_days: tenureDays,
      last_watch_days_ago: daysSinceLastWatch
    }
  });
}

function onCancellationCompleted() {
  FS('trackEvent', {
    name: 'cancellation_completed',
    properties: {
      save_offer_shown: saveOfferShown,
      save_offer_accepted: saveOfferAccepted
    }
  });
}

function onCancellationSaved(offer) {
  FS('trackEvent', {
    name: 'cancellation_saved',
    properties: {
      save_offer_type: offer.type,  // "discount", "pause", "downgrade"
      offer_value: offer.value
    }
  });
}
```

---

## KEY TAKEAWAYS FOR AGENT

When helping media clients with Fullstory:

1. **Content engagement is core**: Track views, progress, completions, interactions
2. **Subscription conversion is critical**: Track full funnel from browse to paid
3. **Video player interactions are valuable**: Skip, seek, quality, subtitles
4. **COPPA compliance**: Never track children's profiles
5. **Payment details excluded**: Standard PCI compliance
6. **Recommendations tracking**: Understand what drives content discovery

### Questions to Ask Media Clients

1. "Do you have children's profiles that need special handling?"
2. "Are you tracking video playback events comprehensively?"
3. "How are you measuring subscription conversion funnel?"
4. "Do you have ad-supported tiers to track?"
5. "How do you define 'engagement' for churn prediction?"

### Key Metrics to Track

- Browse-to-play conversion
- Content completion rates
- Time to first play (onboarding)
- Subscription conversion rate
- Trial-to-paid conversion
- Churn indicators (declining watch time)
- Recommendation effectiveness

---

## REFERENCE LINKS

- **COPPA Compliance**: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- **Fullstory Analytics Events**: ../core/fullstory-analytics-events/SKILL.md
- **User Properties**: ../core/fullstory-user-properties/SKILL.md
- **Privacy Controls**: ../core/fullstory-privacy-controls/SKILL.md

---

*This skill document is specific to media and entertainment implementations. Ensure COPPA compliance if serving children.*

