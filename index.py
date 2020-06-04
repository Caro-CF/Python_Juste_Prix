#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import requests, json
from flask import Flask, render_template, flash, request


app = Flask(__name__)
app.secret_key = 'oh flash oh oh !'

##Page accueil##
@app.route('/')
def home():
    flash("testing", "messages")
    # n = random.randint(0, 100)  # rempplacer par liens api

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

    return render_template("home.html", json="JsOn")


##Jeux du juste Prix##
@app.route('/', methods=['POST'])
def just_price():

    if request.method == 'POST':
        nb = request.form['rep_user']
        p = 15

        while True:
            var = int(nb)
            if var < p:
                return render_template("home.html", message = "C'est plus !")
            else:
                return render_template("home.html", message = "C'est moins !")
            if var == p:
                return render_template("home.html",  message = "Bravo")
                break

    return render_template("home.html")



if __name__ == "__main__":
    app.run()
