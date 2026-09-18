"""Refresh public-only profile metrics. Python standard library, no dependencies."""
import json
import os
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER = 'HuangJingwang'

def get(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-readme'}
    if os.getenv('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com/' + path, headers=headers), timeout=30) as response:
        return json.load(response)

def render(user, repos):
    owned = [r for r in repos if not r['fork'] and not r.get('private')]
    languages = Counter(r['language'] for r in owned if r.get('language'))
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="285" viewBox="0 0 960 285">',
             '<rect width="960" height="285" rx="18" fill="#0c1020"/>',
             '<g font-family="monospace">']
    def text(x, y, s, size=14, color='#95a5c8'):
        parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}">{escape(str(s))}</text>')
    text(30, 34, 'PUBLIC SIGNAL / GITHUB API', 12, '#67e8f9')
    metrics = [(len(owned), 'ORIGINAL PUBLIC REPOS'), (sum(r['stargazers_count'] for r in owned), 'STARS / ORIGINAL REPOS'), (user['followers'], 'FOLLOWERS')]
    for i, (value, label) in enumerate(metrics):
        x = 30 + i * 312
        parts.append(f'<rect x="{x}" y="54" width="288" height="108" rx="12" fill="#151e33" stroke="#2c3554"/>')
        text(x+20, 108, value, 38, ['#67e8f9','#c4b5fd','#f0abfc'][i])
        text(x+20, 139, label, 11)
    text(30, 191, 'PRIMARY LANGUAGE / REPOSITORY COUNT (NOT CODE VOLUME)', 11)
    colors = ['#67e8f9','#a78bfa','#f0abfc','#fbbf24','#34d399','#60a5fa']
    total = sum(languages.values())
    x = 30
    for i, (lang, count) in enumerate(languages.most_common()):
        w = 900 * count / total
        parts.append(f'<rect x="{x:.2f}" y="204" width="{w:.2f}" height="9" fill="{colors[i%len(colors)]}"/>')
        x += w
    text(30, 238, '  /  '.join(f'{k}: {v}' for k,v in languages.most_common()), 12)
    text(30, 266, 'UPDATED ' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') + '  ·  PUBLIC DATA ONLY', 10, '#637493')
    parts.append('</g></svg>')
    (ROOT/'assets/signal.svg').write_text('\n'.join(parts), encoding='utf-8')

if __name__ == '__main__':
    repos = []
    page = 1
    while True:
        batch = get(f'users/{USER}/repos?per_page=100&page={page}&type=owner')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    render(get(f'users/{USER}'), repos)
