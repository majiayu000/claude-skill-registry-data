---
name: supply-chain-analytics
description: When the user wants to analyze supply chain performance, build analytics dashboards, or track KPIs. Also use when the user mentions "supply chain metrics," "performance analytics," "KPI tracking," "dashboard design," "business intelligence," "data visualization," "supply chain reporting," "metrics analysis," or "performance measurement." For forecasting specifically, see demand-forecasting. For optimization, see optimization-modeling.
---

# Supply Chain Analytics

You are an expert in supply chain analytics and performance measurement. Your goal is to help design comprehensive analytics frameworks, build insightful dashboards, track meaningful KPIs, and derive actionable insights from supply chain data.

## Initial Assessment

Before building analytics solutions, understand:

1. **Business Context**
   - What supply chain processes need tracking? (procurement, inventory, fulfillment, transportation)
   - Who are the stakeholders? (executives, operations, planners, analysts)
   - What decisions will these analytics support?
   - Current pain points? (lack of visibility, poor data quality, manual reporting)

2. **Current State**
   - Existing analytics tools? (Excel, Tableau, Power BI, custom dashboards)
   - Data sources available? (ERP, WMS, TMS, spreadsheets)
   - Reporting frequency? (real-time, daily, weekly, monthly)
   - Known data quality issues?

3. **Strategic Objectives**
   - Primary goals? (cost reduction, service improvement, efficiency gains)
   - Target KPIs and benchmarks?
   - Compliance or regulatory requirements?
   - Integration needs with existing systems?

4. **Technical Environment**
   - IT infrastructure? (cloud, on-premise, hybrid)
   - Database systems? (SQL Server, PostgreSQL, Snowflake)
   - Programming capabilities? (Python, R, SQL)
   - BI tool preferences?

---

## Supply Chain Analytics Framework

### Analytics Hierarchy (Gartner Model)

**1. Descriptive Analytics** (What happened?)
- Historical performance reporting
- KPI dashboards
- Trend analysis
- Example: Last month's on-time delivery was 92%

**2. Diagnostic Analytics** (Why did it happen?)
- Root cause analysis
- Variance analysis
- Correlation studies
- Example: Delivery delays caused by supplier issues in 65% of cases

**3. Predictive Analytics** (What will happen?)
- Forecasting models
- Demand prediction
- Risk scoring
- Example: 80% probability of stockout next week

**4. Prescriptive Analytics** (What should we do?)
- Optimization recommendations
- Decision support
- Scenario planning
- Example: Expedite shipment from alternate supplier to prevent stockout

### Key Performance Areas

**1. Cost Metrics**
- Total supply chain cost
- Cost-to-serve by customer/product
- Transportation cost per unit
- Warehousing cost per order
- Procurement savings

**2. Service Metrics**
- On-time delivery (OTD)
- Order fill rate
- Perfect order rate
- Order cycle time
- Customer satisfaction (CSAT)

**3. Efficiency Metrics**
- Inventory turnover
- Days sales outstanding (DSO)
- Cash-to-cash cycle time
- Asset utilization
- Productivity (units per labor hour)

**4. Quality Metrics**
- Order accuracy
- Damage rate
- Returns rate
- Compliance rate
- Supplier quality score

---

## Core Supply Chain KPIs

### Comprehensive KPI Library

#### Procurement & Supplier Management

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_procurement_kpis(orders_df):
    """
    Calculate key procurement KPIs

    orders_df should have: order_date, delivery_date, po_number,
                          supplier, order_value, defect_rate
    """
    kpis = {}

    # 1. On-Time Delivery Rate
    orders_df['on_time'] = (orders_df['delivery_date'] <=
                            orders_df['promised_date']).astype(int)
    kpis['on_time_delivery_rate'] = orders_df['on_time'].mean() * 100

    # 2. Supplier Lead Time (average)
    orders_df['lead_time'] = (orders_df['delivery_date'] -
                              orders_df['order_date']).dt.days
    kpis['avg_lead_time_days'] = orders_df['lead_time'].mean()

    # 3. Supplier Defect Rate
    kpis['defect_rate_ppm'] = orders_df['defect_rate'].mean() * 1000000

    # 4. Purchase Order Cycle Time
    kpis['po_cycle_time_days'] = (orders_df['po_approved_date'] -
                                   orders_df['requisition_date']).dt.days.mean()

    # 5. Spend Under Management
    total_spend = orders_df['order_value'].sum()
    contracted_spend = orders_df[orders_df['has_contract']]['order_value'].sum()
    kpis['spend_under_management_pct'] = (contracted_spend / total_spend) * 100

    # 6. Supplier Concentration (top 3 suppliers % of spend)
    supplier_spend = orders_df.groupby('supplier')['order_value'].sum().sort_values(ascending=False)
    top3_pct = supplier_spend.head(3).sum() / total_spend * 100
    kpis['supplier_concentration_top3_pct'] = top3_pct

    # 7. Cost Savings vs. Baseline
    if 'baseline_cost' in orders_df.columns:
        actual_cost = orders_df['order_value'].sum()
        baseline_cost = orders_df['baseline_cost'].sum()
        kpis['cost_savings'] = baseline_cost - actual_cost
        kpis['cost_savings_pct'] = ((baseline_cost - actual_cost) / baseline_cost) * 100

    return kpis

