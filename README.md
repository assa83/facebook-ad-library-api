# Facebook Ad Library API – working example (Python, JS, n8n)

Export the Facebook & Instagram ads of any page, or of any keyword, from the public **Meta Ad Library** to CSV or JSON: ad copy, headline, CTA, landing page, image and video URLs, start/end dates, platforms, page info, and spend/reach for political ads.

Powered by the [meta-ad-library-scraper](https://apify.com/lagenuina_agency/meta-ad-library-scraper) actor on Apify. No Facebook login, no cookies, no Meta developer app or identity verification.

## Example output (real result, shortened)

```json
{
  "ad_archive_id": "1632663538563793",
  "ad_library_url": "https://www.facebook.com/ads/library/?id=1632663538563793",
  "page_id": "15087023444",
  "page_name": "Nike",
  "is_active": true,
  "start_date_iso": "2026-08-31T07:00:00.000Z",
  "publisher_platform": ["FACEBOOK", "INSTAGRAM", "AUDIENCE_NETWORK"],
  "display_format": "IMAGE",
  "ad_text": "Bring sports more fully into your day with the Nike App.",
  "title": "Nike Zenvy Women's Dri-FIT Tank Top",
  "cta_text": "Install now",
  "link_url": "http://play.google.com/store/apps/details?id=com.nike.omega",
  "image_urls": ["https://scontent.xx.fbcdn.net/v/t39.35426-6/788880667_..._n.jpg"],
  "video_urls": [],
  "page_like_count": 39501406
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py 15087023444 --active            # a page (id, @username or facebook.com link)
python python/example.py "running shoes" --keyword --country US
```

JavaScript: `cd js && npm install && node example.mjs 15087023444`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/meta-ad-library-scraper").call(run_input={
    "pageIDs": ["15087023444"],
    "country": "US",
    "activeStatus": "active",
    "maxAds": 100,
})
for ad in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(ad["page_name"], ad["ad_text"], ad["image_urls"], ad["video_urls"])
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/meta-ad-library-scraper').call({ keywords: ['running shoes'], country: 'US', activeStatus: 'active', maxAds: 100 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~meta-ad-library-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"adLibraryUrls": ["https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&search_type=page&view_all_page_id=15087023444"], "maxAds": 100}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/meta-ad-library-scraper) (Input tab).

## Use case: export a competitor's Facebook & Instagram ads to CSV

`python/example.py` scrapes the Meta Ad Library for one page or keyword and writes `meta_ads_<target>.csv` with ad ID, page, status, dates, platforms, format, copy, headline, CTA, landing page, image and video URLs, spend and Ad Library link – ready for Excel or Google Sheets.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every Monday 08:00 → run the actor on a competitor's page (active ads) → flatten the fields with a Set node → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your page ids or keywords), set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```json
{
  "mcpServers": {
    "meta-ad-library-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/meta-ad-library-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

$0.20 per 1,000 ads on every Apify plan (Free, Bronze, Silver, Gold and above), with Apify platform usage and residential proxy included, no start fee, pay only for results – see [lagenuina_agency/meta-ad-library-scraper](https://apify.com/lagenuina_agency/meta-ad-library-scraper).

## More tools from Quelli di Carne Genuina

- **Ad intelligence:** [Google Ads Transparency](https://github.com/assa83/google-ads-transparency-api) · [TikTok Top Ads](https://github.com/assa83/tiktok-top-ads-api) · [LinkedIn Ad Library](https://github.com/assa83/linkedin-ad-library-api)
- **Competitor & SEO research:** [Similarweb traffic](https://github.com/assa83/similarweb-traffic-api) · [Google Trends](https://github.com/assa83/google-trends-api-python) · [Google Play](https://github.com/assa83/google-play-scraper-api)
- **Travel prices:** [Google Hotels](https://github.com/assa83/google-hotels-prices-api) · [Google Flights](https://github.com/assa83/google-flights-api)
- **Retail prices:** [Woolworths & Coles](https://github.com/assa83/australian-supermarket-prices-api)
- **Content & social data:** [YouTube Transcript](https://github.com/assa83/youtube-transcript-scraper-api) · [Medium](https://github.com/assa83/medium-scraper-api) · [Likee](https://github.com/assa83/likee-scraper-api)

All actors: [apify.com/lagenuina_agency](https://apify.com/lagenuina_agency) · Tutorials: [assa83.github.io](https://assa83.github.io)

## Disclaimer

Independent, not affiliated with Meta (not endorsed by Meta Platforms, Inc.). It reads only publicly available data from the Meta Ad Library. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
