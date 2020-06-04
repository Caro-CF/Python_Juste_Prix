#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json
from flask import Flask, render_template,request

app = Flask(__name__)

##Page accueil##
@app.route('/')
def home():
    return render_template("home.html", message = "Bienvenue dans le jeux du juste prix, entrer un prix")

def json_api():
    # global price

    url = "https://api.cdiscount.com/OpenApi/json/Search"
    params = {
        "ApiKey": "23b7aa67-4725-4f50-bdb5-a3b3a70bc33c",
        "SearchRequest": {
            "Keyword": "tablette",
            "SortBy": "relevance",
            "Pagination": {
                "ItemsPerPage": 5,
                "PageNumber": 0
            },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": 400
                },
                "Navigation": "computers",
                "IncludeMarketPlace": "false",
            }
        }
    }

    r = requests.post(url, data=json.dumps(params))
    price = json.loads(r.text)['Products'][0]['BestOffer']['SalePrice']

    print(r.text)
    print(price)

    return price


##Jeux du juste Prix##
@app.route('/', methods=['POST'])
def just_price():
    p = json_api()
    print("p =" +p)

    if request.method == 'POST':
        nb = request.form['rep_user']

        price_user = float(nb)
        price_object = float(p)

        if price_user < price_object:
            return render_template("home.html", message = "C'est plus !")
        elif price_user > price_object:
            return render_template("home.html", message="C'est moins !")
        elif price_user == price_object:
            return render_template("home.html", message="Bravo")

    return render_template("home.html")


if __name__ == "__main__":
    app.run()
