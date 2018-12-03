from scrapy.crawler import CrawlerProcess
from process import Hl7Spider
import vcr
import os
from unittest.mock import MagicMock

EXPECTED_JSON_PATH = os.path.join("tests", "data", "corrupted", "patient.json")
CURRENT_JSON_PATH = os.path.join("resources", "json",
                                 "Identification", "Individuals",
                                 "Patient.json")
CASSETTE_DIR = os.path.join(
    os.path.dirname(os.path.relpath(__file__)), "cassettes")
# if not os.path.exists(CASSETTE_DIR):
#     os.mkdir(CASSETTE_DIR)
spider_vcr = vcr.VCR(
    cassette_library_dir=CASSETTE_DIR,
    record_mode="once",
    match_on=['method', 'scheme', 'host', 'port', 'query'])


@spider_vcr.use_cassette
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


def mocked_json_dump(args):
    """Mocked function to to only write one JSON to disk"""
    import ipdb; ipdb.set_trace()
    if args[-1] == "Patient":
        return Hl7Spider().dump_json_to_file(args)
    else:
        return MagicMock()
