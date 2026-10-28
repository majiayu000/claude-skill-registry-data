---
name: wix-manage
description: "Wix business solution management recipes — REST API operations for configuring and managing Wix business solutions. Routes to: stores, bookings, get-paid, CMS, contacts, events, forms, media, app-installation, pricing-plans, restaurants, rich-content, sites, blog, calendar, domains, site-properties, ecommerce."
compatibility: Requires Wix REST API access (API key or OAuth).
---

# Management Recipes Index

## What Are Management Recipes?

**Management recipes are for REST API operations** that configure, set up, and manage Wix business entities on your site. These recipes use REST API calls and are designed for:

- **Site setup and configuration** — Initial setup of stores, bookings, payments, and other business apps
- **Entity management** — Creating, updating, and deleting products, services, staff members, pricing plans
- **Administrative operations** — Bulk updates, contact labeling, data migrations
- **Backend integrations** — Server-to-server automations, webhooks, data synchronization

These recipes do NOT cover frontend development or SDK usage for displaying data to users.

---

## App Installation

### Install Wix Apps (`references/app-installation/install_wix_apps.md`)
**Technical:** Installs Wix apps on a site using Apps Installer API. Covers enabling Velo (Wix Code), app installation, and common app definition IDs.

### List Installed Apps (`references/app-installation/list_installed_apps.md`)
**Technical:** Lists all apps installed on a site using Apps Installer API. Useful for verifying app installations before making API calls and diagnosing authorization errors.

---

## Blog

### How to Create Blog Posts (`references/blog/how_to_create_blog_posts.md`)
**Technical:** Creates and publishes blog posts using Blog Posts API. Covers Ricos rich content format, image upload via Media Manager, category/tag assignment, and bulk post creation.

---

## Bookings

### Booking Service Policy Setup (`references/bookings/booking_service_policy_setup.md`)
**Technical:** Sets up booking policies, cancellation rules, and waitlist configuration using the Services API policy fields. Covers bookingPolicy, cancellationPolicy, and waitlist settings.

### Booking System Integration Gaps (`references/bookings/booking_system_integration_gaps.md`)
**Technical:** Documents undocumented API patterns for booking payments. Covers Bookings→Ecommerce integration, booking ID transformation to catalog items, and async payment confirmation flows.

### Bookings Staff Setup (`references/bookings/bookings_staff_setup.md`)
**Technical:** Creates staff members and configures custom working hours using Staff API + Calendar Events API. Critical two-step process: create staff → assign schedule → create working hours events.

### Create and Update Booking Services (`references/bookings/create_and_update_booking_services.md`)
**Technical:** Full CRUD operations for Wix Bookings services using Services API. Covers service types (APPOINTMENT, CLASS, COURSE), pricing configuration, location setup, and schedule management.

### End-to-End Booking Flow (`references/bookings/end_to_end_booking_flow.md`)
**Technical:** Complete booking flow from service discovery to payment. Query services, check availability with Time Slots V2, create bookings, and process payment via eCommerce checkout.

### External Calendar Integration (`references/bookings/external_calendar_integration.md`)
**Technical:** OAuth-based integration with Google Calendar, Microsoft Outlook, and Apple Calendar. Covers authentication flows, sync configuration, and bidirectional event management.

### Multi-Resource Service Creation (`references/bookings/multi_resource_service_creation.md`)
**Technical:** Creates resource types and individual resources using Resources API. Enables services that require multiple resources (rooms + equipment + staff) with automatic allocation.

---

## Calendar

### Configure Default Business Hours (`references/calendar/configure_default_business_hours.md`)
**Technical:** Uses Calendar Events API to create WORKING_HOURS events on the business schedule. Covers the critical distinction between Calendar Events API (correct) vs Site Properties API (incorrect) for setting base availability.

---

## CMS

