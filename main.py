from bs4 import BeautifulSoup
from flask import Flask, current_app, jsonify
from flask_cors import CORS
import json
import requests
import re

app = Flask(__name__)
CORS(app)


def featured():
  URL = 'https://www.vlr.gg'
  html = requests.get(URL).text
  soup = BeautifulSoup(html, "html.parser")
  news_feature_element = soup.find(
      'div', class_="col mod-2").parent.find_all('a', class_="wf-card news-feature")
  news_feature = []
  for video in news_feature_element:
    #   # if video.find('p', class_="title").text.strip() != "Today's selection":
    #     # title = video.find('p', class_="title").text.strip()
      title = video.find('div', class_="wf-spoiler-visible").text.strip()
      url = video['href']
      thumbnail = video.find('img').attrs['src']
      thumbnail = f"https:{thumbnail}"
      url = f"https://vlr.gg{url}"

      news_feature.append({
          "title": title,
          "url": url,
          "thumbnail": thumbnail
      })
  return news_feature


def rankings():
  URL = 'https://www.vlr.gg/rankings/north-america'
  html = requests.get(URL).text
  soup = BeautifulSoup(html, "html.parser")

  s = soup.find("table", class_=re.compile("^wf-faux-table mod-teams"))

  h, [_, *d] = [i.text for i in s.tr.find_all('th')], [[i.text.replace("\t","").replace("\n","").replace("\u2013","-").replace('\u22c5',"") for i in b.find_all('td')] for b in s.find_all('tr')]
  result = [dict(zip(h, i)) for i in d]
  return result


def vlr_recent():
  headers = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '3600',
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
  }
  URL = 'https://www.vlr.gg'
  html = requests.get(URL, headers=headers).text
  soup = BeautifulSoup(html, "html.parser")
  if soup.find(class_="col mod-2") == None:
    return None
  else:
    results = soup.find(class_="col-container")
    news_feature_element = soup.find(class_="js-home-news").find_all(class_="wf-card")
    vlr = []
    for vlrs in news_feature_element:
        title = vlrs.find('div', class_=re.compile('news-item-title'))
        # within news-item-title, grab the text
        title = title.text.replace("\t", "").replace("\n", "").replace("\"", "")
        url = vlrs.find('a', class_=re.compile('wf-module-item news-item '))
        #within new-item, grab url from href
        url = url['href']
        url = f"https://vlr.gg{url}"

        vlr.append({
            "title": title,
            "url": url,
        })
    return vlr

@app.route("/")
def home():
  return jsonify({
      "hello": "world"
  })


@app.route("/featured")
def featured_news():
  return current_app.response_class(json.dumps(featured(), indent=4), mimetype="application/json")


@app.route("/news")
def vlr_news():
  return current_app.response_class(json.dumps(vlr_recent(), indent=4), mimetype="application/json")

@app.route("/rankings")
def vlrR():
  return current_app.response_class(json.dumps(rankings(), indent=4), mimetype="application/json")



if __name__ == "__main__":
  app.run(
      host="0.0.0.0",
      port=9271
  )
