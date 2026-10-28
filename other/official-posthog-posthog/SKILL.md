---
name: posthog
description: PostHog analytics integration and usage skill. Use when working with PostHog product analytics, feature flags, session recordings, A/B testing, or any PostHog SDK integration.
---

# PostHog Skill

PostHog is an open-source product analytics platform. This skill covers integrating and using PostHog in your applications.

## Documentation

Always refer to the official PostHog documentation for the most up-to-date information:
- https://posthog.com/docs

## Key Features

- **Product Analytics**: Track events, user behavior, funnels, retention
- **Feature Flags**: Roll out features gradually, A/B test
- **Session Recordings**: Watch user sessions to understand behavior
- **Experiments**: Run A/B tests with statistical significance
- **Surveys**: Collect user feedback in-app

## Quick Start

### JavaScript/TypeScript

```javascript
import posthog from 'posthog-js'

posthog.init('<ph_project_api_key>', {
  api_host: 'https://us.i.posthog.com',
  person_profiles: 'identified_only'
})
```

### Node.js

```javascript
import { PostHog } from 'posthog-node'

const client = new PostHog('<ph_project_api_key>', {
  host: 'https://us.i.posthog.com'
})

client.capture({
  distinctId: 'user-id',
  event: 'event-name',
  properties: { key: 'value' }
})
```

## Feature Flags

```javascript
const isEnabled = await posthog.isFeatureEnabled('my-flag', 'user-id')
```

## Best Practices

- Always call `posthog.shutdown()` in Node.js before process exit
- Use `identify()` to associate events with users
- Use `group()` for B2B analytics
- Capture meaningful events, not just page views
