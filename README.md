# Sensemaking Lab website

Static rebuild of [www.sensemakinglab.io](https://www.sensemakinglab.io), migrated from Squarespace. Plain HTML/CSS/JS, no build step, ready for GitHub Pages behind Cloudflare.

## Structure

Each page lives in its own folder so URLs match the original site (`/about`, `/services`, `/blog/...`, etc.). Shared styles are in `assets/css/main.css`; `assets/js/main.js` only handles the mobile menu. Blog posts are plain HTML in `blog/<slug>/index.html`; to add a post, copy an existing post folder, edit the content, and add a card to `blog/index.html`.

## One-time setup

1. **Fetch images.** Go to Actions, run "Fetch site assets". This downloads all images from the Squarespace CDN into `assets/images/` and commits them. Do this before cancelling Squarespace.
2. **Enable GitHub Pages.** Settings, Pages, deploy from branch `main`, root folder. Note: publishing Pages from a private repo requires a paid GitHub plan; on the free plan the repo must be public to use Pages.
3. **Point the domain.** In Cloudflare DNS, create a CNAME for `www` to `<username>.github.io`, and either an A record set for the apex (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153) or a redirect from apex to `www`. Then add `www.sensemakinglab.io` as the custom domain in the Pages settings and enable "Enforce HTTPS".
4. **Keep email working.** Before moving DNS to Cloudflare, copy the existing MX and TXT (SPF/DKIM) records for hello@sensemakinglab.io into Cloudflare, or mail will break.

## Notes

- The original site used Adobe Fonts (bc-novatica-cyr, omnes-pro) licensed through Squarespace. This rebuild substitutes the closest free Google Fonts: Poppins for headings and Quicksand for body text.
- The Squarespace cart and account pages were intentionally not migrated.
- The contact page, like the original, lists the email address; there is no form backend.

## Search, listings, and email status

Update this section whenever search, listing, or email settings change.

**2026-10-22 to 2026-10-24**

- Internal files (`README.md`, `README_BLOG_AUTOMATION.md`, `asset-manifest.txt`, `scripts/`, `scheduled/`, `docs/`) are redirected to the home page in `_redirects` so they are not served publicly. Add any new internal file or folder there.
- Page titles are 60 characters or fewer and end in ` | Sensemaking Lab`. Meta descriptions are 155 characters or fewer, and `og:description`, `twitter:description`, and the JSON-LD description carry the same text. New blog posts follow the same limits.
- Photos were converted to resized JPEGs (1920 px wide at most); site images fell from about 18 MB to 5.4 MB. Save new photos as JPEG, not PNG, and resize before committing.
- The sitemap is in Google Search Console and Bing Webmaster Tools. Bing's copy was resubmitted on 2026-10-22, when it held 20 URLs.
- Google Business Profile created on 2026-10-22 under oscar@sensemakinglab.io: category Consultant, service area Los Angeles County, website only (no public phone), address hidden. Waiting on Oscar to verify it.
- DMARC is at quarantine, with reports going to Oscar's personal Gmail. Reports from Google and Microsoft through 2026-10-22 show every message passing.

**Open items**

- Verify the Google Business Profile, then add categories (Educational consultant, Market researcher), a description, and a logo.
- Once the Business Profile and a LinkedIn company page are live, add their URLs to the organization JSON-LD as `sameAs`.