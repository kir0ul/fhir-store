from scrapy.crawler import CrawlerProcess
from process import Hl7Spider
import os
from unittest.mock import MagicMock
from bs4 import BeautifulSoup

EXPECTED_JSON_PATH = os.path.join("tests", "data", "scraping",
                                  "Patient_ref.json")
CURRENT_JSON_PATH = os.path.join("tests", "data", "scraping",
                                 "Patient_test.json")


def test_spider(monkeypatch):
    monkeypatch.setattr("process.Hl7Spider.dump_json_to_file",
                        mocked_json_dump)

    # Run the spider
    process = CrawlerProcess({
        "USER_AGENT":
        "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    })
    process.crawl(Hl7Spider)
    process.start()

    # Compare the produced JSON with the expected one
    with open(EXPECTED_JSON_PATH, "r") as expected_json_handle:
        expected_json_txt = expected_json_handle.read()
    with open(CURRENT_JSON_PATH, "r") as current_json_handle:
        current_json_txt = current_json_handle.read()
    assert expected_json_txt == current_json_txt
    os.remove(CURRENT_JSON_PATH)


def mocked_json_dump(*args):
    """Mocked function to to only write one JSON to disk"""
    if args[-1] == "Patient":
        # Remove the `self` argument
        return write_json_file(*args[1:])
    else:
        return MagicMock()


def write_json_file(response, json_html, parent_category, category, title):
    """Rewritten funtion since the original one has been mocked"""
    json_html = json_html.strip()
    json_text = BeautifulSoup(json_html, 'lxml').text
    if not os.path.exists(os.path.dirname(CURRENT_JSON_PATH)):
        os.makedirs(os.path.dirname(CURRENT_JSON_PATH))
    with open(CURRENT_JSON_PATH, 'w') as f:
        f.write(json_text)
