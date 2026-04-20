"""
SAP Inventory & Supply Chain Analytics
=======================================
Reads Data/ CSVs, performs analysis, saves charts + summary CSVs to Output/
Uses: pandas, plotly
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'Output')
DATA   = os.path.join(os.path.dirname(__file__), '..', 'Data')
os.makedirs(OUTPUT, exist_ok=True)

# ── Load Data ────────────────────────────────────────────────────────────────
inv = pd.read_csv(os.path.join(DATA, 'Inventory.csv'), parse_dates=['Date'])
sup = pd.read_csv(os.path.join(DATA, 'Suppliers.csv'))
wh  = pd.read_csv(os.path.join(DATA, 'Warehouses.csv'))

print(f"Loaded Inventory: {len(inv)} rows")
print(f"Loaded Suppliers: {len(sup)} rows")
print(f"Loaded Warehouses: {len(wh)} rows")

# ── 1. Stock Level by Category ───────────────────────────────────────────────
stock_by_cat = (inv.groupby('Category')['StockLevel']
                   .mean()
                   .reset_index()
                   .rename(columns={'StockLevel': 'AvgStockLevel'})
                   .sort_values('AvgStockLevel', ascending=False))

fig1 = px.bar(
    stock_by_cat, x='Category', y='AvgStockLevel',
    title='Average Stock Level by Product Category',
    color='Category',
    color_discrete_sequence=px.colors.qualitative.Bold,
    labels={'AvgStockLevel': 'Avg Stock Level (Units)'},
    template='plotly_dark'
)
fig1.update_layout(showlegend=False, font=dict(size=13))
fig1.write_image(os.path.join(OUTPUT, 'stock_by_category_chart.png'))
print("[OK] stock_by_category_chart.png")

# ── 2. Slow-Moving Items ──────────────────────────────────────────────────────
slow_items = (inv[inv['SlowMoving'] == 'Yes']
              .groupby('ProductName')
              .agg(Count=('TransactionID', 'count'),
                   AvgStock=('StockLevel', 'mean'),
                   TotalValue=('TotalValue', 'sum'))
              .reset_index()
              .sort_values('TotalValue', ascending=False))

slow_items.to_csv(os.path.join(OUTPUT, 'slow_moving_items.csv'), index=False)

fig2 = px.bar(
    slow_items.head(10), x='TotalValue', y='ProductName',
    orientation='h',
    title='Top 10 Slow-Moving Items by Locked-Up Value',
    color='TotalValue',
    color_continuous_scale='Reds',
    labels={'TotalValue': 'Total Inventory Value (₹)', 'ProductName': ''},
    template='plotly_dark'
)
fig2.update_layout(font=dict(size=12))
fig2.write_image(os.path.join(OUTPUT, 'slow_moving_chart.png'))
print("[OK] slow_moving_chart.png")

# ── 3. Stock Movement Type Distribution ──────────────────────────────────────
movement = inv['MovementType'].value_counts().reset_index()
movement.columns = ['MovementType', 'Count']

fig3 = px.pie(
    movement, names='MovementType', values='Count',
    title='Stock Movement Type Distribution',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    template='plotly_dark',
    hole=0.4
)
fig3.update_traces(textinfo='percent+label')
fig3.write_image(os.path.join(OUTPUT, 'movement_distribution_chart.png'))
print("[OK] movement_distribution_chart.png")

# ── 4. Monthly Inbound vs Outbound Trend ────────────────────────────────────
inv['Month'] = inv['Date'].dt.to_period('M').astype(str)
monthly = (inv[inv['MovementType'].isin(['Inbound', 'Outbound'])]
           .groupby(['Month', 'MovementType'])['Quantity']
           .sum()
           .reset_index())

fig4 = px.line(
    monthly, x='Month', y='Quantity', color='MovementType',
    title='Monthly Inbound vs Outbound Stock Movement',
    markers=True,
    color_discrete_map={'Inbound': '#00C9A7', 'Outbound': '#FF6B6B'},
    template='plotly_dark',
    labels={'Quantity': 'Total Units', 'Month': ''}
)
fig4.update_xaxes(tickangle=45)
fig4.write_image(os.path.join(OUTPUT, 'monthly_movement_chart.png'))
print("[OK] monthly_movement_chart.png")

# ── 5. Supplier Performance ──────────────────────────────────────────────────
sup_perf = (inv.groupby('SupplierID')
               .agg(Transactions=('TransactionID', 'count'),
                    TotalValue=('TotalValue', 'sum'))
               .reset_index()
               .merge(sup[['SupplierID', 'SupplierName', 'Rating', 'OnTime_Pct']],
                      on='SupplierID'))

sup_perf.to_csv(os.path.join(OUTPUT, 'supplier_performance.csv'), index=False)

fig5 = px.scatter(
    sup_perf, x='Rating', y='OnTime_Pct',
    size='TotalValue', color='SupplierName',
    title='Supplier Rating vs On-Time Delivery %',
    labels={'Rating': 'Supplier Rating', 'OnTime_Pct': 'On-Time Delivery (%)'},
    template='plotly_dark',
    size_max=50
)
fig5.write_image(os.path.join(OUTPUT, 'supplier_performance_chart.png'))
print("[OK] supplier_performance_chart.png")

# ── 6. Warehouse Utilisation ─────────────────────────────────────────────────
wh_stock = (inv.groupby('WarehouseID')['StockLevel']
               .sum()
               .reset_index()
               .merge(wh[['WarehouseID', 'WarehouseName', 'Capacity_Units']],
                      on='WarehouseID'))
wh_stock['Utilisation_Pct'] = (wh_stock['StockLevel'] /
                                wh_stock['Capacity_Units'] * 100).round(1)

fig6 = px.bar(
    wh_stock, x='WarehouseName', y='Utilisation_Pct',
    title='Warehouse Utilisation (%)',
    color='Utilisation_Pct',
    color_continuous_scale='RdYlGn_r',
    template='plotly_dark',
    labels={'Utilisation_Pct': 'Utilisation (%)', 'WarehouseName': ''},
    text='Utilisation_Pct'
)
fig6.update_traces(texttemplate='%{text}%', textposition='outside')
fig6.write_image(os.path.join(OUTPUT, 'warehouse_utilisation_chart.png'))
print("[OK] warehouse_utilisation_chart.png")

# ── 7. KPI Summary ───────────────────────────────────────────────────────────
kpi = {
    'Total_Transactions':   len(inv),
    'Total_Inventory_Value': round(inv['TotalValue'].sum(), 2),
    'Avg_Stock_Level':       round(inv['StockLevel'].mean(), 1),
    'Slow_Moving_Count':     int((inv['SlowMoving'] == 'Yes').sum()),
    'Slow_Moving_Pct':       round((inv['SlowMoving'] == 'Yes').mean() * 100, 1),
    'Avg_Supplier_Rating':   round(sup['Rating'].mean(), 2),
    'Avg_OnTime_Delivery':   round(sup['OnTime_Pct'].mean(), 1),
    'Warehouses':            len(wh),
    'Unique_Products':       inv['ProductID'].nunique(),
    'Active_Suppliers':      inv['SupplierID'].nunique(),
}
pd.DataFrame([kpi]).T.reset_index().rename(
    columns={'index': 'KPI', 0: 'Value'}
).to_csv(os.path.join(OUTPUT, 'kpi_summary.csv'), index=False)

print("\n── KPI SUMMARY ──────────────────────────────")
for k, v in kpi.items():
    print(f"  {k:<30} {v}")
print("\n[OK] All analysis complete. Outputs saved to Output/")
