#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, random
from flask import Flask, render_template, request

app = Flask(__name__)

try_list = []
product_infos = ()
some_keywords = ["tablette", "tv", "television", "livre", "smartphone", "four", "cd", "casque", "clavier"]
random_keyword = some_keywords[random.randint(0, len(some_keywords)-1)]
random_max_price = random.randint(0, 499)

##Appel de l'API##
def json_api(keyword, max_price):
    # global price
    url = "https://api.cdiscount.com/OpenApi/json/Search"
    params = {
        "ApiKey": "23b7aa67-4725-4f50-bdb5-a3b3a70bc33c",
        "SearchRequest": {
            "Keyword": keyword,
            "SortBy": "relevance",
            "Pagination": {
                "ItemsPerPage": 5,
                "PageNumber": 0
            },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": max_price
                },
                "Navigation": "computers",
                "IncludeMarketPlace": "false",
            }
        }
    }
    r = requests.post(url, data=json.dumps(params))
    random_index = random.randint(0,len(json.loads(r.text))-1)
    price = json.loads(r.text)['Products'][random_index]['BestOffer']['SalePrice']
    image = json.loads(r.text)['Products'][random_index]['MainImageUrl']
    name = json.loads(r.text)['Products'][random_index]['Name']

    return name, image, price

##Page accueil##
@app.route('/')
def home():
    global product_infos
    message = "Bienvenue dans le jeux du juste prix, deviner le prix de ce produit !"
    try_list = []
    product_infos = json_api(random_keyword, random_max_price)
    return show_render(message, try_list)

##Gestion des messages##
def show_render(message, try_list):
    name = product_infos[0]
    image = product_infos[1]
    return render_template("home.html", name=name, image=image, message=message, try_list=try_list)




##Jeux du juste Prix##
@app.route('/', methods=['POST'])
def just_price():
    price_object = int(float(product_infos[2]))

    if request.method == 'POST':
        price_user = int(request.form['rep_user'])

        if price_user < price_object:
            message = "C'est plus !"
            try_list.append(str(price_user) + " : " + message)
            return show_render(message, try_list)
        elif price_user > price_object:
            message = "C'est moins !"
            try_list.append(str(price_user) + " : " + message)
            return show_render(message, try_list)
        elif price_user == price_object:
            message = "Bravo, c'est bien " + str(price_user) + " € !"
            return show_render(message, try_list)

    return render_template("home.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