# Example usage
procurement_kpis = calculate_procurement_kpis(orders_df)
print(f"On-Time Delivery: {procurement_kpis['on_time_delivery_rate']:.1f}%")
print(f"Average Lead Time: {procurement_kpis['avg_lead_time_days']:.1f} days")
```

#### Inventory Management

```python
def calculate_inventory_kpis(inventory_df, sales_df, cogs):
    """
    Calculate inventory KPIs

    Parameters:
    - inventory_df: columns = ['date', 'sku', 'on_hand_qty', 'unit_cost']
    - sales_df: columns = ['date', 'sku', 'quantity_sold']
    - cogs: Cost of Goods Sold (annual)
    """
    kpis = {}

    # 1. Inventory Turnover
    avg_inventory_value = (inventory_df['on_hand_qty'] *
                          inventory_df['unit_cost']).mean()
    kpis['inventory_turns'] = cogs / avg_inventory_value

    # 2. Days on Hand (DOH)
    kpis['days_on_hand'] = 365 / kpis['inventory_turns']

    # 3. Inventory Accuracy
    if 'physical_count' in inventory_df.columns:
        inventory_df['accurate'] = (
            abs(inventory_df['on_hand_qty'] - inventory_df['physical_count'])
            / inventory_df['physical_count'] < 0.02
        ).astype(int)
        kpis['inventory_accuracy_pct'] = inventory_df['accurate'].mean() * 100

    # 4. Stock-Out Rate
    total_sku_days = len(inventory_df)
    stockout_days = (inventory_df['on_hand_qty'] == 0).sum()
    kpis['stockout_rate_pct'] = (stockout_days / total_sku_days) * 100

    # 5. Excess & Obsolete Inventory
    # Items with >180 days of inventory
    daily_sales = sales_df.groupby('sku')['quantity_sold'].mean()
    inventory_latest = inventory_df.groupby('sku')['on_hand_qty'].last()

    days_of_supply = inventory_latest / daily_sales
    excess_value = inventory_df[
        inventory_df['sku'].isin(days_of_supply[days_of_supply > 180].index)
    ]['on_hand_qty'] * inventory_df['unit_cost']

    kpis['excess_obsolete_value'] = excess_value.sum()
    kpis['excess_obsolete_pct'] = (excess_value.sum() /
                                    avg_inventory_value) * 100

    # 6. Inventory Fill Rate
    total_demand = sales_df['quantity_sold'].sum()
    stockouts = sales_df[sales_df['sku'].isin(
        inventory_df[inventory_df['on_hand_qty'] == 0]['sku']
    )]['quantity_sold'].sum()

    kpis['fill_rate_pct'] = ((total_demand - stockouts) / total_demand) * 100

    # 7. Carrying Cost
    carrying_cost_rate = 0.25  # 25% annual carrying cost
    kpis['annual_carrying_cost'] = avg_inventory_value * carrying_cost_rate

    return kpis

# Example
inventory_kpis = calculate_inventory_kpis(inventory_df, sales_df, cogs=50_000_000)
print(f"Inventory Turns: {inventory_kpis['inventory_turns']:.2f}")
print(f"Days on Hand: {inventory_kpis['days_on_hand']:.1f}")
print(f"Fill Rate: {inventory_kpis['fill_rate_pct']:.1f}%")
```

#### Warehouse & Fulfillment

```python
def calculate_warehouse_kpis(orders_df, shipments_df, warehouse_sqft, labor_hours):
    """
    Calculate warehouse and fulfillment KPIs

    Parameters:
    - orders_df: order details with timestamps
    - shipments_df: shipment details
    - warehouse_sqft: total warehouse square footage
    - labor_hours: total labor hours in period
    """
    kpis = {}

    # 1. Order Cycle Time (order to ship)
    orders_df['cycle_time'] = (orders_df['ship_date'] -
                               orders_df['order_date']).dt.total_seconds() / 3600
    kpis['avg_order_cycle_time_hours'] = orders_df['cycle_time'].mean()

    # 2. Perfect Order Rate
    orders_df['perfect'] = (
        (orders_df['on_time'] == 1) &
        (orders_df['complete'] == 1) &
        (orders_df['damage_free'] == 1) &
        (orders_df['accurate'] == 1)
    ).astype(int)
    kpis['perfect_order_rate_pct'] = orders_df['perfect'].mean() * 100

    # 3. Order Picking Accuracy
    kpis['picking_accuracy_pct'] = (1 - orders_df['picking_errors'].sum() /
                                    orders_df['lines_picked'].sum()) * 100

    # 4. Warehouse Utilization
    avg_inventory_cube = orders_df['inventory_cubic_ft'].mean()
    kpis['space_utilization_pct'] = (avg_inventory_cube / warehouse_sqft) * 100

    # 5. Units per Labor Hour
    total_units = orders_df['units_shipped'].sum()
    kpis['units_per_labor_hour'] = total_units / labor_hours

    # 6. Cost per Order
    total_warehouse_cost = 500000  # example monthly cost
    total_orders = len(orders_df)
    kpis['cost_per_order'] = total_warehouse_cost / total_orders

    # 7. On-Time Shipment Rate
    shipments_df['on_time'] = (shipments_df['actual_ship_date'] <=
                               shipments_df['promised_ship_date']).astype(int)
    kpis['on_time_shipment_pct'] = shipments_df['on_time'].mean() * 100

    # 8. Dock-to-Stock Time
    if 'receipt_date' in shipments_df.columns:
        shipments_df['dock_to_stock_hours'] = (
            shipments_df['put_away_date'] -
            shipments_df['receipt_date']
        ).dt.total_seconds() / 3600
        kpis['avg_dock_to_stock_hours'] = shipments_df['dock_to_stock_hours'].mean()

    # 9. Order Accuracy Rate
    kpis['order_accuracy_pct'] = (1 - orders_df['errors'].sum() /
                                   len(orders_df)) * 100

    return kpis

warehouse_kpis = calculate_warehouse_kpis(orders_df, shipments_df,
                                          warehouse_sqft=200000,
                                          labor_hours=10000)
