---
name: smart-crm
description: AI-driven customer relationship management. Analyzes user base, segments customers, and provides engagement insights based on WordPress user data.
tools_required: [wp_users]
always_on: false
group: marketing
order: 1
suggests: [email-marketer]
---

# Smart CRM

Smart CRM turns your WordPress user database into actionable marketing insights. It analyzes user behavior, roles, and engagement to help you understand your audience.

## Capabilities

1.  **User Segmentation**: Group users by role, registration date, or activity level.
2.  **Engagement Analysis**: Identify top contributors (by post count) or dormant users.
3.  **Growth Metrics**: Analyze registration trends over time.

## Workflows

### 1. Audience Overview
**Trigger**: "Analyze my user base" or "Who are my users?"

**Steps**:
1.  **Fetch**: Call `wp_users` with `action='list'` and `limit=100`.
2.  **Analyze**:
    *   Breakdown by Role (Admin, Editor, Subscriber).
    *   Calculate Active vs. Inactive (based on post count or recent registration).
    *   Identify "Power Users".
3.  **Report**: Summarize findings and suggest actions (e.g., "Email your 50 subscribers," "Promote your top 3 authors").

### 2. Segment Creation
**Trigger**: "Find all subscribers who joined this year"

**Steps**:
1.  **Search**: Call `wp_users` (may need to iterate user list if advanced date filtering isn't in search).
2.  **Filter**: Apply logic (e.g., `registered > 2024-01-01`).
3.  **List**: Return names/emails of matching users.

### 3. VIP Identification
**Trigger**: "Who are my top contributors?"

**Steps**:
1.  **Fetch**: Loop through users with `wp_users`.
2.  **Sort**: Order by `posts_count` descending.
3.  **Highlight**: List top 5 users with their stats.

## Future Integrations
*   **WooCommerce**: If enabled, analyze `orders_count` and `total_spend`.
*   **Email Marketing**: Export segments to CSV/Mailchimp.

## Tool Usage

```javascript
// Example: Get top 50 users to analyze
const result = wp_users({ action: 'list', limit: 50 });
const users = result.users;

// AI Logic:
// 1. Count roles
// 2. Find registration trends
// 3. Output markdown report
```
