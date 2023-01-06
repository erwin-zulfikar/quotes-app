from flask import Flask, jsonify
from scraper import Crawler, url

app = Flask(__name__)


# route
@app.route("/")
def index():
    scrap = Crawler(url=url)
    data_dict: dict = {
        "message": scrap.crawling(),
    }
    return jsonify(data_dict)


if __name__ == '__main__':
    app.run(debug=True)