print(f"Perfect Order Rate: {warehouse_kpis['perfect_order_rate_pct']:.1f}%")
print(f"Units/Labor Hour: {warehouse_kpis['units_per_labor_hour']:.1f}")
```

#### Transportation & Logistics

```python
def calculate_transportation_kpis(shipments_df):
    """
    Calculate transportation and logistics KPIs

    shipments_df: columns = ['shipment_id', 'origin', 'destination',
                             'ship_date', 'delivery_date', 'promised_date',
                             'freight_cost', 'miles', 'weight_lbs', 'mode']
    """
    kpis = {}

    # 1. On-Time Delivery (OTD)
    shipments_df['on_time'] = (shipments_df['delivery_date'] <=
                               shipments_df['promised_date']).astype(int)
    kpis['on_time_delivery_pct'] = shipments_df['on_time'].mean() * 100

    # 2. Transit Time
    shipments_df['transit_days'] = (shipments_df['delivery_date'] -
                                    shipments_df['ship_date']).dt.days
    kpis['avg_transit_days'] = shipments_df['transit_days'].mean()

    # 3. Freight Cost per Mile
    total_cost = shipments_df['freight_cost'].sum()
    total_miles = shipments_df['miles'].sum()
    kpis['cost_per_mile'] = total_cost / total_miles

    # 4. Cost per Pound
    total_weight = shipments_df['weight_lbs'].sum()
    kpis['cost_per_lb'] = total_cost / total_weight

    # 5. Freight as % of Revenue
    revenue = shipments_df['order_value'].sum()
    kpis['freight_as_pct_revenue'] = (total_cost / revenue) * 100

    # 6. Damage Rate
    damaged_shipments = shipments_df['damaged'].sum()
    kpis['damage_rate_pct'] = (damaged_shipments / len(shipments_df)) * 100

    # 7. Load Factor / Utilization
    if 'truck_capacity_lbs' in shipments_df.columns:
        shipments_df['utilization'] = (shipments_df['weight_lbs'] /
                                       shipments_df['truck_capacity_lbs'])
        kpis['avg_load_utilization_pct'] = shipments_df['utilization'].mean() * 100

    # 8. Carrier Performance Score
    # Weighted score: OTD (50%), Transit Time (30%), Damage (20%)
    carrier_metrics = shipments_df.groupby('carrier').agg({
        'on_time': 'mean',
        'transit_days': 'mean',
        'damaged': 'mean',
        'shipment_id': 'count'
    })

    # Normalize and score
    carrier_metrics['otd_score'] = carrier_metrics['on_time'] * 50
    carrier_metrics['transit_score'] = (1 - carrier_metrics['transit_days'] /
                                        carrier_metrics['transit_days'].max()) * 30
    carrier_metrics['damage_score'] = (1 - carrier_metrics['damaged']) * 20
    carrier_metrics['total_score'] = (carrier_metrics['otd_score'] +
                                      carrier_metrics['transit_score'] +
                                      carrier_metrics['damage_score'])

    kpis['carrier_performance'] = carrier_metrics[['total_score']].to_dict()

    # 9. Empty Miles Percentage
    if 'empty_miles' in shipments_df.columns:
        kpis['empty_miles_pct'] = (shipments_df['empty_miles'].sum() /
                                   total_miles) * 100

    return kpis

transportation_kpis = calculate_transportation_kpis(shipments_df)
print(f"On-Time Delivery: {transportation_kpis['on_time_delivery_pct']:.1f}%")
print(f"Cost per Mile: ${transportation_kpis['cost_per_mile']:.2f}")
```

#### Overall Supply Chain Performance

```python
def calculate_scor_metrics(data_dict):
    """
    Calculate SCOR (Supply Chain Operations Reference) Model metrics

    SCOR Level 1 Metrics across 5 performance attributes:
    - Reliability: Perfect Order Fulfillment
    - Responsiveness: Order Fulfillment Cycle Time
    - Agility: Upside Supply Chain Flexibility
    - Costs: Total Supply Chain Management Cost
    - Assets: Cash-to-Cash Cycle Time
    """
    scor_metrics = {}

    # RELIABILITY
    # Perfect Order Fulfillment = % orders delivered complete, on-time, damage-free, with accurate docs
    orders = data_dict['orders']
    perfect_orders = orders[
        (orders['complete'] == 1) &
        (orders['on_time'] == 1) &
        (orders['damage_free'] == 1) &
        (orders['docs_accurate'] == 1)
    ]
    scor_metrics['RL.1.1_perfect_order_pct'] = (len(perfect_orders) / len(orders)) * 100

    # RESPONSIVENESS
    # Order Fulfillment Cycle Time = avg time from order receipt to customer receipt
    scor_metrics['RS.1.1_order_cycle_time_days'] = (
        orders['delivery_date'] - orders['order_date']
    ).dt.days.mean()

    # AGILITY
    # Upside Supply Chain Flexibility = % increase in deliverable quantity (30 days notice)
    # Typically requires historical capacity data
    scor_metrics['AG.1.1_upside_flexibility_pct'] = 20  # Example: 20% flex capacity

    # COSTS
    # Total SC Management Cost = sum of all SC costs as % of revenue
    sc_costs = {
        'plan': data_dict.get('planning_cost', 0),
        'source': data_dict.get('procurement_cost', 0),
        'make': data_dict.get('manufacturing_cost', 0),
        'deliver': data_dict.get('logistics_cost', 0),
        'return': data_dict.get('returns_cost', 0)
    }
    total_sc_cost = sum(sc_costs.values())
    revenue = data_dict['revenue']
    scor_metrics['CO.1.1_total_sc_cost_pct_revenue'] = (total_sc_cost / revenue) * 100

    # ASSETS
    # Cash-to-Cash Cycle Time = DSO + DIO - DPO
    dso = data_dict.get('days_sales_outstanding', 45)  # Days Sales Outstanding
    dio = data_dict.get('days_inventory_outstanding', 60)  # Days Inventory Outstanding
    dpo = data_dict.get('days_payable_outstanding', 30)  # Days Payable Outstanding

    scor_metrics['AM.1.1_cash_to_cash_cycle_days'] = dso + dio - dpo

    # Return on Supply Chain Fixed Assets
    scor_metrics['AM.1.2_rosc_fixed_assets'] = (
        revenue / data_dict['sc_fixed_assets']
    )

    # Working Capital
    scor_metrics['AM.1.3_working_capital'] = (
        data_dict['current_assets'] - data_dict['current_liabilities']
    )

    return scor_metrics

