---
name: Kroger CLI Reference
description: Complete reference guide for using the Kroger CLI to search products, manage your cart, and automate grocery shopping at King Sooppers. Use this when you need to understand Kroger CLI commands, syntax, best practices for product selection, or troubleshoot Kroger operations.
---

## Instructions

This skill provides comprehensive documentation for the Kroger CLI tool, which enables command-line automation of grocery shopping at King Sooppers (a Kroger store).

Use this skill when you need to:
- Understand how to use Kroger CLI commands
- Reference product search and cart management syntax
- Learn best practices for product selection
- Troubleshoot authentication or store issues
- Get examples of common operations

## Overview

The Kroger CLI is a command-line tool for interacting with King Sooppers for automated shopping. It provides authentication, product search, and cart management capabilities.

## Getting Started

### Prerequisites
- The `kroger` command is available in `$PATH` and executable directly
- Kroger account with API authentication configured

### Authentication & Sessions
```bash
kroger auth          # Check current API authentication status
kroger login         # Login to your Kroger account (use if auth fails)
kroger logout        # Logout from your account
```

**Important Notes:**
- Assume `kroger auth` is already valid before starting operations
- If authentication fails, run `kroger login` and wait for the response
- Authentication persists across sessions

## Store Management

### Available Commands
```bash
kroger store show     # Show currently selected store
kroger store set [ID] # Set your default store
kroger stores [ZIP]   # Search for stores by ZIP code
```

**Assumptions:**
- The store is already set; no need to reconfigure unless switching locations
- All operations default to the currently set store

## Product Operations

### Search & Discovery
```bash
kroger products "search term"     # Search for products by name/type
kroger product [ID/UPC]           # Get detailed info on a specific product
```

**Examples:**
```bash
kroger products "organic milk"
kroger products "chicken breast"
kroger product 0001111041700      # Get details for a specific UPC
```

### Product Selection Guidelines

When searching for products, consider:

1. **Brand Preferences**
   - Follow explicit preferences when available

2. **Default Selection Strategy**
   - Prefer **midrange brands on sale** when no specific preference exists
   - Look for good value relative to quality

3. **Quantity & Size Matching**
   - Carefully match product quantity and size to the meal plan
   - Consider expected usage patterns for the week
   - Account for storage capacity and product shelf life

## Cart Operations

### Add to Cart
```bash
kroger cart add [UPC]              # Add item to cart (single unit)
kroger cart add [UPC] -q 2         # Add item with specific quantity
```

**Examples:**
```bash
kroger cart add 0001111041700
kroger cart add 0001111041700 -q 2
```

**Requirements:**
- Cart operations require valid login (`kroger auth` must pass)
- Assume cart starts empty (API doesn't allow checking existing items)

## Tips & Best Practices

1. **Search Thoroughly** - Try multiple search terms if needed to find alternatives
2. **Check Details** - Use `kroger product [UPC]` to verify prices, sizes, and ratings before adding
3. **Batch Operations** - Add multiple items in sequence for efficiency
4. **Quantity Planning** - Use `-q` flag to add multiple units of the same product in one command
5. **Sales & Deals** - Look for sale prices when no brand preference is specified

## Troubleshooting

- **Auth Failed**: Run `kroger login` and complete the login flow
- **Product Not Found**: Try alternative search terms or check spelling
- **Store Issues**: Verify store is set with `kroger store show`

## More Help
```bash
kroger [command] --help    # Get detailed help for any command
```
