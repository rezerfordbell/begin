import json
import requests
from flask import Flask, abort
import werkzeug
app = Flask(__name__)


BASE_API_URL = "https://randomuser.me/api/"


def parse_result(input_json):
    data = input_json["results"][0]
    result = {
        "title": data["name"]["title"],
        "firstname": data["name"]["first"],
        "lastname": data["name"]["last"],
        "street_address": " ".join([data["location"]["street"]["name"],
                                    str(data["location"]["street"]["number"])]),
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
    return """{title} {firstname} {lastname} lives at {street_address} in {city}, {state}, {country}. Has logged in with username {username}""".format(**data)


def test_index():
    # это хуйня
    assert True == True


def test_parse_result():
    payload = """{"results":[{"gender":"female","name":{"title":"Ms","first":"Kübra","last":"Süleymanoğlu"},"location":{"street":{"number":8563,"name":"Mevlana Cd"},"city":"Gümüşhane","state":"Bilecik","country":"Turkey","postcode":77474,"coordinates":{"latitude":"70.5637","longitude":"52.3158"},"timezone":{"offset":"+10:00","description":"Eastern Australia, Guam, Vladivostok"}},"email":"kubra.suleymanoglu@example.com","login":{"uuid":"8bcfde52-b68a-4fc0-9f78-49904789c098","username":"orangeelephant614","password":"joanne","salt":"yHO7Xav8","md5":"2f0ea74e164636c93d89e9e0b2cb8134","sha1":"49f363ccda58b60a3a5b4d8822867ca664552135","sha256":"3263a46f9ef6b6958b199a8246e96eb4941eddfb74ca5f85d1d7b8c6912502db"},"dob":{"date":"1976-12-30T07:37:42.220Z","age":45},"registered":{"date":"2002-07-10T01:19:55.536Z","age":19},"phone":"(456)-705-5655","cell":"(252)-731-6614","id":{"name":"","value":null},"picture":{"large":"https://randomuser.me/api/portraits/women/27.jpg","medium":"https://randomuser.me/api/portraits/med/women/27.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/women/27.jpg"},"nat":"TR"}],"info":{"seed":"9d2dc00ba0c17972","results":1,"page":1,"version":"1.3"}}"""
    payload_json = json.loads(payload)
    result = parse_result(payload_json)
    assert result["title"] == "Ms"
    assert result["firstname"] == "Kübra"
    assert result["street_address"] == "Mevlana Cd 8563"


def test_user():
    try:
        res = user()
    except Exception as ex:
        res = ex
    assert  type(res) in (str, werkzeug.exceptions.HTTPException, werkzeug.exceptions.ServiceUnavailable)

app.run(host='0.0.0.0', port=5000)