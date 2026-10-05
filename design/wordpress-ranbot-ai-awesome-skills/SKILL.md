---
name: wordpress
description: Complete WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security hardening. 
category: Security & Systems
source: antigravity
tags: [react, api, ai, automation, workflow, template, design, image, security, tailwind]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/wordpress
---


# WordPress Development Workflow Bundle

## Overview

Comprehensive WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security. This bundle orchestrates skills for building production-ready WordPress sites and applications.

## When to Use This Workflow

Use this workflow when:
- Building new WordPress websites
- Creating custom themes
- Developing WordPress plugins
- Setting up WooCommerce stores
- Optimizing WordPress performance
- Hardening WordPress security

## Workflow Phases

### Phase 1: WordPress Setup

#### Skills to Invoke
- `app-builder` - Project scaffolding
- `environment-setup-guide` - Development environment

#### Actions
1. Set up local development environment (LocalWP, Docker, or Valet)
2. Install WordPress
3. Configure development database
4. Set up version control
5. Configure wp-config.php for development

#### Copy-Paste Prompts
```
Use @app-builder to scaffold a new WordPress project with modern tooling
```

### Phase 2: Theme Development

#### Skills to Invoke
- `frontend-developer` - Component development
- `frontend-design` - UI implementation
- `tailwind-patterns` - Styling
- `web-performance-optimization` - Performance

#### Actions
1. Design theme architecture
2. Create theme files (style.css, functions.php, index.php)
3. Implement template hierarchy
4. Create custom page templates
5. Add custom post types and taxonomies
6. Implement theme customization options
7. Add responsive design

#### Theme Structure
```
theme-name/
├── style.css
├── functions.php
├── index.php
├── header.php
├── footer.php
├── sidebar.php
├── single.php
├── page.php
├── archive.php
├── search.php
├── 404.php
├── template-parts/
├── inc/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

#### Copy-Paste Prompts
```
Use @frontend-developer to create a custom WordPress theme with React components
```

```
Use @tailwind-patterns to style WordPress theme with modern CSS
```

### Phase 3: Plugin Development

#### Skills to Invoke
- `backend-dev-guidelines` - Backend standards
- `api-design-principles` - API design
- `auth-implementation-patterns` - Authentication

#### Actions
1. Design plugin architecture
2. Create plugin boilerplate
3. Implement hooks (actions and filters)
4. Create admin interfaces
5. Add custom database tables
6. Implement REST API endpoints
7. Add settings and options pages

#### Plugin Structure
```
plugin-name/
├── plugin-name.php
├── includes/
│   ├── class-plugin-activator.php
│   ├── class-plugin-deactivator.php
│   ├── class-plugin-loader.php
│   └── class-plugin.php
├── admin/
│   ├── class-plugin-admin.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-plugin-public.php
│   ├── css/
│   └── js/
└── languages/
```

#### Copy-Paste Prompts
```
Use @backend-dev-guidelines to create a WordPress plugin with proper architecture
```

### Phase 4: WooCommerce Integration

#### Skills to Invoke
- `payment-integration` - Payment processing
- `stripe-integration` - Stripe payments
- `billing-automation` - Billing workflows

#### Actions
1. Install and configure WooCommerce
2. Create custom product types
3. Customize checkout flow
4. Integrate payment gateways
5. Set up shipping methods
6. Create custom order statuses
7. Implement subscription products
8. Add custom email templates

#### Copy-Paste Prompts
```
Use @payment-integration to set up WooCommerce with Stripe
```

```
Use @billing-automation to create subscription products in WooCommerce
```

### Phase 5: Performance Optimization

#### Skills to Invoke
- `web-performance-optimization` - Performance optimization
- `database-optimizer` - Database optimization

#### Actions
1. Implement caching (object, page, browser)
2. Optimize images (lazy loading, WebP)
3. Minify and combine assets
4. Enable CDN
5. Optimize database queries
6. Implement lazy loading
7. Configure OPcache
8. Set up Redis/Memcached

#### Performance Checklist
- [ ] Page load time < 3 seconds
- [ ] Time to First Byte < 200ms
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1
- [ ] First Input Delay < 100ms

#### Copy-Paste Prompts
```
Use @web-performance-optimization to audit and improve WordPress performance
```

### Phase 6: Security Hardening

#### Skills to Invoke
- `security-auditor` - Security audit
- `wordpress-penetration-testing` - WordPress security testing
- `sast-configuration` - Static analysis

#### Actions
1. Update WordPress core, themes, plugins
2. Implement security headers
3. Configure file permissions
4. Set up firewall rules
5. Enable two-factor authentication
6. Implement rate limiting
7. Configure security logging
8. Set up malware scanning

#### Security Checklist
- [ ] WordPress core updated
- [ ] All plugins/themes updated
- [ ] Strong passwords enforced
- [ ] Two-factor authentication enabled
- [ ] Security headers configured
- [ ] XML-RPC disabled or protected
- [ ] File editing disabled
- [ ] Database prefix cha
