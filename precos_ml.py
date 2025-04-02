import requests
from pprint import pprint


def main():
    access_token = get_access_token()
    product_name = "switch oled"
    products = search_product(access_token, product_name, 5)
    
    product_market_data = []
    for item, name in products.items():
        search_data = search_items(access_token, item, name, 10)

def get_access_token():
    refresh_token = 'TG-67e721d2aa3540000124c846-230655983'

    url = "https://api.mercadolibre.com/oauth/token"

    payload = f'grant_type=refresh_token&client_id=1878666561750588&client_secret=DWGMmnHmeTbi7XtD17R3wpP3Lcct8KtF&refresh_token={refresh_token}'
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response['access_token']


def search_product(access_token, product_name, limit=10):
    # limit includes blank requests
    url = f"https://api.mercadolibre.com/products/search?status=active&site_id=MLB&q={product_name}&limit={limit}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    
    results_list = dict()
    for row in response['results']:
        results_list.update({row['id']: row['name']})

    return results_list


def search_items(access_token, product_id, product_name='', limit=5):
    # limit of items per product searched
    url = f"https://api.mercadolibre.com/products/{product_id}/items"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    search_data = []
    if 'error' not in response and (result_count := len(response['results'])) != 1:
        if limit >= result_count:
            max_limit = result_count
        else:
            max_limit = limit
        
        i = 0
        while i < max_limit:
            data = {
                'product_name': product_name,
                'product_id': product_id,
                'price': response['results'][i]['price'],
                'original_price': response['results'][i]['original_price'],
                'seller_id': response['results'][i]['seller_id'],
                'free_shipping': response['results'][i]['shipping']['free_shipping'],
                'warranty': response['results'][i]['warranty']
            }
            i += 1
            search_data.append(data)
    
    pprint(search_data)
    return search_data


if __name__ == "__main__":
    main()