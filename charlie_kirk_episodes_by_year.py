#!/usr/bin/env python3
"""
Pulls the full episode list for *The Charlie Kirk Show* from its official RSS feed
and prints titles grouped by year. Optionally export to CSV or Markdown.
Now also includes a link to the episode (prefers audio enclosure URL; falls back to item link).

Usage examples:
  python3 charlie_kirk_episodes_by_year.py
  python3 charlie_kirk_episodes_by_year.py --format csv --output charlie_kirk_episodes.csv
  python3 charlie_kirk_episodes_by_year.py --format markdown > episodes.md
"""
import sys
import argparse
import csv
import itertools
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://www.omnycontent.com/d/playlist/5e27a451-e6e6-4c51-aa03-a7370003783c/c865b590-c84f-4f7e-a43e-ac64014b61d9/8978e846-cacd-4d65-b085-ac64014cd49f/podcast.rss"

def fetch_feed(url: str) -> bytes:
    with urllib.request.urlopen(url) as r:
        return r.read()

def get_text(elem, tag, default=""):
    child = elem.find(tag)
    return child.text.strip() if (child is not None and child.text) else default

def get_link(item):
    enclosure = item.find('enclosure')
    if enclosure is not None and enclosure.get('url'):
        return enclosure.get('url')
    return get_text(item, 'link', '')

def parse_items(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    items = root.findall('.//item')
    def when(i):
        return parsedate_to_datetime(get_text(i, 'pubDate')).date()
    rows = []
    for i in items:
        ymd = when(i)
        title = get_text(i, 'title')
        link = get_link(i)
        rows.append((ymd.year, ymd.isoformat(), title, link))
    rows.sort(key=lambda x: (-x[0], x[1]))
    return rows

def emit_text(rows, out):
    for year, group in itertools.groupby(rows, key=lambda r: r[0]):
        print(f"===== {year} =====", file=out)
        for _, d, t, link in group:
            line = f"{d} — {t}"
            if link:
                line += f"\n    {link}"
            print(line, file=out)
        print("", file=out)

def emit_csv(rows, out_file):
    with (open(out_file, "w", newline="", encoding="utf-8") if out_file else sys.stdout) as f:
        w = csv.writer(f)
        w.writerow(["Year", "Date", "Title", "Link"])
        for y, d, t, link in rows:
            w.writerow([y, d, t, link])

def emit_markdown(rows, out):
    current_year = None
    for y, d, t, link in rows:
        if y != current_year:
            if current_year is not None:
                print("", file=out)
            print(f"## {y}", file=out)
            print("", file=out)
            current_year = y
        if link:
            print(f"- **{d}** — [{t}]({link})", file=out)
        else:
            print(f"- **{d}** — {t}", file=out)

def main():
    ap = argparse.ArgumentParser(
        description="List all episodes of The Charlie Kirk Show grouped by year, including links."
    )
    ap.add_argument("--format", choices=["text", "csv", "markdown"], default="text",
                    help="Output format (default: text).")
    ap.add_argument("--output", "-o", default=None,
                    help="Optional path to write output file (CSV only; text/markdown go to stdout).")
    ap.add_argument("--feed-url", default=FEED_URL,
                    help="Override the default RSS feed URL if needed.")
    args = ap.parse_args()

    try:
        xml = fetch_feed(args.feed_url)
    except Exception as e:
        print(f"Error fetching RSS feed: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        rows = parse_items(xml)
    except Exception as e:
        print(f"Error parsing RSS feed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "csv":
        emit_csv(rows, args.output)
    elif args.format == "markdown":
        emit_markdown(rows, sys.stdout)
    else:
        emit_text(rows, sys.stdout)

if __name__ == "__main__":
    main()
