#!/usr/bin/env python3
"""Publish scheduled blog posts whose date has arrived.

Run from the repo root (the directory containing blog/ and sitemap.xml).
For every post in scheduled/manifest.json whose publish date is today or
earlier (America/Los_Angeles) and whose folder still sits in scheduled/posts/:

  1. move scheduled/posts/<slug>/  ->  blog/<slug>/
  2. insert its card at the top of blog/index.html
  3. add its URL to sitemap.xml
  4. mark it published in the manifest

Then regenerate feed.xml from all published posts.

The script is idempotent: a post already moved is skipped, a card or sitemap
entry that already exists is not duplicated. Safe to run manually or from CI.
"""
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(REPO, "scheduled", "manifest.json")
BLOG_INDEX = os.path.join(REPO, "blog", "index.html")
SITEMAP = os.path.join(REPO, "sitemap.xml")
FEED = os.path.join(REPO, "feed.xml")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def pacific_today():
    """Date in America/Los_Angeles without external tz data.

    DST rule (2007+): begins second Sunday in March, ends first Sunday in
    November, both at 2:00 AM local. Good through any year this blog runs.
    """
    utc = datetime.now(timezone.utc)

    def nth_sunday(year, month, n):
        d = datetime(year, month, 1, tzinfo=timezone.utc)
        first_sunday = 1 + (6 - d.weekday()) % 7
        return datetime(year, month, first_sunday + 7 * (n - 1), 10, 0,
                        tzinfo=timezone.utc)  # 2 AM PST = 10:00 UTC

    start = nth_sunday(utc.year, 3, 2)
    end = nth_sunday(utc.year, 11, 1)
    offset = -7 if start <= utc < end else -8
    return (utc + timedelta(hours=offset)).date()


def card_html(post):
    y, m, d = (int(x) for x in post["date"].split("-"))
    date_short = f"{m}/{d}/{str(y)[2:]}"
    slug, title = post["slug"], post["title"]
    return f"""        <article class="blog-item">
          <a href="{slug}/"><img src="../assets/images/{post['image']}" alt="{title}" width="1600" height="900" loading="lazy" decoding="async"></a>
          <div class="blog-meta">{post['category']} &middot; Oscar J Mayorga &middot; {date_short}</div>
          <h2><a href="{slug}/">{title}</a></h2>
          <p>{post['excerpt']}</p>
          <a class="read-more" href="{slug}/">Read More</a>
        </article>
"""


def insert_card(post):
    html = open(BLOG_INDEX, encoding="utf-8").read()
    if f'href="{post["slug"]}/"' in html:
        return False
    marker = '<div class="blog-list">'
    if marker not in html:
        raise SystemExit(f"ERROR: could not find {marker!r} in blog/index.html")
    html = html.replace(marker, marker + "\n" + card_html(post).rstrip(), 1)
    open(BLOG_INDEX, "w", encoding="utf-8").write(html)
    return True


def insert_sitemap(post, site):
    xml = open(SITEMAP, encoding="utf-8").read()
    loc = f"{site}/blog/{post['slug']}"
    if f"<loc>{loc}</loc>" in xml:
        return False
    entry = f"  <url><loc>{loc}</loc></url>\n"
    lines = xml.splitlines(keepends=True)
    last_blog = max(i for i, ln in enumerate(lines)
                    if "/blog" in ln and "<loc>" in ln)
    lines.insert(last_blog + 1, entry)
    open(SITEMAP, "w", encoding="utf-8").write("".join(lines))
    return True


def rfc822(date_iso):
    y, m, d = (int(x) for x in date_iso.split("-"))
    dt = datetime(y, m, d, 15, 0, tzinfo=timezone.utc)  # 8 AM Pacific in summer
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def write_feed(manifest):
    site = manifest["site"]
    published = sorted((p for p in manifest["posts"] if p.get("published")),
                       key=lambda p: p["date"], reverse=True)
    items = []
    for p in published:
        url = f"{site}/blog/{p['slug']}"
        items.append(f"""    <item>
      <title>{esc(p['title'])}</title>
      <link>{url}</link>
      <guid>{url}</guid>
      <pubDate>{rfc822(p['date'])}</pubDate>
      <description>{esc(p['excerpt'])}</description>
    </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Sensemaking Lab Blog</title>
    <link>{site}/blog/</link>
    <atom:link href="{site}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Insights on program evaluation, data consulting, and Critical Analytics for education, healthcare, and nonprofit organizations.</description>
    <language>en-us</language>
{chr(10).join(items)}
  </channel>
</rss>
"""
    open(FEED, "w", encoding="utf-8").write(feed)


def main():
    if not os.path.exists(MANIFEST):
        raise SystemExit("ERROR: scheduled/manifest.json not found. Run from the repo root.")
    for req in (BLOG_INDEX, SITEMAP):
        if not os.path.exists(req):
            raise SystemExit(f"ERROR: {os.path.relpath(req, REPO)} not found. "
                             "Is the repo root the site root?")

    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    site = manifest["site"]
    today = pacific_today()
    changed = False

    for post in sorted(manifest["posts"], key=lambda p: p["date"]):
        due = datetime.strptime(post["date"], "%Y-%m-%d").date() <= today
        src = os.path.join(REPO, "scheduled", "posts", post["slug"])
        dst = os.path.join(REPO, "blog", post["slug"])

        if post.get("published") and not os.path.isdir(src):
            continue
        if not due:
            print(f"not due yet: {post['slug']} ({post['date']})")
            continue

        if os.path.isdir(src):
            if os.path.isdir(dst):
                shutil.rmtree(src)  # already live; drop the staged copy
            else:
                shutil.move(src, dst)
                print(f"published page: blog/{post['slug']}/")
        elif not os.path.isdir(dst):
            print(f"WARNING: {post['slug']} is due but has no staged folder and "
                  "is not live; skipping")
            continue

        if insert_card(post):
            print(f"added card to blog index: {post['slug']}")
        if insert_sitemap(post, site):
            print(f"added to sitemap: {post['slug']}")
        post["published"] = True
        changed = True

    if changed or not os.path.exists(FEED):
        write_feed(manifest)
        json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), indent=2)
        print("feed.xml and manifest updated")
    else:
        print("nothing to publish")


if __name__ == "__main__":
    sys.exit(main())
