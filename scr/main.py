# coding=utf-8
import requests
from flask import Flask, abort

app = Flask(__name__)

BASE_API_URL = "https://randomuser.me/api/"


def parse_result(input_json):
    data = input_json["results"][0]
    result = {
        "title": data["name"]["title"],
        "firstname": data["name"]["first"],
        "lastname": data["name"]["last"],
        "street_address": " ".join([data["location"]["street"]["name"],
                                    str(data["location"]["street"]
                                        ["number"])]),
        "city": data["location"]["city"],
        "state": data["location"]["state"],
        "country": data["location"]["country"],
        "username": data["login"]["username"]
    }
    return result


@app.route("/")
def index():
    return "use /user endpoint"


@app.route("/user")
def user():
    result = requests.get(BASE_API_URL)
    if result.status_code != 200:
        abort(503)
    data = parse_result(result.json())
    return """{title} {firstname} {lastname} lives at {street_address}
    in {city}, {state}, {country}. Has logged in
    with username {username}""".format(**data)


app.run(host='0.0.0.0', port=5000)
