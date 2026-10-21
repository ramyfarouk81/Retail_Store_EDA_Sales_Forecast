# 📊 Sales & Distribution — Analysis and Forecast

End-to-end exploratory data analysis (EDA) and 6-month sales forecast on an
electronics retail dataset (~186,000 order line items across 2019).

## 📌 Project Overview

| Item | Detail |
|------|--------|
| **Domain** | Retail / e-commerce sales |
| **Rows (clean)** | 185,950 |
| **Date range** | Jan 2019 – Dec 2019 |
| **Total revenue** | ~$34.5 M |
| **Unique orders** | ~178,000 |
| **Tools** | Python 3.11, pandas, plotly, statsmodels |
| **Environment** | Jupyter Notebook (EDA) + offline HTML exports |

---

## 🎯 Objectives

1. Understand **what** sells, **when**, and **where**.
2. Identify **high-revenue products**, **cities**, and **time patterns**.
3. Build a **6-month forecast** for the next period.
4. Export interactive dashboards for GitHub review.

---

## 🗂️ Data Preparation

| Step | Action |
|------|--------|
| 1 | Removed 545 repeated header rows (`Product == 'Order ID'`) |
| 2 | Coerced `Quantity Ordered` and `Price Each` to numeric |
| 3 | Parsed `Order Date` with explicit format `%m/%d/%y %H:%M` |
| 4 | Dropped the incomplete **Jan 2020** bucket (only $8,670) to avoid a false cliff in forecasting |
| 5 | Derived `Sales`, `Month`, `Hour`, `Weekday`, `City`, `State` |

---

## 📈 Graph Descriptions

Each plot in `plots/` is described below. Open the `.html` file to interact
(hover, zoom, filter).

### 🟦 01 — Monthly Sales Trend
**File:** `01_monthly_sales.png` / `.html`
**What it shows:** Total sales aggregated by month across 2019.
**Key insight:** Sales **peak in December ($4.61 M)** and dip in January ($1.81 M),
showing a clear Q4 holiday effect. A sudden drop to ~$8 K in Jan 2020 was
identified as an **incomplete data bucket** and removed before forecasting.

---

### 🟩 02 — Average Price per Product (Pillar Chart)
**File:** `02_price_pillars.png` / `.html`
**What it shows:** Bar chart of the average selling price per product,
sorted descending.
**Key insight:** Two clear tiers — **premium electronics** (Macbook Pro ~$1,700,
ThinkPad ~$1,000) vs **cheap accessories** (AA Batteries ~$3, USB-C Cable ~$12).
A box plot was rejected here because each product has a **single fixed price**,
making a bar chart the right visual.

---

### 🟨 03 — Top 10 Cities by Revenue
**File:** `03_top_cities.png` / `.html`
**What it shows:** Horizontal bar chart of revenue by city.
**Key insight:** **San Francisco, Los Angeles, and New York** dominate. These three
cities alone generate a disproportionate share of total revenue, making them
priority targets for stock and marketing spend.

---

### 🟪 04 — Sales by Hour and Weekday
**File:** `04_hour_weekday.png` / `.html`
**What it shows:** Two charts side-by-side — revenue per hour of day, and revenue
per weekday.
**Key insight:** Sales peak at **11:00–12:00 and 18:00–19:00** (lunch and after
work), which suggests running flash promotions during these windows.
Weekday patterns show **Tuesday and Wednesday** as the strongest days.

---

### 🟥 05 — 6-Month Sales Forecast
**File:** `05_forecast.png` / `.html`
**What it shows:** Historical monthly sales (blue, solid) plus a **6-month
projection** (red, dashed), fit using **Holt-Winters exponential smoothing**
(fallback to linear trend if statsmodels fails).
**Key insight:** The model predicts stable revenue in the **$2.5 M–$3.0 M range**
per month for the next six months — consistent with the 2019 average and
excluding the artificial Jan 2020 drop.

---

## 🧠 Conclusion

> The business generated **$34.5 M in 2019** from ~186 K line items across the US.
> Revenue is **highly concentrated** in a handful of premium products
> (Macbooks, iPhones, monitors) and a few coastal cities
> (SF, LA, NYC).
>
> **Seasonality is strong**: December revenue is ~2.5× January revenue, driven
> by holiday shopping. Sales also follow a daily rhythm with two clean peaks
> (lunch + early evening), which is a clear signal for time-targeted campaigns.
>
> The **6-month forecast** projects **$2.5 M–$3.0 M/month**, suggesting the
> business is stable but not growing without intervention. To push beyond the
> forecast, the highest-ROI actions would be:
>
> 1. **Bundle premium + accessory products** (iPhone + Lightning Cable already
>    pairs naturally) and discount the bundle instead of the device.
> 2. **Target Q4 marketing** around the November–December peak — inventory
>    planning should happen in September.
> 3. **Focus ad spend on SF, LA, and NYC**, where cart sizes are highest.
> 4. **Run lunch/evening promotions** (11–13 h and 18–20 h) to capture the
>    natural demand curve.
>
> **Data caveat:** The Jan 2020 row contained only a handful of orders and was
> excluded from the forecast to avoid biasing the model toward a false collapse.

---

## 🛠️ How to Run

```bash
# 1. Install dependencies
make install

# 2. Launch Jupyter
make notebook

# 3. Generate plots (from notebook or:)
make plots

# 4. Clean the data cache
make clean