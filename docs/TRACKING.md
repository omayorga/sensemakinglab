# Sensemaking Lab: Blog Tracking Playbook

How new blog posts get measured, what happens automatically, and the one manual step you own.

Measurement ID: **G-ECJDV02GDB** (Google Analytics 4)
Site: https://www.sensemakinglab.io

---

## What happens automatically (no action needed)

Every new blog post is tracked end to end without any per-post setup:

1. **Page views and engagement.** Google Analytics is injected on every page by Cloudflare, so a new post is tracked the moment it goes live. Enhanced measurement also records scrolls, outbound clicks, file downloads, and video.
2. **Discovery by Google.** The Tuesday publishing job adds each new post's URL to `sitemap.xml` and regenerates the RSS feed. Google re-reads the submitted sitemap and indexes new posts on its own.
3. **Search and AI readiness.** The post template already includes a canonical tag, Open Graph and Twitter cards, and structured data for Article, FAQ, and Organization.
4. **Conversions.** Every post links to the Contact page, and a Contact visit now fires the `generate_lead` key event. This lets you trace blog traffic through to an inquiry.

You do not need to touch Analytics, the sitemap, or the tag for a new post to be tracked.

---

## The one manual step: tag your promotion links

When you share or advertise a post on LinkedIn, email, or anywhere else, add UTM tags to the link. Without them, the traffic is lumped into generic "referral" and you cannot tell paid from organic, or one campaign from another.

### The convention

Keep these values consistent every time:

| Parameter | What to put | Examples |
|-----------|-------------|----------|
| `utm_source` | the platform | `linkedin`, `email`, `x`, `facebook` |
| `utm_medium` | the type of traffic | `paid_social` for ads, `social` for organic posts, `email` for newsletters |
| `utm_campaign` | the initiative | `blog_promo_2026` |
| `utm_content` | which post or creative | the post slug, e.g. `program_evaluator` |

Rules: all lowercase, words joined with underscores, no spaces. Use `paid_social` only for paid ads so Analytics files them under the Paid Social channel.

### Template

Copy this and replace the bracketed parts:

```
https://www.sensemakinglab.io/blog/[POST-SLUG]/?utm_source=[PLATFORM]&utm_medium=[social OR paid_social]&utm_campaign=[CAMPAIGN]&utm_content=[POST-SLUG]
```

### Ready examples for current posts

LinkedIn paid ad to the evaluator post:
```
https://www.sensemakinglab.io/blog/how-to-choose-a-program-evaluator/?utm_source=linkedin&utm_medium=paid_social&utm_campaign=blog_promo_2026&utm_content=program_evaluator
```

LinkedIn organic post to the retention post:
```
https://www.sensemakinglab.io/blog/student-retention-strategies-that-work/?utm_source=linkedin&utm_medium=social&utm_campaign=blog_promo_2026&utm_content=student_retention
```

Email newsletter to the critical analytics post:
```
https://www.sensemakinglab.io/blog/what-is-critical-analytics/?utm_source=email&utm_medium=email&utm_campaign=newsletter_2026&utm_content=critical_analytics
```

For a LinkedIn ad, paste the tagged link as the destination URL in LinkedIn Campaign Manager.

---

## Where to see the results in GA4

- **Traffic by channel and source:** Reports, then Traffic acquisition. Switch the dimension to Session source / medium to see `linkedin / paid_social`, `linkedin / social`, and so on.
- **Which post a source landed on:** in that same report, add Landing page as a secondary dimension.
- **Conversions:** the `generate_lead` key event appears in the Key events report and can be added as a column anywhere.
- **Search terms:** Reports, then Search Console, then Google organic search traffic.

---

## Optional enhancements (nice to have, not required)

- **Faster indexing of a new post.** In Google Search Console, use URL Inspection on the new post URL and click Request Indexing. Google will find it via the sitemap regardless, this just speeds it up.
- **Track the email click as a conversion.** The current `generate_lead` event counts Contact page visits, which is a strong proxy. Tracking the actual `mailto:` click would be more precise but requires a small code addition and depends on how the tag is loaded. Worth doing later if inquiry volume grows.
- **Compare like windows.** When judging a campaign, compare the same date range in LinkedIn and GA4. LinkedIn Campaign Manager is the source of truth for ad cost, clicks, and cost per result.

---

## Quick launch checklist for each new post

1. Write the post and stage it (folder in `scheduled/posts/` and an entry in `scheduled/manifest.json`). The Tuesday job publishes it.
2. Confirm it is live and looks right.
3. Build the UTM link with the template above.
4. Promote using the tagged link.
5. Optional: request indexing in Search Console.
6. Check Traffic acquisition and `generate_lead` in GA4 after a few days.
