This repository contains Python codes for conducting fundamental analysis in the financial domain. The codes are designed to analyze various fundamental factors and metrics to evaluate the financial health and performance of companies.

Table of Contents
Introduction
Installation
Usage
Features
Contributing
License

Introduction
The fundamental analysis Python codes in this repository aim to provide tools and functions for analyzing financial data and performing fundamental analysis on companies. These codes can be used to evaluate key fundamental factors, calculate financial ratios, and generate insights for investment decision-making.

Installation
To use the fundamental analysis Python codes, follow these steps:

git clone https://github.com/your-username/fundamental-analysis-python.git
```
git clone https://github.com/your-username/fundamental-analysis-python.git
```

Install the required dependencies by running the following command:
basic
pip install -r requirements.txt
```

Usage
The fundamental analysis Python codes can be used as standalone scripts or imported as modules into your own projects. Here are some examples of how to use the codes:

# Calculate financial ratios
pe_ratio = companyOverview['trailingPE']
peg_ratio = companyOverview['pegRatio']
beta = companyOverview['beta']
MA_50 = stock.history(period='50d')['Close'].mean()
MA_200 = stock.history(period='200d')['Close'].mean()

#Compare the income and expenese
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
income_vs_expense = ((incomeStmt['totalRevenue'] / incomeStmt['totalOperatingExpense']) - 1).mean()
print(f"Income vs Expense Ratio: {income_vs_expense}")

#Calculate the profit and loss
fig3, ax = plt.subplots(figsize=(15.93, 3))
cashflow['totalCashFromOperatingActivities'].plot(kind='bar', color=cashflow['totalCashFromOperatingActivities'].apply(lambda x: 'g' if x > 0 else 'r'), ax=ax)
ax.set_ylabel('USD')
plt.title("Profit/Loss Chart")
plt.show()

# Calculate and display profit/loss ratio
pnl = (cashflow['totalCashFromOperatingActivities'] > 0).mean()
print(f"Profit/Loss Ratio: {pnl}")

Features
The fundamental analysis Python codes in this repository offer the following key features:

1. Calculation of various financial ratios, including profitability ratios, liquidity ratios, and efficiency ratios.
2. Data preprocessing and cleaning functions to handle missing values, outliers, and inconsistencies.
3. Visualization functions to generate plots and charts for financial data analysis.
4. Integration with external APIs or data sources to fetch financial data for analysis.


