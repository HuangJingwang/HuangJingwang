"""Refresh the three latest posts from the owner's public RSS feed."""
import re
import xml.etree.ElementTree as ET
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit, quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- BLOG-POST-LIST:START -->'
END = '<!-- BLOG-POST-LIST:END -->'

def latest_posts(feed):
    posts = []
    for item in ET.fromstring(feed).findall('./channel/item'):
        title = item.findtext('title', '').strip()
        link = item.findtext('link', '').strip()
        if not title or urlsplit(link).scheme not in ('http', 'https'):
            continue
        date = parsedate_to_datetime(item.findtext('pubDate', ''))
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        posts.append((title, link, date))
    if not posts:
        raise ValueError('No valid posts; preserving the existing README')
    return sorted(posts, key=lambda post: post[2], reverse=True)[:3]

def update_readme(readme, posts):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError('Expected exactly one pair of blog markers')
    lines = []
    for title, link, _ in posts:
        label = re.sub(r'([\\`*_{}\[\]<>])', r'\\\1', ' '.join(title.split()))
        lines.append(f'- [{label}]({quote(link, safe=":/?=&%#-._~")})')
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return before + START + '\n' + '\n'.join(lines) + '\n' + END + after

if __name__ == '__main__':
    with urlopen(Request('https://www.asterh.me/rss.xml', headers={'User-Agent': 'aster-profile-readme'}), timeout=30) as response:
        posts = latest_posts(response.read())
    path = ROOT / 'README.md'
    path.write_text(update_readme(path.read_text(encoding='utf-8'), posts), encoding='utf-8')
