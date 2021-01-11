import ssl

import pandas as pd

# remove validation for ssl
ssl._create_default_https_context = ssl._create_unverified_context

import shopify

# request shop_url
shop_url = 'https://cbc3e9686911d1cadbce71005e884660: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@shopcider.myshopify.com' \
           '/admin '
shopify.ShopifyResource.set_site(shop_url)

# create attributes we need
wrong_id = []
its_stock_quantity = []
its_stock_state = []


# method to select unmatched id and corresponding stock quantity, stock state of a single product
def get_wrong_sku(product):
    product_html = str(product.body_html).replace(" ", "").replace("\n", "")
    for i in range(len(product.variants)):
        quantity = product.variants[i].inventory_quantity
        color = str(product.variants[i].option1)
        size = str(product.variants[i].option2)
        string_found = color + "-" + size + "</td><td>"
        if quantity > 0:
            if product_html.find(string_found + "Outof stock") != -1:
                wrong_id.append(product.variants[i].sku)
                its_stock_quantity.append(quantity)
                its_stock_state.append("out of stock")
        else:
            if product_html.find(string_found + "Instock") != -1:
                wrong_id.append(product.variants[i].sku)
                its_stock_quantity.append(quantity)
                its_stock_state.append("in stock")


# traverse all products
page = shopify.Product.find()
while True:
    for prod in page:
        get_wrong_sku(prod)
    if page.has_next_page():
        page = page.next_page()
    else:
        break

# output results into a csv file
test_dict = {'sku': wrong_id, 'stock quantity': its_stock_quantity, 'stock state': its_stock_state}
output_df = pd.DataFrame(test_dict)
output_df.to_csv("./output.csv")
