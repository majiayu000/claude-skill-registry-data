---
name: picnic
description: Add groceries to Picnic shopping cart via voice/text commands.
homepage: https://picnic.app
metadata: {"clawdis":{"emoji":"🛒","requires":{"env":["PICNIC_EMAIL","PICNIC_PASSWORD"]},"primaryEnv":"PICNIC_EMAIL"}}
---

# Picnic Grocery Skill

Manage your Picnic grocery shopping cart via CLI.

## Setup

1. Set `PICNIC_EMAIL` and `PICNIC_PASSWORD` in config
2. Run `npm install` in the skill directory

## Commands

### Search for products
```bash
node {baseDir}/scripts/picnic.js search "milch"
```

### Add product to cart
```bash
node {baseDir}/scripts/picnic.js add PRODUCT_ID [count]
```

### View cart
```bash
node {baseDir}/scripts/picnic.js cart
```

### Remove from cart
```bash
node {baseDir}/scripts/picnic.js remove PRODUCT_ID [count]
```

### Clear cart
```bash
node {baseDir}/scripts/picnic.js clear
```

## Workflow

1. Search for product → get product IDs
2. Add desired product by ID
3. View cart to confirm

## Notes

- Country: DE (Germany)
- Credentials stored in clawdis config
- Auth token cached in ~/.picnic-auth
