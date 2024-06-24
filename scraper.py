# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# %%
output_path = "output"
datestring = dt.datetime.now().strftime("%Y%m%d")
# %%
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "DNT": "1",
    "Sec-GPC": "1",
    "Priority": "u=1",
}

response = requests.get(
    "https://www.moneyweb.co.za/tools-and-data/jse-search/", headers=headers
)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find(id="cac-search-table-list")
rows = table.find_all("tr")

tickers = []
row_output = []
for row in rows:
    if row.find("a"):
        cols = row.find_all("td")
        row_data = []
        for col in cols:
            link = col.find("a")
            text = col.text.strip()
            if text:
                row_data.append(text)
            if link and "href" in link.attrs:
                tickers.append(link["href"].split("/")[-2])
        row_output.append(row_data)
pd.DataFrame(row_output).to_csv(
    "{}/sector/{}_sector.csv".format(output_path, datestring)
)
# %%

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "*/*",
    "Accept-Language": "en-GB,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.moneyweb.co.za",
    "Connection": "keep-alive",
    "Referer": "https://www.moneyweb.co.za/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "DNT": "1",
    "Sec-GPC": "1",
}
# %%
data = {
    "action": "load_snapshots",
    "codes[]": tickers,
    "type": "clickacompany",
}

response = requests.post(
    "https://cache.moneyweb.co.za/mny-snapshots.php", headers=headers, data=data
)
prices_output = pd.DataFrame(response.json())
prices_output.to_csv("{}/prices/{}.csv".format(output_path, datestring))
