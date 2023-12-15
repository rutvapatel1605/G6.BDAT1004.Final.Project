import requests
import pandas as pd

L = ['Mumbai/Mumbai-central', 'New-delhi/Connaught-place-(cp)']
lat_long = {'Mumbai': [18.9707028, 72.8194241], 'New-delhi': [28.6314512, 77.2166672]}
D = {"Name": [], "Rating": [], "Discount(%)": [], "CashBack": [], "Cost_for_Two(₹)": [], "City": [], "Locality": [],
     "Home_Delivery": [], "Manu_Count": []}
a = 14

for l in L:
    city, locality = l.split('/')
    
    for pg_no in range(1, 410):
        base_url = f'https://webapi.magicpin.in/search/app/universal/search/v6?suggestion_id=Food+and+Beverages&query=emptyQuery&longitude={lat_long[city][1]}&versionCode=5001&offset={a}&search_tab=STORES&latitude={lat_long[city][0]}&rows=14&sort=distance%3Aasc&oldFilter=use_magicpoints_v1&country=India&utm_campaign=%24search&suggestion_type=MERCHANTCATEGORYL1&collapse=true'
        referer_url = f'https://magicpin.in/india/{l}/Restaurant/'

        headers = {
            'authority': 'magicpin.in',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://magicpin.in',
            'referer': referer_url,
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        json_data = {
            'apiUrl': base_url,
            'queryString': '',
            'isAroundPage': True,
            'pageName': 'aroundyou',
        }

        response = requests.post('https://magicpin.in/sam-api/universal-search-v6/', headers=headers, json=json_data)

        data = response.json()
        storage = data['results']['STORES']

        def name():
            for strg in storage:
                n = strg['name']
                D['Name'].append(n)

        def rating():
            for strg in storage:
                rating = strg['rating']
                D['Rating'].append(rating)

        def disc():
            for strg in storage:
                dis = strg['cashback_percent']
                D['Discount(%)'].append(dis)

        def avg_spent():
            for strg in storage:
                avg_spent_value = strg.get('avg_spent', None)

                if avg_spent_value and '₹' in avg_spent_value:
                    cf2 = avg_spent_value.strip('₹').strip().split()[0]
                    D['Cost_for_Two(₹)'].append(cf2)
                else:
                    D['Cost_for_Two(₹)'].append(None)

        def loocality():
            for strg in storage:
                lcl = strg['locality']
                D['Locality'].append(lcl)

        def hm_delivery():
            for strg in storage:
                hmd = strg['home_delivery_available']
                D['Home_Delivery'].append(hmd)

        def cshbck():
            for strg in storage:
                cb = strg['cashback_value']
                D['CashBack'].append(cb)

        def ct():
            for strg in storage:
                siti = strg['city']
                D['City'].append(siti)

        def manu():
            for strg in storage:
                mnc = strg['menu_image_count']
                D['Manu_Count'].append(mnc)

        name()
        rating()
        disc()
        avg_spent()
        loocality()
        hm_delivery()
        cshbck()
        ct()
        manu()
        a += 14

magicpin = pd.DataFrame.from_dict(D)
print(magicpin)
magicpin.to_csv("data.csv")
