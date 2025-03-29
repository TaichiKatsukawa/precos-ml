import requests
from pprint import pprint


def main():
    access_token = get_access_token()
    product_name = "DJI action 4"
    products = search_product(access_token, product_name)
    
    for item, name in products.items():
        search_items(access_token, item, name)

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


def search_product(access_token, product_name):
    url = f"https://api.mercadolibre.com/products/search?status=active&site_id=MLB&q={product_name}&limit=50"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    
    results_list = dict()
    for row in response['results']:
        results_list.update({row['id']: row['name']})

    return results_list


def search_items(access_token, product_id, product_name=''):
    url = f"https://api.mercadolibre.com/products/{product_id}/items"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    if 'error' not in response:
        print(f'{product_name} [{product_id}]')
        print(f"Preço: {response['results'][0]['price']}")
    
    #pprint(response)


if __name__ == "__main__":
    main()