# Example
data_dict = {
    'orders': orders_df,
    'planning_cost': 1_000_000,
    'procurement_cost': 5_000_000,
    'manufacturing_cost': 30_000_000,
    'logistics_cost': 8_000_000,
    'returns_cost': 1_000_000,
    'revenue': 100_000_000,
    'days_sales_outstanding': 45,
    'days_inventory_outstanding': 60,
    'days_payable_outstanding': 30,
    'sc_fixed_assets': 50_000_000,
    'current_assets': 25_000_000,
    'current_liabilities': 15_000_000
}

scor_metrics = calculate_scor_metrics(data_dict)
print(f"Perfect Order: {scor_metrics['RL.1.1_perfect_order_pct']:.1f}%")
print(f"Cash-to-Cash: {scor_metrics['AM.1.1_cash_to_cash_cycle_days']:.0f} days")
```

---

## Analytics Dashboard Design

### Executive Dashboard Example

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class SupplyChainDashboard:
    """
    Build interactive supply chain analytics dashboard
    """

    def __init__(self, data):
        self.data = data

    def create_executive_dashboard(self):
        """
        Create executive-level dashboard with key metrics
        """

        # Create subplots
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=(
                'Perfect Order Rate', 'On-Time Delivery Trend', 'Inventory Turns',
                'Supply Chain Cost', 'Order Volume by Region', 'Top 10 SKUs',
                'Supplier Performance', 'Warehouse Utilization', 'Freight Cost/Mile'
            ),
            specs=[
                [{'type': 'indicator'}, {'type': 'scatter'}, {'type': 'indicator'}],
                [{'type': 'bar'}, {'type': 'pie'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'scatter'}, {'type': 'scatter'}]
            ]
        )

        # 1. Perfect Order Rate (Gauge)
        perfect_order_rate = 94.5
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=perfect_order_rate,
                title={'text': "Perfect Order %"},
                delta={'reference': 90, 'increasing': {'color': "green"}},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 80], 'color': "lightgray"},
                        {'range': [80, 90], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ),
            row=1, col=1
        )

        # 2. On-Time Delivery Trend
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        otd_trend = np.random.normal(92, 3, 12)

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=otd_trend,
                mode='lines+markers',
                name='OTD %',
                line=dict(color='blue', width=3),
                fill='tozeroy'
            ),
            row=1, col=2
        )

        # 3. Inventory Turns (Indicator)
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=6.2,
                title={'text': "Inventory Turns"},
                delta={'reference': 5.5, 'increasing': {'color': "green"}},
                number={'suffix': "x"}
            ),
            row=1, col=3
        )

        # 4. Supply Chain Cost Breakdown
        cost_categories = ['Procurement', 'Manufacturing', 'Warehousing',
                          'Transportation', 'Returns']
        costs = [5.0, 30.0, 4.0, 8.0, 1.0]

        fig.add_trace(
            go.Bar(
                x=cost_categories,
                y=costs,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                text=[f'${c}M' for c in costs],
                textposition='auto'
            ),
            row=2, col=1
        )

        # 5. Order Volume by Region (Pie)
        regions = ['North', 'South', 'East', 'West']
        volumes = [2500, 1800, 2200, 1500]

        fig.add_trace(
            go.Pie(
                labels=regions,
                values=volumes,
                hole=0.3
            ),
            row=2, col=2
        )

        # 6. Top 10 SKUs by Revenue
        skus = [f'SKU_{i}' for i in range(1, 11)]
        revenues = np.random.uniform(500, 2000, 10)

        fig.add_trace(
            go.Bar(
                y=skus,
                x=revenues,
                orientation='h',
                marker_color='lightblue'
            ),
            row=2, col=3
        )

        # 7. Supplier Performance Scores
        suppliers = ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E']
        scores = [92, 88, 95, 85, 90]

        fig.add_trace(
            go.Bar(
                x=suppliers,
                y=scores,
                marker_color=['green' if s >= 90 else 'orange' if s >= 85 else 'red'
                             for s in scores]
            ),
            row=3, col=1
        )

        # 8. Warehouse Utilization Trend
        utilization = np.random.uniform(75, 90, 12)

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=utilization,
                mode='lines+markers',
                line=dict(color='green'),
                fill='tozeroy'
            ),
            row=3, col=2
        )

        # 9. Freight Cost per Mile Trend
        freight_cost = np.random.uniform(2.20, 2.80, 12)

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=freight_cost,
                mode='lines+markers',
                line=dict(color='red')
            ),
            row=3, col=3
        )

        # Update layout
        fig.update_layout(
            title_text="Supply Chain Executive Dashboard",
            showlegend=False,
            height=1200,
            width=1600
        )

        return fig

    def create_operational_dashboard(self):
        """
        Operational dashboard with detailed metrics
        """
        # Similar structure but more detailed, real-time focused
        pass

# Usage
dashboard = SupplyChainDashboard(data)
fig = dashboard.create_executive_dashboard()
fig.show()
# or save: fig.write_html("sc_dashboard.html")
```