### CMS Data Items CRUD (`references/cms/cms_data_items_crud.md`)
**Technical:** Add, query, update, and delete items in CMS collections. Use this to insert content, bulk insert/update/patch/delete items, query with filters, and manage collection data. Key endpoints: /wix-data/v2/items, /wix-data/v2/bulk/items/*.

### CMS Data Operations Extended (`references/cms/cms_data_operations_extended.md`)
**Technical:** Additional CMS data operations including count, upsert (bulk save), and update by filter patterns.

### CMS eCommerce Catalog Integration (`references/cms/cms_ecommerce_catalog_integration.md`)
**Technical:** The recommended way to sell existing CMS collection items (tickets, bookings, memberships) through Wix checkout. Add the CATALOG plugin to convert any CMS collection into purchasable products with cart and payment integration.

### CMS References & Relationships (`references/cms/cms_references_and_relationships.md`)
**Technical:** Add, replace, or remove items from MULTI_REFERENCE fields. Use insert-references, replace-references, remove-references endpoints. Required for managing multi-reference relationships - these CANNOT be set via regular insert/update/patch operations. Also covers single references and querying with expanded references.

### CMS Schema Management (`references/cms/cms_schema_management.md`)
**Technical:** Create and modify CMS collection structures. Covers listing collections, creating collections with fields, adding/removing fields, and updating collection settings.

---

## Contacts

### Bulk Delete Contacts (`references/contacts/bulk_delete_contacts.md`)
**Technical:** Deletes multiple contacts using filter-based bulk delete. Covers safe deletion patterns, GDPR compliance, soft delete alternatives, and batch processing strategies.

### Bulk Label and Unlabel Contacts (`references/contacts/bulk_label_and_unlabel_contacts.md`)
**Technical:** Adds/removes labels from multiple contacts using Contacts API bulk operations. Covers label creation, contact filtering, batch processing, and rate limit handling.

---

## Domains

### Domain Search and Purchase (`references/domains/domain_search_and_purchase.md`)
**Technical:** Search for available domains, get domain suggestions, and generate purchase links using Domain Search V2 API. Covers availability checks, TLD filtering, and connecting domains to Wix sites.

---

## eCommerce

### Setup Store Pickup Location (`references/ecommerce/setup_store_pickup_location.md`)
**Technical:** Configures a pickup option for an online store so customers can choose in-store pickup at checkout. Uses the Delivery Profiles API to discover the Pickup carrier, add a delivery region, and attach the carrier with a free pickup rate.

---

## Events

### List Events (`references/events/list_events.md`)
**Technical:** Queries events from Wix Events using Events API. Covers field sets (DETAILS, URLS, REGISTRATION), filtering by status/date, and pagination.

---

## Forms

### Create Form (`references/forms/create_form.md`)
**Technical:** Creates a form with fields (name, email, etc.) using the Form Schemas API. Covers field configuration, layout, and post-submission triggers.

---

## Get Paid

### Create Payment Links (`references/get-paid/create_payment_links.md`)
**Technical:** Creates payment links for collecting payments without a checkout flow. Covers store products (catalog items), custom line items, variants, due dates, and sending links via email.

### How to Setup Wix Payments (`references/get-paid/how_to_setup_wix_payments.md`)
**Technical:** Configures Wix Payments as the payment provider. Covers eligibility checking, business verification, bank account setup, and payment method configuration (cards, PayPal, Apple Pay).

### Payment Links for Bookings (`references/get-paid/payment_links_for_bookings.md`)
**Technical:** Creates payment links for unpaid bookings using Payment Links API. Links booking IDs to payment requests with proper redirect handling.

---

## Media

### Upload Media to Wix (`references/media/upload_media_to_wix.md`)
**Technical:** Uploads images and files to the Wix Media Manager using the Import File API. Covers importing from external URLs, checking file status, and using the returned wixstatic.com URL in other APIs.

---

## Pricing Plans

### Create and Update Pricing Plans (`references/pricing-plans/create_and_update_pricing_plans.md`)
**Technical:** Creates subscription and one-time payment plans using Plans API. Covers pricing models (recurring, one-time, free), trial periods, perks configuration, and plan visibility.

### Pricing Plans Bookings Integration (`references/pricing-plans/pricing_plans_bookings_integration.md`)
**Technical:** Links Pricing Plans to Bookings services using the Benefit Programs API. Enables package deals and memberships that grant booking access.

---

## Restaurants

### Wix Restaurants Setup (`references/restaurants/wix_restaurants_setup.md`)
**Technical:** Configures restaurant menus, sections, and items using Menus API. Covers menu structure (Menu → Section → Item), modifiers, pricing, availability schedules, and ordering settings.

---

## Rich Content

### Ricos Converter Service (`references/rich-content/ricos_converter_service.md`)
**Technical:** Validates and converts content between Ricos documents and HTML/Markdown/plain text using the Ricos Documents API. Covers plugin configuration, format conversion in both directions, and document validation.

---

## Site Properties

### Change Payment Currency (`references/site-properties/change_payment_currency_site_properties.md`)
**Technical:** Updates the site-level payment currency (store billing currency) using Site Properties API, including the required request body shape and field mask.

---

## Sites

### Create Site from Template (`references/sites/create_site_from_template.md`)
**Technical:** Creates new Wix sites from templates using account-level APIs. Covers template search, site creation, headless site setup, OAuth app creation, and publishing.

### Query Sites (`references/sites/query_sites.md`)
**Technical:** Lists and queries all sites associated with a Wix account using Sites API. Covers pagination with cursor-based navigation.

---

## Stores

### Add Store Pages to Site (`references/stores/add_store_pages_to_site.md`)
**Technical:** Adds missing checkout and cart pages to a site when Stores app is installed. Used when store pages are missing after migration or setup issues.

### Bulk Create Products with Options (`references/stores/bulk_create_products_with_options.md`)
**Technical:** Uses bulk products endpoint to create multiple products with inventory in a single request. Handles variant generation from options, media format requirements, and error handling for partial failures.

### Create Product (Catalog V1) (`references/stores/create_product_catalog_v1.md`)
**Technical:** Create products using the Catalog V1 Products API. Use this recipe when the site's catalog version is CATALOG_V1. Covers simple product creation, product with options, and key V1 request structure differences from V3.

### Create Product with Options (Catalog V3) (`references/stores/create_product_with_options_catalog_v3.md`)
**Technical:** Single product creation with options using Catalog V3 Products API. Covers option types (TEXT_CHOICES, SWATCH_CHOICES), choice configuration, and automatic variant generation.

### Query Products (`references/stores/query_products.md`)
**Technical:** Query and list products from a Wix Store using Catalog V3 Query Products endpoint. Covers correct fields enum values, filtering, sorting, and paging.

### Query Products (Catalog V1) (`references/stores/query_products_catalog_v1.md`)
**Technical:** Query and list products from a Wix Store using the Catalog V1 Query Products endpoint. Use this recipe when the site's catalog version is CATALOG_V1. Covers basic queries, filtering, sorting, and paging.

### Setup Online Store (Catalog V3) (`references/stores/setup_online_store_catalog_v3.md`)
**Technical:** Initializes a Stores catalog with Catalog V3 Products API, bulk products endpoint, and Categories API. Covers product creation, option configuration, variant management, and category assignment.

### Update Product Pre-Order (`references/stores/update_product_pre_order.md`)
**Technical:** Manages pre-order settings for product variants using V3 Inventory API. Covers enabling/disabling pre-orders, setting messages, configuring limits, and handling trackQuantity requirements.

### Update Product with Options (`references/stores/update_product_with_options.md`)
**Technical:** Modifies existing products and variants using Catalog V3 Products API. Covers adding/removing option choices, variant-specific pricing, and revision-based updates to prevent conflicts.
