import yfinance as yf
import finviz
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.markdown import Markdown

# Set the ticker symbol
TICKER = 'AAPL'

# Fetch financial data using yfinance
stock = yf.Ticker(TICKER)
companyOverview = stock.info
incomeStmt = stock.quarterly_financials.loc['Total Revenue']
balanceSheet = stock.quarterly_balance_sheet.loc['Total Assets':'Total Liabilities']
cashflow = stock.quarterly_cashflow.loc['Total Cash From Operating Activities']

# Display company overview
print(f"Analyzing {companyOverview['shortName']}, {companyOverview['address1']}\n{companyOverview['longBusinessSummary']}")

# Calculate financial ratios
pe_ratio = companyOverview['trailingPE']
peg_ratio = companyOverview['pegRatio']
beta = companyOverview['beta']
MA_50 = stock.history(period='50d')['Close'].mean()
MA_200 = stock.history(period='200d')['Close'].mean()

# Display financial ratios
print(f"P/E Ratio: {pe_ratio}\tPEG Ratio: {peg_ratio}\tBeta: {beta}")
print(f"Signal 1: {'BUY' if MA_50 > MA_200 else 'SELL'}")

# Plot income vs expense
fig1, ax1 = plt.subplots(figsize=(15, 3))
ax1.plot(incomeStmt.index, incomeStmt['totalRevenue'], label='Total Revenue', color='g')
ax2 = ax1.twinx()
ax2.plot(incomeStmt.index, incomeStmt['totalOperatingExpense'], label='Total Operating Expense', color='r')
ax1.set_ylabel('USD')
ax2.set_ylabel('USD')
ax1.legend(loc='lower left')
ax2.legend(loc='upper right')
plt.title("Income vs Expense Chart")
plt.show()

# Calculate and display income vs expense ratio
income_vs_expense = ((incomeStmt['totalRevenue'] / incomeStmt['totalOperatingExpense']) - 1).mean()
print(f"Income vs Expense Ratio: {income_vs_expense}")

# Plot gross profit chart
fig2, ax = plt.subplots(figsize=(12.75, 3))
balanceSheet[['totalAssets', 'totalLiabilities']].plot(kind='bar', width=0.25, ax=ax)
ax.set_ylabel('USD')
ax.set_title("Gross Profit Chart")
plt.show()

# Calculate and display asset vs liability ratio
asset_vs_liability = ((balanceSheet['totalAssets'] / balanceSheet['totalLiabilities']) - 1).mean()
print(f"Asset vs Liability Ratio: {asset_vs_liability}")

# Plot profit/loss chart
fig3, ax = plt.subplots(figsize=(15.93, 3))
cashflow['totalCashFromOperatingActivities'].plot(kind='bar', color=cashflow['totalCashFromOperatingActivities'].apply(lambda x: 'g' if x > 0 else 'r'), ax=ax)
ax.set_ylabel('USD')
plt.title("Profit/Loss Chart")
plt.show()

# Calculate and display profit/loss ratio
pnl = (cashflow['totalCashFromOperatingActivities'] > 0).mean()
print(f"Profit/Loss Ratio: {pnl}")

# Analyze signals
signals = (pnl + asset_vs_liability + income_vs_expense) / 3

# Display Signal 2
console = Console()
md = Markdown(f"# Signal 2: {'BUY' if signals > 0.5 else 'SELL'}")
console.print(md)

# Fetch news sentiment using finviz
news_sentiment = finviz.get_news(TICKER)

# Calculate overall sentiment score
overall_sentiment_score = news_sentiment['sentiment'].mean()

# Display Signal 3
console = Console()
if overall_sentiment_score > 0.15:
    md = Markdown("# Signal 3: BUY")
elif -0.15 <= overall_sentiment_score <= 0.15:
    md = Markdown("# Signal 3: HOLD")
else:
    md = Markdown("# Signal 3: SELL")
console.print(md)