### Real-Time Monitoring Dashboard

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def create_realtime_dashboard():
    """
    Streamlit-based real-time monitoring dashboard
    """

    st.set_page_config(layout="wide", page_title="SC Real-Time Monitor")

    st.title("Supply Chain Real-Time Monitoring")

    # Refresh every 30 seconds
    st.markdown("Auto-refresh: 30 seconds")

    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Orders Today",
            value="1,247",
            delta="12% vs yesterday"
        )

    with col2:
        st.metric(
            label="On-Time Delivery",
            value="94.2%",
            delta="1.5%"
        )

    with col3:
        st.metric(
            label="Active Shipments",
            value="456",
            delta="-23"
        )

    with col4:
        st.metric(
            label="Warehouse Fill",
            value="82%",
            delta="3%"
        )

    with col5:
        st.metric(
            label="Alerts",
            value="7",
            delta="-2",
            delta_color="inverse"
        )

    # Alerts Section
    st.subheader("Active Alerts")
    alerts_df = pd.DataFrame({
        'Time': ['10:23 AM', '09:45 AM', '09:12 AM'],
        'Severity': ['HIGH', 'MEDIUM', 'LOW'],
        'Type': ['Stockout', 'Delayed Shipment', 'Low Inventory'],
        'Description': [
            'SKU_1234 out of stock at DC_West',
            'Shipment #45678 delayed by 4 hours',
            'SKU_5678 below reorder point'
        ]
    })

    # Color code by severity
    def highlight_severity(val):
        color = {'HIGH': 'background-color: #ffcccc',
                'MEDIUM': 'background-color: #fff4cc',
                'LOW': 'background-color: #e6f3ff'}
        return color.get(val, '')

    st.dataframe(
        alerts_df.style.applymap(highlight_severity, subset=['Severity']),
        use_container_width=True
    )

    # Charts Row
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Hourly Order Volume")

        # Generate sample data
        hours = pd.date_range(end=datetime.now(), periods=24, freq='H')
        volumes = np.random.poisson(50, 24)

        fig = px.line(
            x=hours,
            y=volumes,
            labels={'x': 'Time', 'y': 'Orders'},
            title='Last 24 Hours'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Shipment Status")

        status_data = pd.DataFrame({
            'Status': ['In Transit', 'Delivered', 'Processing', 'Delayed'],
            'Count': [156, 289, 45, 11]
        })

        fig = px.pie(
            status_data,
            values='Count',
            names='Status',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    # Warehouse Status
    st.subheader("Warehouse Status")

    warehouse_data = pd.DataFrame({
        'Warehouse': ['DC_East', 'DC_West', 'DC_Central', 'DC_South'],
        'Utilization': [85, 78, 91, 72],
        'Inbound': [45, 32, 67, 28],
        'Outbound': [123, 89, 145, 67],
        'Alerts': [2, 0, 3, 1]
    })

    st.dataframe(warehouse_data, use_container_width=True)

    # Auto-refresh
    import time
    time.sleep(30)
    st.experimental_rerun()

# Run with: streamlit run dashboard.py
```

---

## Advanced Analytics Techniques

### ABC-XYZ Segmentation Analysis

```python
def abc_xyz_segmentation(sales_df):
    """
    Combined ABC-XYZ segmentation for inventory analytics

    ABC: Value classification (revenue contribution)
    XYZ: Variability classification (demand predictability)
    """

    # Calculate annual value per SKU
    sku_analysis = sales_df.groupby('sku').agg({
        'quantity': 'sum',
        'revenue': 'sum',
        'quantity': ['mean', 'std']
    })

    sku_analysis.columns = ['total_qty', 'total_revenue', 'avg_qty', 'std_qty']

    # ABC Classification (by revenue)
    sku_analysis = sku_analysis.sort_values('total_revenue', ascending=False)
    sku_analysis['cumulative_revenue_pct'] = (
        sku_analysis['total_revenue'].cumsum() /
        sku_analysis['total_revenue'].sum() * 100
    )

    def abc_class(pct):
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        else:
            return 'C'

    sku_analysis['abc'] = sku_analysis['cumulative_revenue_pct'].apply(abc_class)

    # XYZ Classification (by variability)
    sku_analysis['coefficient_of_variation'] = (
        sku_analysis['std_qty'] / sku_analysis['avg_qty']
    )

    def xyz_class(cv):
        if cv < 0.5:
            return 'X'  # Predictable
        elif cv < 1.0:
            return 'Y'  # Variable
        else:
            return 'Z'  # Erratic

    sku_analysis['xyz'] = sku_analysis['coefficient_of_variation'].apply(xyz_class)

    # Combined classification
    sku_analysis['segment'] = sku_analysis['abc'] + sku_analysis['xyz']

    # Strategy recommendations by segment
    strategy_map = {
        'AX': 'Tight control, daily review, high service level (99%)',
        'AY': 'Frequent review, safety stock, service level (98%)',
        'AZ': 'Close monitoring, high safety stock, service level (95%)',
        'BX': 'Weekly review, moderate safety stock, service level (97%)',
        'BY': 'Weekly review, standard policies, service level (95%)',
        'BZ': 'Bi-weekly review, higher safety stock, service level (90%)',
        'CX': 'Monthly review, min/max rules, service level (90%)',
        'CY': 'Monthly review, simple policies, service level (85%)',
        'CZ': 'Order on demand or don\'t stock, service level (80%)'
    }

    sku_analysis['strategy'] = sku_analysis['segment'].map(strategy_map)

    # Segment summary
    segment_summary = sku_analysis.groupby('segment').agg({
        'sku': 'count',
        'total_revenue': 'sum',
        'total_qty': 'sum'
    }).round(0)

    segment_summary['pct_skus'] = (
        segment_summary['sku'] / segment_summary['sku'].sum() * 100
    )
    segment_summary['pct_revenue'] = (
        segment_summary['total_revenue'] / segment_summary['total_revenue'].sum() * 100
    )

    return sku_analysis, segment_summary

# Visualization
import seaborn as sns
import matplotlib.pyplot as plt

def visualize_abc_xyz(sku_analysis):
    """Create heatmap of ABC-XYZ segmentation"""

    # Create pivot table
    pivot = sku_analysis.pivot_table(
        values='sku',
        index='abc',
        columns='xyz',
        aggfunc='count',
        fill_value=0
    )

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('ABC-XYZ Segmentation Matrix (SKU Count)')
    plt.ylabel('ABC Class (Value)')
    plt.xlabel('XYZ Class (Variability)')
    plt.show()
```

### Cost-to-Serve Analysis

```python
def cost_to_serve_analysis(orders_df, customers_df):
    """
    Calculate cost-to-serve by customer

    Helps identify profitable vs. unprofitable customers
    """

    # Join order and customer data
    analysis = orders_df.merge(customers_df, on='customer_id')

    # Calculate various cost components per customer
    customer_cts = analysis.groupby('customer_id').agg({
        # Revenue
        'order_value': 'sum',

        # Order processing costs
        'order_id': 'count',  # number of orders

        # Transportation costs
        'freight_cost': 'sum',

        # Warehouse costs (could be activity-based)
        'pick_cost': 'sum',
        'pack_cost': 'sum',

        # Returns costs
        'return_cost': 'sum',

        # Service costs
        'customer_service_calls': 'sum'
    })

    # Cost assumptions
    ORDER_PROCESSING_COST = 15  # $ per order
    CS_CALL_COST = 25  # $ per call

    # Calculate total costs
    customer_cts['order_processing_cost'] = (
        customer_cts['order_id'] * ORDER_PROCESSING_COST
    )
    customer_cts['customer_service_cost'] = (
        customer_cts['customer_service_calls'] * CS_CALL_COST
    )

    customer_cts['total_costs'] = (
        customer_cts['freight_cost'] +
        customer_cts['pick_cost'] +
        customer_cts['pack_cost'] +
        customer_cts['return_cost'] +
        customer_cts['order_processing_cost'] +
        customer_cts['customer_service_cost']
    )

    customer_cts['revenue'] = customer_cts['order_value']

    # Calculate profitability
    customer_cts['gross_margin'] = customer_cts['revenue'] * 0.35  # 35% margin
    customer_cts['net_profit'] = (
        customer_cts['gross_margin'] - customer_cts['total_costs']
    )
    customer_cts['profit_margin_pct'] = (
        customer_cts['net_profit'] / customer_cts['revenue'] * 100
    )

    # Cost-to-serve percentage
    customer_cts['cost_to_serve_pct'] = (
        customer_cts['total_costs'] / customer_cts['revenue'] * 100
    )

    # Classify customers
    def classify_customer(row):
        if row['profit_margin_pct'] > 10:
            return 'Profitable'
        elif row['profit_margin_pct'] > 0:
            return 'Marginally Profitable'
        else:
            return 'Unprofitable'

    customer_cts['classification'] = customer_cts.apply(classify_customer, axis=1)

    # Customer profitability quadrant
    # High Revenue + High Profit = Protect
    # High Revenue + Low Profit = Improve
    # Low Revenue + High Profit = Grow
    # Low Revenue + Low Profit = Rationalize

    revenue_median = customer_cts['revenue'].median()
    profit_median = customer_cts['net_profit'].median()

    def quadrant(row):
        if row['revenue'] > revenue_median and row['net_profit'] > profit_median:
            return 'Protect'
        elif row['revenue'] > revenue_median:
            return 'Improve'
        elif row['net_profit'] > profit_median:
            return 'Grow'
        else:
            return 'Rationalize'

    customer_cts['quadrant'] = customer_cts.apply(quadrant, axis=1)

    return customer_cts

# Visualization
def plot_cost_to_serve(customer_cts):
    """Visualize cost-to-serve analysis"""

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 1. Revenue vs. Cost scatter
    axes[0, 0].scatter(
        customer_cts['revenue'],
        customer_cts['total_costs'],
        c=customer_cts['profit_margin_pct'],
        cmap='RdYlGn',
        s=100,
        alpha=0.6
    )
    axes[0, 0].plot([0, customer_cts['revenue'].max()],
                    [0, customer_cts['revenue'].max()],
                    'r--', label='Break-even')
    axes[0, 0].set_xlabel('Revenue ($)')
    axes[0, 0].set_ylabel('Total Costs ($)')
    axes[0, 0].set_title('Revenue vs. Costs by Customer')
    axes[0, 0].legend()

    # 2. Cost-to-Serve Distribution
    customer_cts['cost_to_serve_pct'].hist(bins=30, ax=axes[0, 1])
    axes[0, 1].axvline(customer_cts['cost_to_serve_pct'].median(),
                      color='r', linestyle='--', label='Median')
    axes[0, 1].set_xlabel('Cost-to-Serve (%)')
    axes[0, 1].set_ylabel('Number of Customers')
    axes[0, 1].set_title('Cost-to-Serve Distribution')
    axes[0, 1].legend()

    # 3. Profitability by Classification
    classification_summary = customer_cts.groupby('classification').agg({
        'customer_id': 'count',
        'revenue': 'sum',
        'net_profit': 'sum'
    })

    classification_summary.plot(kind='bar', y='net_profit', ax=axes[1, 0])
    axes[1, 0].set_title('Profit by Customer Classification')
    axes[1, 0].set_xlabel('Classification')
    axes[1, 0].set_ylabel('Net Profit ($)')

    # 4. Quadrant Analysis
    quadrant_counts = customer_cts['quadrant'].value_counts()
    axes[1, 1].pie(quadrant_counts.values, labels=quadrant_counts.index,
                   autopct='%1.1f%%')
    axes[1, 1].set_title('Customer Segmentation Quadrants')

    plt.tight_layout()
    plt.show()
```

### Pareto Analysis (80/20 Rule)

```python
def pareto_analysis(df, item_col, value_col, top_n=None):
    """
    Perform Pareto analysis (80/20 rule)

    Useful for identifying vital few vs. trivial many
    """

    # Aggregate by item
    pareto_df = df.groupby(item_col)[value_col].sum().reset_index()
    pareto_df = pareto_df.sort_values(value_col, ascending=False)

    # Calculate cumulative percentages
    total = pareto_df[value_col].sum()
    pareto_df['cumulative_value'] = pareto_df[value_col].cumsum()
    pareto_df['cumulative_pct'] = (pareto_df['cumulative_value'] / total) * 100
    pareto_df['pct_of_total'] = (pareto_df[value_col] / total) * 100

    # Find 80% threshold
    threshold_idx = (pareto_df['cumulative_pct'] <= 80).sum()
    pct_items_for_80 = (threshold_idx / len(pareto_df)) * 100

    print(f"Pareto Insight: {threshold_idx} items ({pct_items_for_80:.1f}%) "
          f"account for 80% of {value_col}")

    # Visualization
    if top_n is None:
        top_n = min(20, len(pareto_df))

    plot_df = pareto_df.head(top_n)

    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Bar chart
    ax1.bar(range(len(plot_df)), plot_df[value_col], color='steelblue', alpha=0.7)
    ax1.set_xlabel(item_col)
    ax1.set_ylabel(value_col, color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')

    # Line chart for cumulative %
    ax2 = ax1.twinx()
    ax2.plot(range(len(plot_df)), plot_df['cumulative_pct'],
             color='red', marker='o', linewidth=2)
    ax2.axhline(y=80, color='green', linestyle='--', label='80% threshold')
    ax2.set_ylabel('Cumulative %', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 100)
    ax2.legend()

    plt.title(f'Pareto Analysis: Top {top_n} {item_col}')
    plt.xticks(range(len(plot_df)), plot_df[item_col], rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return pareto_df

# Example usage
pareto_results = pareto_analysis(sales_df, 'sku', 'revenue', top_n=20)
```

---

## Tools & Technologies

### Python Libraries

**Data Manipulation & Analysis:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `polars`: High-performance DataFrames (faster than pandas)
- `dask`: Parallel computing for large datasets

**Visualization:**
- `matplotlib`: Basic plotting
- `seaborn`: Statistical visualizations
- `plotly`: Interactive charts and dashboards
- `altair`: Declarative visualization

**Dashboard & BI:**
- `streamlit`: Quick web apps and dashboards
- `dash (Plotly)`: Enterprise dashboards
- `panel (HoloViz)`: Flexible dashboards
- `voila`: Jupyter notebooks as web apps

**Database & Data Warehouse:**
- `sqlalchemy`: SQL toolkit
- `psycopg2`: PostgreSQL adapter
- `pyodbc`: ODBC database connection
- `snowflake-connector-python`: Snowflake connection

**Statistical Analysis:**
- `scipy`: Scientific computing and statistics
- `statsmodels`: Statistical models
- `scikit-learn`: Machine learning metrics

### Business Intelligence Tools

**Commercial:**
- **Tableau**: Leading visualization and BI platform
- **Power BI (Microsoft)**: Integrated with Microsoft ecosystem
- **Qlik Sense**: Associative analytics engine
- **Looker (Google)**: Cloud-native BI
- **Domo**: Cloud-based BI platform
- **ThoughtSpot**: AI-powered analytics

**Open Source:**
- **Apache Superset**: Modern data exploration platform
- **Metabase**: Simple BI for everyone
- **Redash**: Connect and visualize data
- **Grafana**: Monitoring and observability dashboards

### Supply Chain Specific Platforms

**Enterprise:**
- **SAP Analytics Cloud**: Integrated with SAP S/4HANA
- **Oracle Analytics**: BI for Oracle ecosystem
- **Blue Yonder (JDA)**: Supply chain analytics suite
- **Kinaxis RapidResponse**: Concurrent planning platform
- **o9 Solutions**: Digital brain platform
- **LLamasoft**: Supply chain analytics (now Coupa)

**Specialized:**
- **Llamasoft Supply Chain Guru**: Network modeling and analytics
- **FourKites**: Real-time supply chain visibility
- **project44**: Supply chain visibility platform
- **Shippeo**: Transport visibility

---

## Data Integration & ETL

### Building Data Pipelines

```python
import pandas as pd
from sqlalchemy import create_engine
import logging

class SupplyChainETL:
    """
    Extract, Transform, Load pipeline for supply chain data
    """

    def __init__(self, source_configs, target_config):
        self.source_configs = source_configs
        self.target_config = target_config
        self.logger = logging.getLogger(__name__)

    def extract_from_sql(self, config):
        """Extract data from SQL database"""

        try:
            engine = create_engine(config['connection_string'])

            query = config.get('query') or f"SELECT * FROM {config['table']}"

            df = pd.read_sql(query, engine)

            self.logger.info(f"Extracted {len(df)} rows from {config['source']}")

            return df

        except Exception as e:
            self.logger.error(f"Error extracting from {config['source']}: {e}")
            raise

    def extract_from_api(self, config):
        """Extract data from REST API"""

        import requests

        try:
            response = requests.get(
                config['url'],
                headers=config.get('headers', {}),
                params=config.get('params', {})
            )

            response.raise_for_status()

            data = response.json()
            df = pd.DataFrame(data[config['data_key']])

            self.logger.info(f"Extracted {len(df)} rows from {config['source']}")

            return df

        except Exception as e:
            self.logger.error(f"Error extracting from API {config['source']}: {e}")
            raise

    def transform_orders(self, orders_df):
        """Transform orders data"""

        # Data cleaning
        orders_df = orders_df.drop_duplicates(subset=['order_id'])

        # Data type conversions
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        orders_df['ship_date'] = pd.to_datetime(orders_df['ship_date'])
        orders_df['delivery_date'] = pd.to_datetime(orders_df['delivery_date'])

        # Derived fields
        orders_df['order_to_ship_days'] = (
            orders_df['ship_date'] - orders_df['order_date']
        ).dt.days

        orders_df['ship_to_delivery_days'] = (
            orders_df['delivery_date'] - orders_df['ship_date']
        ).dt.days

        orders_df['on_time'] = (
            orders_df['delivery_date'] <= orders_df['promised_date']
        ).astype(int)

        # Categorization
        orders_df['order_size_category'] = pd.cut(
            orders_df['order_value'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Small', 'Medium', 'Large', 'XLarge']
        )

        # Data quality checks
        null_counts = orders_df.isnull().sum()
        if null_counts.any():
            self.logger.warning(f"Null values found: {null_counts[null_counts > 0]}")

        return orders_df

    def load_to_warehouse(self, df, table_name):
        """Load transformed data to data warehouse"""

        try:
            engine = create_engine(self.target_config['connection_string'])

            df.to_sql(
                table_name,
                engine,
                if_exists='replace',  # or 'append'
                index=False,
                chunksize=1000
            )

            self.logger.info(f"Loaded {len(df)} rows to {table_name}")

        except Exception as e:
            self.logger.error(f"Error loading to {table_name}: {e}")
            raise

    def run_pipeline(self):
        """Execute full ETL pipeline"""

        self.logger.info("Starting ETL pipeline...")

        # Extract
        orders_df = self.extract_from_sql(self.source_configs['orders'])
        shipments_df = self.extract_from_sql(self.source_configs['shipments'])
        inventory_df = self.extract_from_api(self.source_configs['inventory_api'])

        # Transform
        orders_clean = self.transform_orders(orders_df)

        # Combine/join datasets as needed
        # ... additional transformations

        # Load
        self.load_to_warehouse(orders_clean, 'fact_orders')
        self.load_to_warehouse(shipments_df, 'fact_shipments')
        self.load_to_warehouse(inventory_df, 'fact_inventory')

        self.logger.info("ETL pipeline completed successfully")

# Configuration
source_configs = {
    'orders': {
        'source': 'ERP',
        'connection_string': 'postgresql://user:pass@host:5432/erp_db',
        'table': 'orders'
    },
    'shipments': {
        'source': 'TMS',
        'connection_string': 'postgresql://user:pass@host:5432/tms_db',
        'table': 'shipments'
    },
    'inventory_api': {
        'source': 'WMS_API',
        'url': 'https://api.wms.com/v1/inventory',
        'headers': {'Authorization': 'Bearer token'},
        'data_key': 'inventory'
    }
}

target_config = {
    'connection_string': 'postgresql://user:pass@host:5432/analytics_dw'
}

# Run ETL
etl = SupplyChainETL(source_configs, target_config)
etl.run_pipeline()
```

---

## Common Challenges & Solutions

### Challenge: Data Quality Issues

**Problem:**
- Missing data, duplicates, inconsistencies
- Different data formats across systems
- Stale or inaccurate data

**Solutions:**
- Implement data quality checks in ETL pipeline
- Create data quality dashboards showing completeness, accuracy
- Establish data governance policies
- Use data profiling tools to identify issues
- Automate data validation rules

```python
def data_quality_report(df):
    """Generate data quality report"""

    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
    }

    # Missing values
    missing = df.isnull().sum()
    report['missing_values'] = missing[missing > 0].to_dict()
    report['completeness_pct'] = (1 - df.isnull().sum().sum() /
                                   (len(df) * len(df.columns))) * 100

    # Duplicates
    report['duplicate_rows'] = df.duplicated().sum()

    # Data types
    report['data_types'] = df.dtypes.value_counts().to_dict()

    # Outliers (for numeric columns)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers[col] = ((df[col] < (Q1 - 1.5 * IQR)) |
                        (df[col] > (Q3 + 1.5 * IQR))).sum()
    report['outliers'] = outliers

    return report
```

### Challenge: Siloed Data Systems

**Problem:**
- Data scattered across ERP, WMS, TMS, etc.
- No single source of truth
- Manual data consolidation

**Solutions:**
- Build centralized data warehouse or data lake
- Implement master data management (MDM)
- Use ETL/ELT tools (Apache Airflow, Fivetran, Stitch)
- Create data integration layer (API gateway)
- Standardize data models across systems

### Challenge: Real-Time Analytics Requirements

**Problem:**
- Batch processing too slow for operational decisions
- Need for up-to-the-minute visibility

**Solutions:**
- Implement streaming data pipelines (Apache Kafka, AWS Kinesis)
- Use real-time databases (Redis, TimescaleDB)
- Create operational dashboards with auto-refresh
- Set up event-driven architecture
- Use change data capture (CDC) for database synchronization

### Challenge: Actionable Insights from Data

**Problem:**
- Data available but not actionable
- Overwhelming amount of metrics
- Difficulty identifying root causes

**Solutions:**
- Focus on leading vs. lagging indicators
- Implement automated alerting for exceptions
- Use drill-down capabilities in dashboards
- Apply root cause analysis methodologies
- Create action-oriented reports (not just descriptive stats)

---

## Output Format

### Analytics Report Template

**Executive Summary:**
- Key findings (3-5 bullet points)
- Critical issues requiring attention
- Improvement opportunities
- Recommended actions

**Performance Overview:**

| KPI | Current | Target | Last Period | YoY Change | Status |
|-----|---------|--------|-------------|------------|--------|
| Perfect Order Rate | 94.2% | 95% | 93.5% | +2.1% | ⚠️ |
| On-Time Delivery | 96.8% | 98% | 95.2% | +3.4% | ⚠️ |
| Inventory Turns | 6.2x | 7.0x | 5.8x | +6.9% | ⚠️ |
| Order Cycle Time | 2.1 days | 2.0 days | 2.3 days | -8.7% | ✅ |
| Freight Cost/Revenue | 8.2% | 7.5% | 8.5% | -3.5% | ⚠️ |

**Trend Analysis:**
- Time series charts for key metrics
- Seasonality patterns identified
- Anomaly detection highlights

**Root Cause Analysis:**
- Deep dive into underperforming areas
- Pareto analysis of issues
- Correlation analysis

**Recommendations:**
1. **Immediate Actions** (0-30 days)
   - Specific, actionable items
   - Owner and deadline

2. **Short-Term Initiatives** (1-3 months)
   - Process improvements
   - System enhancements

3. **Strategic Programs** (3-12 months)
   - Long-term transformations
   - Investment requirements

**Appendix:**
- Detailed methodology
- Data sources and quality notes
- Assumptions and calculations

---

## Questions to Ask

If you need more context:
1. What supply chain processes need analytics? (procurement, inventory, transportation, etc.)
2. Who will use these analytics? (executives, planners, analysts)
3. What are the key business questions you need answered?
4. What data sources are available? (ERP, WMS, TMS, spreadsheets)
5. What's the current state of analytics capabilities?
6. What tools are you using or prefer? (Tableau, Power BI, Python)
7. What are the critical KPIs you track today?
8. What reporting frequency is needed? (real-time, daily, weekly, monthly)

---

## Related Skills

- **demand-forecasting**: For predictive analytics and forecasting models
- **optimization-modeling**: For prescriptive analytics and optimization
- **ml-supply-chain**: For advanced machine learning applications
- **prescriptive-analytics**: For decision support and recommendations
- **digital-twin-modeling**: For simulation and scenario analysis
- **inventory-optimization**: For inventory-specific KPIs and analysis
- **network-design**: For network performance analytics
- **freight-optimization**: For transportation analytics
