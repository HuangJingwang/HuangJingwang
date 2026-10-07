"""Apple-inspired glass artwork for GitHub README's image-only styling surface.

These SVGs approximate frosted materials within each image; they do not implement
native Apple Liquid Glass or blur the surrounding GitHub page.
"""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
FONT = "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, 'PingFang SC', sans-serif"


def palette(dark):
    return dict(ink='#f5f7fa', muted='#a8b1bf', accent='#8ebcff', tint='#558dca', glass='#243143', edge='#ffffff', opacity='.65', edge_top='.42', edge_mid='.08', edge_bottom='.22') if dark else dict(ink='#1d1d1f', muted='#626873', accent='#0064ce', tint='#b0d5ff', glass='#ffffff', edge='#ffffff', opacity='.68', edge_top='.85', edge_mid='.14', edge_bottom='.38')


def foundation(w, h, p, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">',
            f'<title>{escape(title)}</title>',
            '<defs>',
            f'<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p["glass"]}" stop-opacity=".93"/><stop offset=".55" stop-color="{p["glass"]}" stop-opacity="{p["opacity"]}"/><stop offset="1" stop-color="{p["glass"]}" stop-opacity=".82"/></linearGradient>',
            f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p["edge"]}" stop-opacity="{p["edge_top"]}"/><stop offset=".48" stop-color="{p["edge"]}" stop-opacity="{p["edge_mid"]}"/><stop offset="1" stop-color="{p["edge"]}" stop-opacity="{p["edge_bottom"]}"/></linearGradient>',
            f'<radialGradient id="halo"><stop stop-color="{p["tint"]}" stop-opacity=".75"/><stop offset="1" stop-color="{p["tint"]}" stop-opacity="0"/></radialGradient>',
            '<filter id="shadow" x="-20%" y="-30%" width="140%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#142c50" flood-opacity=".12"/></filter>',
            '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>',
            '</defs>',
            '<style>.wave{animation:breathe 3.4s ease-in-out infinite alternate}@keyframes breathe{from{transform:scaleY(.5)}to{transform:scaleY(1)}}@media(prefers-reduced-motion:reduce){.wave{animation:none}}</style>',
            f'<g font-family="{FONT}">']


def text(parts, x, y, value, size, fill, weight=400, anchor='start', tracking=0):
    parts.append(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{tracking}">{escape(value)}</text>')


def panel(parts, x, y, w, h, r=28):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass)" stroke="url(#edge)" stroke-width="1.5" filter="url(#shadow)"/>')
    parts.append(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="{r-1}" fill="none" stroke="#ffffff" stroke-opacity=".08"/>')


def wave(parts, cx, cy, p, mobile=False):
    count, spacing = (23, 9) if mobile else (23, 8)
    for i in range(count):
        height = 12 + 66 * math.exp(-((i-11)/8)**2) * (.5+.5*abs(math.sin(i*1.17)))
        parts.append(f'<g transform="translate({cx+(i-11)*spacing} {cy})"><rect class="wave" x="-2.5" y="{-height/2:.1f}" width="5" height="{height:.1f}" rx="2.5" fill="{p["accent"]}" opacity="{.45+.5*height/78:.2f}" style="animation-delay:-{i*.15:.2f}s"/></g>')


def render(dark=False, mobile=False):
    w, h = (480, 436) if mobile else (960, 398)
    p = palette(dark)
    parts = foundation(w, h, p, 'Sincerelyplz · Voice Agent, RAG and developer tools')
    text(parts, w/2, 72, 'Sincerelyplz', 44 if mobile else 52, p['ink'], 600, 'middle', -1.8)
    text(parts, w/2, 108, 'Build something. Figure it out. Write it down.', 16 if mobile else 19, p['muted'], anchor='middle', tracking=-.2)
    y = 147
    # Blurred color is composed behind translucent panels, within the SVG itself.
    parts.append(f'<ellipse cx="{w*.67}" cy="{y+95}" rx="{w*.26}" ry="110" fill="url(#halo)" filter="url(#blur)"/>')
    parts.append(f'<ellipse cx="{w*.30}" cy="{y+116}" rx="{w*.22}" ry="85" fill="url(#halo)" opacity=".4"/>')
    panel(parts, 20, y, w-40, 258 if mobile else 209)
    tx = 44 if mobile else 56
    text(parts, tx, y+34, 'CURRENTLY EXPLORING', 11 if mobile else 12, p['muted'], 500, tracking=1.3)
    text(parts, tx, y+80, 'Voice Agent', 38 if mobile else 43, p['ink'], 600, tracking=-1.4)
    text(parts, tx, y+113, 'Pipecat · Realtime audio · MCP', 16 if mobile else 19, p['muted'])
    if mobile:
        wave(parts, 240, y+183, p, True)
        text(parts, 240, y+235, 'Listen. Think. Speak.', 14, p['muted'], anchor='middle')
    else:
        text(parts, tx, y+160, '研究实时语音交互，也记录实践里的问题。', 18, p['muted'])
        panel(parts, 630, y+28, 265, 151, 24)
        wave(parts, 762, y+91, p)
        text(parts, 762, y+132, 'Listen. Think. Speak.', 14, p['muted'], anchor='middle')
    parts.append('</g></svg>')
    return '\n'.join(parts) + '\n'


CARDS = [
    ('rag', 'RAG Knowledge Lab', '把检索过程摊开来看。', '原文、Chunk、向量检索与知识图谱。', 'Knowledge & retrieval', '01'),
    ('mcp', 'ChatBot MCP', '给聊天机器人接上工具。', '通过 MCP 连接外部服务与 API。', 'Agents & tools', '02'),
    ('crew', 'Change Crew', '折腾编码 Agent 的协作。', '面向 Codex 的多智能体交付工作流。', 'Developer workflow', '03'),
]


def render_card(card, dark=False, mobile=False):
    slug, name, description, detail, label, number = card
    w, h = (480, 180) if mobile else (960, 174)
    p = palette(dark)
    parts = foundation(w, h, p, name + ' · ' + description)
    parts.append(f'<ellipse cx="{w*.84}" cy="84" rx="{w*.25}" ry="90" fill="url(#halo)" opacity=".6" filter="url(#blur)"/>')
    panel(parts, 16, 12, w-32, h-33, 24)
    x = 36 if mobile else 48
    text(parts, x, 43, label, 11 if mobile else 13, p['muted'], 500)
    text(parts, x, 81, name, 26 if mobile else 31, p['ink'], 600, tracking=-.7)
    text(parts, x, 112, description, 17 if mobile else 20, p['muted'])
    if mobile:
        text(parts, x, 136, detail, 14, p['muted'])
    else:
        text(parts, w-60, 105, number, 45, p['accent'], 300, 'end', -2)
        text(parts, x+320, 112, detail, 18, p['muted'])
    parts.append('</g></svg>')
    return '\n'.join(parts) + '\n'


if __name__ == '__main__':
    for dark in (False, True):
        for mobile in (False, True):
            suffix = ('-dark' if dark else '') + ('-mobile' if mobile else '') + '.svg'
            (ROOT / 'assets' / ('voice-header' + suffix)).write_text(render(dark, mobile), encoding='utf-8')
            for card in CARDS:
                (ROOT / 'assets' / ('project-' + card[0] + suffix)).write_text(render_card(card, dark, mobile), encoding='utf-8')
