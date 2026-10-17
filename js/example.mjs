// Active Facebook & Instagram ads of a page from the Meta Ad Library.
// Usage: node example.mjs 15087023444   (page id, @username or facebook.com link)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const page = process.argv[2] ?? '15087023444';
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/meta-ad-library-scraper').call({
    pageIDs: [page],
    activeStatus: 'active',
    maxAds: 50,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const ad of items) {
    console.log(`${ad.display_format}  ${ad.publisher_platform.join(',')}  ${ad.start_date_iso?.slice(0, 10)}  ${ad.ad_text?.slice(0, 60) ?? ''}  ${ad.ad_library_url}`);
}
