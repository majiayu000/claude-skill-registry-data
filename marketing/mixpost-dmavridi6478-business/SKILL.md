---
name: mixpost
description: Self-hosted social media management platform — schedule, publish, and analyze posts across Twitter/X, Facebook, LinkedIn, Instagram, Pinterest, Mastodon, and Bluesky from one dashboard. PHP/Laravel backend with Vue.js frontend. Use when the project needs an owned alternative to Buffer or Hootsuite with no per-seat SaaS fees.
---

# Mixpost — Self-Hosted Social Media Management

A complete self-hosted social media scheduling and analytics platform built with PHP/Laravel.

## What it replaces

SaaS tools like Buffer, Hootsuite, Later, or Sprout Social — with full data ownership, no per-seat pricing, and white-label capability.

## Key capabilities

- **Multi-platform publishing**: Twitter/X, Facebook Pages & Groups, LinkedIn Personal & Company, Instagram, Pinterest, Mastodon, Bluesky
- **Content calendar**: Visual drag-and-drop scheduling with queue management
- **Media library**: Upload and reuse images/videos across posts
- **Analytics**: Engagement metrics per post and platform
- **Teams**: Multi-workspace support with role-based permissions
- **Webhooks**: Hook into post lifecycle events

## When to reach for it

- You need social scheduling without a recurring SaaS subscription
- GDPR or data-residency requirements prevent cloud SaaS
- You're building a white-label marketing platform for clients
- You want to extend scheduling logic with custom Laravel code

## Stack

PHP 8.1+ · Laravel · Vue 3 · Inertia.js · MySQL/PostgreSQL · Redis (for queues)

## Clone

```bash
git clone https://github.com/inovector/mixpost
```

## Self-host quickstart

```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan db:seed
npm install && npm run build
```

Requires Redis for queue processing of scheduled posts.
