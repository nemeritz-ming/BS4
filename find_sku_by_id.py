import ssl
from bs4 import BeautifulSoup
import pandas as pd

# remove validation for ssl
ssl._create_default_https_context = ssl._create_unverified_context

import shopify

# request shop_url
shop_url = 'https://cbc3e9686911d1cadbce71005e884660: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@shopcider.myshopify.com/admin'
shopify.ShopifyResource.set_site(shop_url)

# create attributes we need
wrong_id = []

# find the product the size table
def find_sku(product):
    try:
        soup = BeautifulSoup(product.body_html, features="lxml")
        match = soup.find('div', id='goods_size_table')
        if match is None:
            wrong_id.append(product.title)
    except Exception as e:
        pass


page = shopify.Product.find()

# traverse all products
while True:
    for prod in page:
        find_sku(prod)
    if page.has_next_page():
        page = page.next_page()
    else:
        break


# output results into an excel file
test_dict = {'title': wrong_id}
output_df = pd.DataFrame(test_dict)
output_df.to_excel('./title_without_table.xlsx')
