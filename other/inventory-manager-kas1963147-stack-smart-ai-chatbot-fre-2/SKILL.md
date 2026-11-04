---
name: inventory-manager
description: Manage WooCommerce product inventory. Track stock levels, set alerts, manage backorders, and optimize inventory turnover.
tools_required: [woo_product_manage, woo_product_details, woo_search_products, woo_variations, woo_reports, email]
always_on: false
group: woocommerce
order: 9
suggests: [product-description-writer, order-management]
---

# Inventory Manager

Complete WooCommerce inventory and stock management.

## When to Use This Skill

- Tracking stock levels
- Setting low stock alerts
- Managing backorders
- Updating inventory
- Analyzing inventory performance
- Forecasting stock needs

## Core Capabilities

### Stock Tracking
- View stock levels with `woo_product_details`
- Search inventory with `woo_search_products`
- Track variation stock with `woo_variations`
- Monitor stock status

### Stock Management
- Update quantities with `woo_product_manage`
- Set stock status
- Configure backorders
- Manage reservations

### Reporting
- Stock reports with `woo_reports`
- Low stock alerts via `email`
- Inventory valuation
- Turnover analysis

## Stock Status Types

| Status | Meaning | Display |
|--------|---------|---------|
| In Stock | Available | Add to Cart |
| Out of Stock | None available | Sold Out |
| On Backorder | Available to order | Backorder |
| Low Stock | Below threshold | Limited Stock |

## Inventory Settings

### Per Product
```yaml
Stock Management: Enabled
Stock Quantity: 50
Low Stock Threshold: 10
Allow Backorders: No
Stock Status: In Stock
```

### Variations
```yaml
Parent Product: T-Shirt
Variations:
  - Small/Red: 25 units
  - Small/Blue: 30 units
  - Medium/Red: 0 units (Out of Stock)
  - Medium/Blue: 15 units
  - Large/Red: 20 units
  - Large/Blue: 10 units
```

## Workflow

### Daily Stock Check

1. **Review Alerts**
   - Check low stock notifications
   - Review out of stock items
   - Note backorder requests

2. **Update Stock**
   - Enter received inventory
   - Adjust for damages/returns
   - Sync with external systems

3. **Reorder Planning**
   - Identify items needing reorder
   - Calculate reorder quantity
   - Place supplier orders

### Stock Receiving

1. **Receive Shipment**
   - Verify against PO
   - Count items
   - Note discrepancies

2. **Update Inventory**
   - Add quantities with `woo_product_manage`
   - Update costs if changed
   - Document receipt

3. **Verify**
   - Confirm stock display correctly
   - Check variation levels
   - Test purchase flow

### Inventory Audit

1. **Physical Count**
   - Select products to audit
   - Count physical inventory
   - Compare to system

2. **Reconcile**
   - Document discrepancies
   - Investigate variances
   - Adjust system

3. **Report**
   - Shrinkage calculation
   - Accuracy percentage
   - Improvement actions

## Low Stock Alerts

### Alert Configuration
```yaml
Low Stock Threshold: 10 units
Out of Stock Threshold: 0 units
Notify: admin@store.com
Frequency: Immediate
```

### Alert Email Template
```
Subject: Low Stock Alert - [Product Name]

[Product Name] is running low!

Current Stock: [quantity]
Threshold: [threshold]
Recent Sales: [last 7 days]

View Product: [link]
Reorder Now: [supplier link]
```

## Backorder Management

### Backorder Settings
- **Do not allow**: Stop sales when out
- **Allow, notify customer**: Accept orders, inform
- **Allow**: Accept silently

### Backorder Workflow
1. Customer orders backordered item
2. Customer notified of backorder
3. Stock received
4. Backorder fulfilled
5. Customer notified of shipment

## Inventory Metrics

### Stock Metrics
| Metric | Calculation | Target |
|--------|-------------|--------|
| Stock Turnover | COGS / Avg Inventory | 4-6x/year |
| Days on Hand | Inventory / Daily Sales | 30-60 days |
| Stockout Rate | Stockouts / Total SKUs | <5% |
| Accuracy | Correct / Total Audited | 99%+ |

### Valuation
- **FIFO**: First In, First Out
- **LIFO**: Last In, First Out
- **WAC**: Weighted Average Cost

## Best Practices

1. **Real-time updates** - Sync immediately
2. **Safety stock** - Buffer for demand spikes
3. **ABC analysis** - Focus on high-value items
4. **Regular audits** - Monthly or quarterly
5. **Forecast demand** - Use historical data
6. **Supplier relationships** - Reliable reordering
7. **Document everything** - Audit trail

## Reorder Point Formula

```
Reorder Point = (Average Daily Sales × Lead Time) + Safety Stock

Example:
- Daily sales: 5 units
- Lead time: 7 days
- Safety stock: 10 units
- Reorder at: (5 × 7) + 10 = 45 units
```

## Economic Order Quantity

```
EOQ = √(2DS / H)

Where:
D = Annual demand
S = Order cost
H = Holding cost per unit

Example:
D = 1,000 units/year
S = $50 per order
H = $5 per unit/year
EOQ = √(2 × 1000 × 50 / 5) = 141 units
```

## Troubleshooting

### Stock Shows Wrong
- Check variation vs parent
- Verify recent orders processed
- Look for sync issues
- Run inventory sync

### Oversold
- Immediately notify customer
- Check for concurrent orders
- Enable stock reservation
- Review inventory buffer

### Sync Issues
- Check integration logs
- Verify API connections
- Manual reconciliation
- Contact support if needed
