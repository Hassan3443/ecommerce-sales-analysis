import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------------------
# Load dataset
# ---------------------------------------

current_path = os.path.dirname(__file__)
file_path = os.path.join(current_path, "Amazon Sale Report.csv")

df = pd.read_csv(file_path, low_memory=False)

# ---------------------------------------
# Initial exploration
# ---------------------------------------

print("\nColumns in dataset:\n")
print(df.columns)

print("\nMissing values:\n")
print(df.isnull().sum())

# ---------------------------------------
# Data cleaning
# ---------------------------------------

df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')

# Remove cancelled orders
df = df[df['Status'] != 'Cancelled']

# Drop rows with missing important values
df = df.dropna(subset=['Amount', 'Category', 'ship-state'])

# ---------------------------------------
# Feature engineering
# ---------------------------------------

df['Month_Name'] = df['Date'].dt.month_name()

# ---------------------------------------
# Sales analysis
# ---------------------------------------

total_sales = df['Amount'].sum()
print("\nTotal Sales:", round(total_sales, 2))

# Top Categories (by Revenue)
top_categories = (
    df.groupby('Category')['Amount']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop Categories by Revenue:\n")
print(top_categories)

# Monthly Sales
monthly_sales = df.groupby('Month_Name')['Amount'].sum()

month_order = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]

monthly_sales = monthly_sales.reindex(month_order).dropna()

print("\nMonthly Sales:\n")
print(monthly_sales)

# Top States (by Revenue)
top_states = (
    df.groupby('ship-state')['Amount']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop States by Revenue:\n")
print(top_states)

# ---------------------------------------
# Visualization (Styled)
# ---------------------------------------

plt.style.use('seaborn-v0_8')

# -------- Top Categories --------
plt.figure(figsize=(10,6))

bars = top_categories.plot(kind='bar', color='#4CAF50')

plt.title("Top 10 Categories by Revenue", fontsize=14, weight='bold')
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add values on bars
for i, v in enumerate(top_categories):
    plt.text(i, v, f'{int(v/1e6)}M', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# -------- Monthly Sales --------
plt.figure(figsize=(10,6))

monthly_sales.plot(marker='o', linewidth=3, color='#2196F3')

plt.title("Monthly Revenue Trend (2022)", fontsize=14, weight='bold')
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.grid(True, linestyle='--', alpha=0.6)

# Add values
for i, v in enumerate(top_states.sort_values()):
    plt.text(v, i, f'{int(v/1e6)}M', va='center')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------- Top States --------
plt.figure(figsize=(10,6))

top_states.sort_values().plot(kind='barh', color='#FF9800')

plt.title("Top 10 States by Revenue", fontsize=14, weight='bold')
plt.xlabel("Revenue")
plt.ylabel("State")

plt.grid(axis='x', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()