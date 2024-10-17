import requests
import pandas as pd 

url = "https://cuuo4s.a.searchspring.io/api/search/search.json"

link =[]

querystring = {"ajaxCatalog":"v3","resultsFormat":"native","siteId":"cuuo4s","domain":"https://houseofrohl.com/rohl/bathroom/faucets/","bgfilter.categories_hierarchy":"ROHL>bathroom>faucets","q":"","userId":"0a40a54f-2ea5-4b9d-b3c3-35cd54ccc8c6","sessionId":"e5f83710-c03e-46fc-9acb-68116cb61508","pageLoadId":"35f78391-a5a2-4e20-9986-ba1f62d3cd0f","lastViewed":"CU354LAPC2","bgfilter.ss_disabled":"0"}

payload = ""
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://houseofrohl.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://houseofrohl.com/",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
r = response.json()
ad = r.get('results')

df = pd.json_normalize(ad)
df['json'] = df['json'].str.replace("&quot;", '"')
json_data = df['json'].apply(eval)
normalized_df = pd.json_normalize(json_data.explode().tolist())
normalized_df['links'] = 'https://houseofrohl.com' + normalized_df['product_url']
print(normalized_df["links"])
normalized_df['links'].to_csv('page1.csv', index= False)
# print(response.text)