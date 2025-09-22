import pandas as pd
import requests
import time as t
import random

col_list_url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/SBER.json?from=2024-06-14&till=2024-06-14'
r = requests.get(col_list_url).json()
col = r['history']['columns']
data = pd.DataFrame(columns=col)
t.sleep(0.5)
url_div = 'https://iss.moex.com/iss/securities/SBER/dividends.json?from=2023-01-01&till=2023-01-01'
r = requests.get(url_div).json()
col_div = r['dividends']['columns']
data_div = pd.DataFrame(columns=col_div)
t.sleep(0.5)
url_emis = f"https://iss.moex.com/iss/securities/SBER/corporateactions.json?from=2023-01-01&till=2023-01-01"
r = requests.get(url_emis).json()
col_emis = r['description']['columns']
col_emis.append('date')
col_emis.append('ticket')
data_emis = pd.DataFrame(columns=col_emis)
t.sleep(0.5)

tickets = list(pd.read_csv("C:\\Users\\olesh\\Desktop\\котировки\\мусор\\уникальные.csv")['0'])
tickets = tickets[98:]
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

for ticket in tickets:
    print(ticket)
    for year in range(2010, 2026):
        time_waite = 0.3
        for month in range(1, 13):
            month_format = str(month)
            month_format_plus = str(month + 1)
            if len(month_format) == 1:
                month_format = '0' + month_format
            if len(month_format_plus) == 1:
                month_format_plus = '0' + month_format_plus


            url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/{ticket}.json?from={year}-{month_format}-01&till={year}-{month_format_plus}-01'
            url_div = f'https://iss.moex.com/iss/securities/{ticket}/dividends.json?from={year}-{month_format}-01&till={year}-{month_format_plus}-01'
            url_emis = f"https://iss.moex.com/iss/securities/{ticket}/corporateactions.json?from={year}-{month_format}-01&till={year}-{month_format_plus}-01"

            headers = {'User-Agent': random.choice(user_agents)}
            while True:
                try:
                    response_div = requests.get(url_div, headers=headers, timeout=10)
                    t.sleep(time_waite)

                    response = requests.get(url, headers=headers, timeout=10)

                    response_emis = requests.get(url_emis, headers=headers, timeout = 10)

                    t.sleep(time_waite)
                    status = response.status_code
                    status_div = response_div.status_code
                    status_emis = response_emis.status_code

                    response = response.json()
                    element = response['history']['data']
                    response_div = response_div.json()
                    element_div = response_div['dividends']['data']
                    response_emis = response_emis.json()
                    element_emis = response_emis['description']['data'][6]

                    element_emis.append(ticket)
                    element_emis.append(f'{year}-{month_format}-01')

                    print(element)

                    df = pd.DataFrame(element, columns=col)
                    df_div = pd.DataFrame(element_div, columns=col_div)
                    df_emis = pd.DataFrame([element_emis], columns=col_emis)
                    data = pd.concat([data, df])
                    data_div = pd.concat([data_div, df_div])
                    data_emis = pd.concat([data_emis, df_emis])
                    time_waite = 0.3
                    break



                except (requests.exceptions.RequestException, KeyError, IndexError, ValueError):
                    data.to_csv("C:\\Users\\olesh\\Desktop\\data5.csv", index=False)
                    data_div.to_csv("C:\\Users\\olesh\\Desktop\\data_div5.csv", index=False)
                    data_emis.to_csv("C:\\Users\\olesh\\Desktop\\data_emis5.csv", index=False)
                    print('Ошибка  запроса', ticket)
                    t.sleep(15)
                    time_waite = time_waite + 1




            if month_format_plus == '13':
                break
data.to_csv("C:\\Users\\olesh\\Desktop\\data5.csv", index=False)
data_div.to_csv("C:\\Users\\olesh\\Desktop\\data_div5.csv", index=False)
data_emis.to_csv("C:\\Users\\olesh\\Desktop\\data_emis5.csv", index=False)
