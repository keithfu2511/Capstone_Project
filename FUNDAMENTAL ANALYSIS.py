import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from newsapi import NewsApiClient
from rich.console import Console
from rich.markdown import Markdown

NEWS_API = "91a737ebd85f43e9bc86f807d11c909f"
AV_API = "S91CFWX47K68FVB0"

TICKER = 'CAT'                           # Here I've put the symbol for Apple, please change it for your analysis

companyOverview = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={TICKER}&apikey={AV_API}').json()
incomeStmt = requests.get(f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={TICKER}&apikey={AV_API}').json()
balanceSheet = requests.get(f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={TICKER}&apikey={AV_API}').json()
cashflow = requests.get(f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={TICKER}&apikey={AV_API}').json()

print(f"Analysing {companyOverview['Name']}, {companyOverview['Address']}\n{companyOverview['Description']}")
pe_ratio = float(companyOverview['PERatio'])
peg_ratio = float(companyOverview['PEGRatio'])
pe_ratio = float(companyOverview['PERatio'])
beta = float(companyOverview['Beta'])
MA_50 = float(companyOverview['50DayMovingAverage'])
MA_200 = float(companyOverview['200DayMovingAverage'])

annual_incomes = pd.DataFrame.from_records(incomeStmt['annualReports'])
annual_incomes.set_index('fiscalDateEnding', inplace=True)
annual_incomes = annual_incomes.apply(pd.to_numeric, errors='coerce')
annual_incomes.dropna(axis=1, inplace=True)
annual_incomes

annual_balances = pd.DataFrame.from_records(balanceSheet['annualReports'])
annual_balances.set_index('fiscalDateEnding', inplace=True)
annual_balances = annual_balances.apply(pd.to_numeric, errors='coerce')
annual_balances.dropna(axis=1, inplace=True)
annual_balances

annual_cashflow = pd.DataFrame.from_records(cashflow['annualReports'])
annual_cashflow.set_index('fiscalDateEnding', inplace=True)
annual_cashflow = annual_cashflow.apply(pd.to_numeric, errors='coerce')
annual_cashflow.dropna(axis=1, inplace=True)
annual_cashflow

MARKDOWN = f"""
# P/E Ratio : {pe_ratio} \t PEG Ratio: {peg_ratio} \t Beta : {beta} \n # Signal 1: {'BUY (50 day Moving Average is above 200 day)' if MA_50 > MA_200 else 'SELL (50 day Moving Average is below 200 day)'} 

"""

console = Console()
md = Markdown(MARKDOWN)
console.print(md)

fig1 = plt.figure(figsize=(15, 3))
plt.plot(annual_incomes.index, annual_incomes.operatingIncome, label='Annual Operating Income (Left scale)', c='g')
ax = fig1.axes[0]
ax2 = ax.twinx()
ax2.plot(annual_incomes.index, annual_incomes.operatingExpenses, label='Annual Operating Expense (Right scale)', c='r')
_ = plt.title("Income vs Expense Chart")
ax.legend(loc='lower left')
ax2.legend(loc='upper right')
ax.annotate('Both income and Expense increasing, but income scale is larger than expense', xy=('2021-09-30', 1.2e11),
           xytext=('2020-09-30', 0.9e11), arrowprops=dict(facecolor='black', shrink=0.05), bbox=dict(boxstyle='round', fc='0.8'))
ax.set_ylabel('USD')
ax2.set_ylabel('USD')

income_vs_expense = ((annual_incomes.operatingIncome / annual_incomes.operatingExpenses) - 1).mean()

width = 0.25
multiplier = 0
date_list = None
fig2, ax = plt.subplots(layout='constrained', figsize=(12.75, 3))
for attr in annual_balances[['totalAssets', 'totalLiabilities']].items():
    offset = width * multiplier
    if date_list is None:
        date_list = attr[1].index.tolist()
    x = np.arange(len(date_list))
    rects = ax.bar(x + offset, attr[1].values.tolist(), width, label=attr[0])
    # ax.bar_label(rects, padding=3)
    multiplier += 1
ax.set_ylabel('USD')
ax.set_title("Gross Profit Chart")
ax.set_xticks(x + width/2, date_list)
ax.legend(loc='upper right')
plt.show()

asset_vs_liability = ((annual_balances.totalAssets / annual_balances.totalLiabilities) - 1).mean()

fig3 = plt.figure(figsize=(15.93, 3))
rects = plt.bar(annual_cashflow.index, annual_cashflow.profitLoss, label='Profit/Loss')
ax = fig3.axes[0]
_ = ax.bar_label(rects, padding=3)

pnl = (annual_cashflow['profitLoss'] > 0).mean()

signals = np.mean([sg > 0 for sg in [pnl, asset_vs_liability, income_vs_expense]])

if signals > 0.5:
    console = Console()
    md = Markdown(f"# Signal 2: {'BUY'}")
    console.print(md)
else:
    console = Console()
    md = Markdown(f"# Signal 2: {'SELL'}")
    console.print(md)

newsapi = NewsApiClient(api_key=NEWS_API)

news_object = newsapi.get_everything(q=Caterpillar,
                                      from_param='2023-10-09',
                                      language='en',
                                      sort_by='relevancy')

all_articles = pd.DataFrame.from_records(news_object['articles'])
all_articles.head()

for desc in all_articles['description'].values[:10]:
    print(f"====================\n{desc}")

newsAndSentiment = requests.get(
    f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={TICKER}&apikey={AV_API}').json()

newsdf = pd.DataFrame.from_records(newsAndSentiment['feed'])
newsdf.head()

overall_sentiment_score = np.mean(newsdf['overall_sentiment_score'])

if overall_sentiment_score > 0.15:
    console = Console()
    md = Markdown(f"# Signal 3: {'BUY'}")
    console.print(md)
elif overall_sentiment_score < 0.15 and overall_sentiment_score > -0.15:
    console = Console()
    md = Markdown(f"# Signal 3: {'HOLD'}")
    console.print(md)
else:
    console = Console()
    md = Markdown(f"# Signal 3: {'SELL'}")
    console.print(md)

print