import requests
import pandas as pd 

url = "https://cuuo4s.a.searchspring.io/api/search/search.json"

link = []
all_links = []
ba = pd.read_csv('page1.csv')
for i in range(2,5):

    querystring = {"ajaxCatalog":"v3","resultsFormat":"native","siteId":"cuuo4s","domain":"https://houseofrohl.com/rohl/bathroom/faucets/?page=2","bgfilter.categories_hierarchy":"ROHL>bathroom>faucets","q":"","page":f"{i}","userId":"0a40a54f-2ea5-4b9d-b3c3-35cd54ccc8c6","sessionId":"e5f83710-c03e-46fc-9acb-68116cb61508","pageLoadId":"368d13ce-7bce-403f-8d6d-cfc2720c13a6","lastViewed":"CU354LAPC2","bgfilter.ss_disabled":"0"}

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
    r = response.json()
    ad = r.get('results')

    df = pd.json_normalize(ad)
    df['json'] = df['json'].str.replace("&quot;", '"')
    json_data = df['json'].apply(eval)
    normalized_df = pd.json_normalize(json_data.explode().tolist())
    normalized_df['links'] = 'https://houseofrohl.com' + normalized_df['product_url']
    ls = normalized_df["links"] 
    
    # Append the links to the list
    all_links.extend(normalized_df['links'])

# Convert the list to a DataFrame and save it to CSV
final_df = pd.DataFrame(all_links, columns=['links'])
allink = pd. concat([ba ,final_df])
allink.to_csv('final.csv', index=False)