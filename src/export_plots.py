# ============================================================
# export_plots.py — regenerate all plots from the feather file
# ============================================================
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing

DATA  = 'data/Sales_data.ftr'
OUT   = 'plots'
os.makedirs(OUT, exist_ok=True)

# ---- load & clean ----
df = pd.read_feather(DATA)
df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
df['Price Each']       = pd.to_numeric(df['Price Each'],       errors='coerce')
df = df.dropna(subset=['Quantity Ordered', 'Price Each'])
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', format='mixed')
df = df.dropna(subset=['Order Date'])
df['Sales']   = df['Quantity Ordered'] * df['Price Each']
df['Month']   = df['Order Date'].dt.to_period('M').astype(str)
df['Hour']    = df['Order Date'].dt.hour
df['Weekday'] = df['Order Date'].dt.day_name()
df['City']    = df['Purchase Address'].str.split(',').str[1].str.strip()

def save(fig, name):
    fig.write_html(f'{OUT}/{name}.html')
    fig.write_image(f'{OUT}/{name}.png', width=1200, height=500, scale=2)
    print(f'  ✓ {name}')

# ---- 01 monthly ----
m = df.groupby('Month')['Sales'].sum().reset_index()
save(px.line(m, x='Month', y='Sales', markers=True,
             title='Monthly Sales', template='plotly_white'), '01_monthly_sales')

# ---- 02 product prices ----
p = df.groupby('Product')['Price Each'].mean().reset_index().sort_values('Price Each', ascending=False)
save(px.bar(p, x='Product', y='Price Each', title='Average Price per Product',
            template='plotly_white', color='Price Each',
            color_continuous_scale='Blues'), '02_price_pillars')

# ---- 03 top cities ----
c = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
save(px.bar(c, x='City', y='Sales', title='Top 10 Cities',
            template='plotly_white', color='Sales'), '03_top_cities')

# ---- 04 hour + weekday ----
fig = make_subplots(rows=1, cols=2, subplot_titles=('Hour', 'Weekday'))
h = df.groupby('Hour')['Sales'].sum().reset_index()
fig.add_trace(go.Scatter(x=h['Hour'], y=h['Sales'], mode='lines+markers'), row=1, col=1)
order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
w = df.groupby('Weekday')['Sales'].sum().reindex(order).reset_index()
fig.add_trace(go.Bar(x=w['Weekday'], y=w['Sales']), row=1, col=2)
fig.update_layout(height=400, template='plotly_white', showlegend=False)
save(fig, '04_hour_weekday')

# ---- 05 forecast ----
ts = df.groupby('Month')['Sales'].sum().sort_index()
ts.index = pd.to_datetime(ts.index)
ts = ts[ts.index < '2020-01-01'].asfreq('MS')
try:
    model = ExponentialSmoothing(ts, trend='add', seasonal=None).fit()
except Exception:
    model = None
if model:
    fut = model.forecast(6)
else:
    x = range(len(ts)); a, b = np.polyfit(x, ts.values, 1)
    fut = pd.Series(a*np.arange(len(ts), len(ts)+6)+b,
                    index=pd.date_range(ts.index[-1]+pd.offsets.MonthBegin(1), periods=6, freq='MS'))
fut.index = pd.date_range(ts.index[-1] + pd.offsets.MonthBegin(1), periods=6, freq='MS')

fig = go.Figure()
fig.add_trace(go.Scatter(x=ts.index, y=ts.values, name='Actual', mode='lines+markers'))
fig.add_trace(go.Scatter(x=fut.index, y=fut.values, name='Forecast',
                         mode='lines+markers', line=dict(dash='dash', color='red')))
fig.update_layout(title='6-Month Forecast', template='plotly_white', height=450)
save(fig, '05_forecast')

print('\n✅ All plots exported to', OUT)