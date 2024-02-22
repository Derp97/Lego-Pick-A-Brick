import csv

import requests

from product_dataclass import Part
from query_txt import query_txt

fieldnames = ["id", "name", "in_stock", "variant_id", "variant_price_raw", "variant_price_formatted",
              "attr_design_number", "attr_colour_id", "attr_del_channel", "attr_system_name", "img_url"]


def product_json_request(page: int, results_amt: int):
    if page == 1:
        variables = {"input": {"perPage": results_amt, "system": ["LEGO", "TECHNIC"]}}
    else:
        variables = {"input": {"perPage": results_amt, "system": ["LEGO", "TECHNIC"], "page": page}}

    url = 'https://www.lego.com/api/graphql/PickABrickQuery'
    headers = {'Content-Type': 'application/json', 'X-Locale': 'en-GB'}
    data = {
        "operationName": "PickABrickQuery",
        "variables": variables,
        "query": query_txt
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def product_json_parser(response) -> list:

    list_of_items = []

    for items in response["data"]["elements"]["results"]:
        items = Part(
            id=items["id"],
            name=items["name"],
            in_stock=items["inStock"],
            variant_id=items["variant"]["id"],
            variant_price_raw=items["variant"]["price"]["centAmount"],
            variant_price_formatted=items["variant"]["price"]["formattedAmount"],
            attr_design_number=items["variant"]["attributes"]["designNumber"],
            attr_colour_id=items["variant"]["attributes"]["colourId"],
            attr_del_channel=items["variant"]["attributes"]["deliveryChannel"],
            attr_system_name=items["variant"]["attributes"]["system"],
            img_url=f'www.lego.com/cdn/product-assets/element.img.lod5photo.192x192/{items["variant"]["id"]}.jpg'
        )
        list_of_items.append(items)

    return list_of_items


def file_output(data: list):
    with open('lego.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for item in data:
            writer.writerow(item.__dict__)
    pass


if __name__ == '__main__':
    with open('lego.csv', mode='w', newline='') as init_file:
        init_writer = csv.DictWriter(init_file, fieldnames=fieldnames)
        init_writer.writeheader()

    page_number = 1
    per_page = 500  # 500 is the maximum per_page allowed
    total_results = 0

    while True:
        resp = product_json_request(page_number, per_page)
        total_count = resp["data"]["elements"]["total"]
        print("Total Count : ", total_count)

        total_results += resp["data"]["elements"]["count"]
        print("Total Results : ", total_results)

        list_items = product_json_parser(resp)
        print(list_items)

        file_output(list_items)

        if total_results >= resp["data"]["elements"]["total"]:
            break
        print("Page Num : ", page_number, "\n ----------------------")
        page_number += 1
