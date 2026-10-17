"""Export the Facebook & Instagram ads of a page (or a keyword) from the Meta Ad Library to CSV.

Usage: python example.py 15087023444 --country US --active
       python example.py "running shoes" --keyword --country US
"""
import argparse
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/meta-ad-library-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")

FIELDS = ["ad_archive_id", "page_name", "is_active", "start_date_iso", "end_date_iso", "publisher_platform",
          "display_format", "ad_text", "title", "cta_text", "link_url", "image_urls", "video_urls", "spend", "ad_library_url"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("target", help="page id, @username, facebook.com link, or a keyword with --keyword")
    p.add_argument("--keyword", action="store_true", help="search the target as a keyword across all advertisers")
    p.add_argument("--country", default="ALL", help="two-letter code or ALL")
    p.add_argument("--active", action="store_true", help="only ads running now")
    p.add_argument("--limit", type=int, default=200)
    a = p.parse_args()

    run_input = {"country": a.country, "activeStatus": "active" if a.active else "all", "maxAds": a.limit}
    run_input["keywords" if a.keyword else "pageIDs"] = [a.target]
    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input=run_input)

    safe = "".join(c if c.isalnum() else "_" for c in a.target)[:40]
    out = f"meta_ads_{safe}.csv"
    n = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for ad in client.dataset(run["defaultDatasetId"]).iterate_items():
            row = {k: (" | ".join(v) if isinstance(v, list) else v) for k, v in ad.items() if k in FIELDS}
            w.writerow(row)
            n += 1
    print(f"{n} ads -> {out}")


if __name__ == "__main__":
    main()
