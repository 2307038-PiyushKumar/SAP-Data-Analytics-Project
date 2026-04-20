"""
SAP Inventory & Supply Chain Dashboard
========================================
Interactive Dash app — run with:  python dashboard.py
Then open: http://127.0.0.1:8050
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc   # pip install dash-bootstrap-components

BASE   = os.path.dirname(__file__)
DATA   = os.path.join(BASE, '..', 'Data')
OUTPUT = os.path.join(BASE, '..', 'Output')

# ── Load ─────────────────────────────────────────────────────────────────────
inv = pd.read_csv(os.path.join(DATA, 'Inventory.csv'), parse_dates=['Date'])
sup = pd.read_csv(os.path.join(DATA, 'Suppliers.csv'))
wh  = pd.read_csv(os.path.join(DATA, 'Warehouses.csv'))

CATEGORIES  = ['All'] + sorted(inv['Category'].unique().tolist())
WAREHOUSES  = ['All'] + sorted(inv['WarehouseID'].unique().tolist())
MOVEMENTS   = ['All'] + sorted(inv['MovementType'].unique().tolist())

# ── Colour palette ────────────────────────────────────────────────────────────
COLORS = dict(
    bg       = '#0D1117',
    card     = '#161B22',
    border   = '#30363D',
    accent   = '#00C9A7',
    accent2  = '#F78C6C',
    accent3  = '#C792EA',
    text     = '#E6EDF3',
    subtext  = '#8B949E',
)

CARD_STYLE = {
    'backgroundColor': COLORS['card'],
    'border': f'1px solid {COLORS["border"]}',
    'borderRadius': '10px',
    'padding': '16px',
    'marginBottom': '16px',
}

def kpi_card(title, value, unit='', color=None):
    color = color or COLORS['accent']
    return html.Div([
        html.P(title, style={'color': COLORS['subtext'], 'fontSize': '12px',
                             'marginBottom': '4px', 'textTransform': 'uppercase',
                             'letterSpacing': '1px'}),
        html.H3(f'{value}{unit}', style={'color': color, 'margin': '0',
                                          'fontSize': '28px', 'fontWeight': '700'}),
    ], style={**CARD_STYLE, 'textAlign': 'center'})

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG],
           suppress_callback_exceptions=True)
app.title = 'SAP Supply Chain Dashboard'

app.layout = html.Div(style={'backgroundColor': COLORS['bg'],
                              'minHeight': '100vh', 'fontFamily': 'Segoe UI, sans-serif',
                              'color': COLORS['text'], 'padding': '24px'}, children=[

    # ── Header ────────────────────────────────────────────────────────────────
    html.Div([
        html.H1('📦 SAP Inventory & Supply Chain Dashboard',
                style={'color': COLORS['accent'], 'margin': '0 0 4px 0',
                       'fontSize': '26px', 'fontWeight': '700'}),
        html.P('SAP MM/WM · aDSO + CompositeProvider · Stock KPIs',
               style={'color': COLORS['subtext'], 'margin': '0', 'fontSize': '13px'}),
    ], style={'marginBottom': '24px'}),

    # ── Filters ───────────────────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.Label('Category', style={'color': COLORS['subtext'], 'fontSize': '12px'}),
            dcc.Dropdown(CATEGORIES, 'All', id='filter-category', clearable=False,
                         style={'backgroundColor': COLORS['card'],
                                'color': COLORS['text'], 'border': f'1px solid {COLORS["border"]}'}),
        ], style={'flex': '1', 'marginRight': '12px'}),

        html.Div([
            html.Label('Warehouse', style={'color': COLORS['subtext'], 'fontSize': '12px'}),
            dcc.Dropdown(WAREHOUSES, 'All', id='filter-warehouse', clearable=False,
                         style={'backgroundColor': COLORS['card'],
                                'color': COLORS['text'], 'border': f'1px solid {COLORS["border"]}'}),
        ], style={'flex': '1', 'marginRight': '12px'}),

        html.Div([
            html.Label('Movement Type', style={'color': COLORS['subtext'], 'fontSize': '12px'}),
            dcc.Dropdown(MOVEMENTS, 'All', id='filter-movement', clearable=False,
                         style={'backgroundColor': COLORS['card'],
                                'color': COLORS['text'], 'border': f'1px solid {COLORS["border"]}'}),
        ], style={'flex': '1', 'marginRight': '12px'}),

        html.Div([
            html.Label('Date Range', style={'color': COLORS['subtext'], 'fontSize': '12px'}),
            dcc.DatePickerRange(
                id='filter-date',
                min_date_allowed=inv['Date'].min(),
                max_date_allowed=inv['Date'].max(),
                start_date=inv['Date'].min(),
                end_date=inv['Date'].max(),
                style={'backgroundColor': COLORS['card']},
            ),
        ], style={'flex': '2'}),
    ], style={'display': 'flex', 'alignItems': 'flex-end', 'marginBottom': '24px',
              **CARD_STYLE}),

    # ── KPI Row ───────────────────────────────────────────────────────────────
    html.Div(id='kpi-row',
             style={'display': 'grid',
                    'gridTemplateColumns': 'repeat(5, 1fr)',
                    'gap': '12px', 'marginBottom': '16px'}),

    # ── Charts Row 1 ─────────────────────────────────────────────────────────
    html.Div([
        html.Div([dcc.Graph(id='chart-stock-cat')],
                 style={**CARD_STYLE, 'flex': '1', 'marginRight': '12px'}),
        html.Div([dcc.Graph(id='chart-movement-pie')],
                 style={**CARD_STYLE, 'flex': '1'}),
    ], style={'display': 'flex', 'marginBottom': '4px'}),

    # ── Charts Row 2 ─────────────────────────────────────────────────────────
    html.Div([
        html.Div([dcc.Graph(id='chart-monthly')],
                 style={**CARD_STYLE, 'flex': '2', 'marginRight': '12px'}),
        html.Div([dcc.Graph(id='chart-wh-util')],
                 style={**CARD_STYLE, 'flex': '1'}),
    ], style={'display': 'flex', 'marginBottom': '4px'}),

    # ── Charts Row 3 ─────────────────────────────────────────────────────────
    html.Div([
        html.Div([dcc.Graph(id='chart-slow')],
                 style={**CARD_STYLE, 'flex': '1', 'marginRight': '12px'}),
        html.Div([dcc.Graph(id='chart-supplier')],
                 style={**CARD_STYLE, 'flex': '1'}),
    ], style={'display': 'flex', 'marginBottom': '4px'}),

    # ── Data Table ───────────────────────────────────────────────────────────
    html.Div([
        html.H4('Transaction Log', style={'color': COLORS['accent'],
                                           'marginBottom': '12px'}),
        dash_table.DataTable(
            id='data-table',
            page_size=12,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': COLORS['border'],
                          'color': COLORS['text'], 'fontWeight': 'bold'},
            style_cell={'backgroundColor': COLORS['card'],
                        'color': COLORS['text'], 'border': f'1px solid {COLORS["border"]}',
                        'fontSize': '12px', 'textAlign': 'left', 'padding': '8px'},
            style_data_conditional=[
                {'if': {'filter_query': '{SlowMoving} = "Yes"'},
                 'backgroundColor': '#2d1a1a', 'color': '#FF6B6B'},
            ],
        ),
    ], style=CARD_STYLE),
])

# ── Callbacks ─────────────────────────────────────────────────────────────────
DARK = 'plotly_dark'
LAYOUT_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=COLORS['text'], size=11),
    margin=dict(l=40, r=20, t=40, b=40),
)

def filter_df(cat, wh_id, mov, start, end):
    df = inv.copy()
    if cat  != 'All': df = df[df['Category']    == cat]
    if wh_id!= 'All': df = df[df['WarehouseID'] == wh_id]
    if mov  != 'All': df = df[df['MovementType']== mov]
    df = df[(df['Date'] >= start) & (df['Date'] <= end)]
    return df

@app.callback(
    Output('kpi-row',          'children'),
    Output('chart-stock-cat',  'figure'),
    Output('chart-movement-pie','figure'),
    Output('chart-monthly',    'figure'),
    Output('chart-wh-util',    'figure'),
    Output('chart-slow',       'figure'),
    Output('chart-supplier',   'figure'),
    Output('data-table',       'data'),
    Output('data-table',       'columns'),
    Input('filter-category',   'value'),
    Input('filter-warehouse',  'value'),
    Input('filter-movement',   'value'),
    Input('filter-date',       'start_date'),
    Input('filter-date',       'end_date'),
)
def update_all(cat, wh_id, mov, start, end):
    df = filter_df(cat, wh_id, mov, pd.Timestamp(start), pd.Timestamp(end))

    # KPIs
    total_val    = df['TotalValue'].sum()
    avg_stock    = df['StockLevel'].mean() if len(df) else 0
    slow_pct     = (df['SlowMoving'] == 'Yes').mean() * 100 if len(df) else 0
    transactions = len(df)
    products     = df['ProductID'].nunique()

    kpis = html.Div([
        kpi_card('Transactions',    f'{transactions:,}',  color=COLORS['accent']),
        kpi_card('Inventory Value', f'₹{total_val/1e6:.1f}M', color=COLORS['accent2']),
        kpi_card('Avg Stock Level', f'{avg_stock:,.0f}',  color=COLORS['accent3']),
        kpi_card('Slow-Moving',     f'{slow_pct:.1f}',   '%', color='#FF6B6B'),
        kpi_card('Unique Products', f'{products}',        color='#82B1FF'),
    ], style={'display': 'contents'})

    # 1. Stock by category
    sc = (df.groupby('Category')['StockLevel'].mean()
            .reset_index().sort_values('StockLevel', ascending=False))
    fig1 = px.bar(sc, x='Category', y='StockLevel',
                  color='Category', template=DARK,
                  color_discrete_sequence=px.colors.qualitative.Bold,
                  title='Avg Stock Level by Category',
                  labels={'StockLevel': 'Avg Units'})
    fig1.update_layout(**LAYOUT_BASE, showlegend=False)

    # 2. Movement pie
    mv = df['MovementType'].value_counts().reset_index()
    mv.columns = ['Type', 'Count']
    fig2 = px.pie(mv, names='Type', values='Count', hole=0.45,
                  template=DARK, title='Movement Type Split',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(**LAYOUT_BASE)

    # 3. Monthly trend
    df2 = df[df['MovementType'].isin(['Inbound', 'Outbound'])].copy()
    df2['Month'] = df2['Date'].dt.to_period('M').astype(str)
    mt = df2.groupby(['Month', 'MovementType'])['Quantity'].sum().reset_index()
    fig3 = px.line(mt, x='Month', y='Quantity', color='MovementType',
                   markers=True, template=DARK,
                   color_discrete_map={'Inbound': COLORS['accent'],
                                       'Outbound': COLORS['accent2']},
                   title='Monthly Stock Movement',
                   labels={'Quantity': 'Units', 'Month': ''})
    fig3.update_layout(**LAYOUT_BASE)
    fig3.update_xaxes(tickangle=45)

    # 4. Warehouse utilisation
    ws = (df.groupby('WarehouseID')['StockLevel'].sum().reset_index()
            .merge(wh[['WarehouseID', 'WarehouseName', 'Capacity_Units']], on='WarehouseID'))
    ws['Util'] = (ws['StockLevel'] / ws['Capacity_Units'] * 100).round(1)
    fig4 = px.bar(ws, x='WarehouseName', y='Util',
                  color='Util', color_continuous_scale='RdYlGn_r',
                  template=DARK, title='Warehouse Utilisation (%)',
                  text='Util', labels={'Util': '%', 'WarehouseName': ''})
    fig4.update_traces(texttemplate='%{text}%', textposition='outside')
    fig4.update_layout(**LAYOUT_BASE, coloraxis_showscale=False)

    # 5. Slow-moving
    sl = (df[df['SlowMoving'] == 'Yes']
            .groupby('ProductName')['TotalValue'].sum()
            .reset_index().sort_values('TotalValue', ascending=False).head(8))
    fig5 = px.bar(sl, x='TotalValue', y='ProductName', orientation='h',
                  color='TotalValue', color_continuous_scale='Reds',
                  template=DARK, title='Top Slow-Moving Items (Value ₹)',
                  labels={'TotalValue': 'Value (₹)', 'ProductName': ''})
    fig5.update_layout(**LAYOUT_BASE, coloraxis_showscale=False)

    # 6. Supplier scatter
    sp = (df.groupby('SupplierID')
            .agg(Txns=('TransactionID','count'), Val=('TotalValue','sum'))
            .reset_index()
            .merge(sup[['SupplierID','SupplierName','Rating','OnTime_Pct']], on='SupplierID'))
    fig6 = px.scatter(sp, x='Rating', y='OnTime_Pct', size='Val',
                      color='SupplierName', template=DARK,
                      size_max=40, title='Supplier: Rating vs On-Time %',
                      labels={'Rating': 'Rating', 'OnTime_Pct': 'On-Time %'})
    fig6.update_layout(**LAYOUT_BASE)

    # Table
    cols_show = ['TransactionID','ProductName','Category','WarehouseID',
                 'MovementType','Quantity','TotalValue','StockLevel','SlowMoving','Date']
    tbl_df = df[cols_show].head(200).copy()
    tbl_df['Date'] = tbl_df['Date'].astype(str)
    tbl_df['TotalValue'] = tbl_df['TotalValue'].apply(lambda x: f'₹{x:,.0f}')
    columns = [{'name': c, 'id': c} for c in cols_show]

    return (kpis, fig1, fig2, fig3, fig4, fig5, fig6,
            tbl_df.to_dict('records'), columns)


if __name__ == '__main__':
    app.run(debug=True)
