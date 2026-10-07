"""Generate small transparent typing intros with a reduced-motion fallback."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
LINES = ['Exploring Voice Agents', 'Building with Pipecat & MCP', 'Code, experiment, write.']

def render(dark=False):
    color = '#f6bb84' if dark else '#a35429'
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="550" height="48" viewBox="0 0 550 48" role="img" aria-label="Exploring Voice Agents. Building with Pipecat and MCP. Code, experiment, write.">',
             '<title>Exploring Voice Agents</title>',
             '<style>.line{opacity:0;clip-path:inset(0 100% 0 0);animation:type 18s steps(28,end) infinite}@keyframes type{0%{opacity:1;clip-path:inset(0 100% 0 0)}18%,26%{opacity:1;clip-path:inset(0 0 0 0)}32%{opacity:1;clip-path:inset(0 100% 0 0)}33.3%{opacity:1}33.4%,100%{opacity:0}}@media(prefers-reduced-motion:reduce){.line{animation:none;display:none}.first{display:block;opacity:1;clip-path:none}}</style>']
    for i, line in enumerate(LINES):
        parts.append(f'<text class="line {"first" if i==0 else ""}" x="275" y="32" text-anchor="middle" fill="{color}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="23" style="animation-delay:{i*6}s">{escape(line)}</text>')
    return '\n'.join(parts + ['</svg>']) + '\n'

if __name__ == '__main__':
    for dark in (False, True):
        (ROOT / 'assets' / ('intro-dark.svg' if dark else 'intro.svg')).write_text(render(dark), encoding='utf-8')
