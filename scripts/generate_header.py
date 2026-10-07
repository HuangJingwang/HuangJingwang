"""Generate the profile's Voice Agent masthead in both themes and sizes."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]

def render(dark=False, mobile=False):
    w, h = (480, 390) if mobile else (960, 330)
    ink, muted, accent, soft = ('#f0f6fc', '#919da8', '#68e0c2', '#193930') if dark else ('#172c33', '#60737a', '#087f72', '#d4eee7')
    name_size = 36 if mobile else 48
    voice_size = 54 if mobile else 76
    x = 22 if mobile else 24
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Sincerelyplz, exploring Voice Agents">',
             '<title>Sincerelyplz · Exploring Voice Agents</title>',
             '<style>.bar{animation:wave 2.8s ease-in-out infinite alternate}@keyframes wave{from{transform:scaleY(.35)}to{transform:scaleY(1)}}@media(prefers-reduced-motion:reduce){.bar{animation:none}}</style>',
             f'<g font-family="ui-monospace, SFMono-Regular, Consolas, monospace">',
             f'<circle cx="{x+5}" cy="23" r="4" fill="{accent}"/>',
             f'<text x="{x+19}" y="27" font-size="12" fill="{muted}" letter-spacing="2">PERSONAL LAB / NOW EXPLORING</text>',
             f'<text x="{x}" y="86" font-size="{name_size}" font-weight="700" fill="{ink}" letter-spacing="-2">Sincerelyplz</text>',
             f'<text x="{x-3}" y="{160 if mobile else 176}" font-size="{voice_size}" font-weight="700" fill="{accent}" letter-spacing="-3">Voice Agent<tspan font-size="{int(voice_size*.55)}">_</tspan></text>',
             f'<text x="{x}" y="{197 if mobile else 218}" font-size="{16 if mobile else 18}" fill="{ink}">Listen. Think. Speak.</text>']
    cx, cy = (240, 275) if mobile else (788, 160)
    count = 31 if mobile else 25
    spacing = 12 if mobile else 10
    for i in range(count):
        height = 12 + 100 * math.exp(-((i-(count-1)/2)/(count/3.1))**2) * (.48+.52*abs(math.sin(i*1.17)))
        bx = cx + (i-(count-1)/2)*spacing
        parts.append(f'<g transform="translate({bx:.1f} {cy})"><rect class="bar" x="-3" y="{-height/2:.1f}" width="6" height="{height:.1f}" rx="3" fill="{accent}" opacity="{.35+.65*(height/112):.2f}" style="animation-delay:-{i*.19:.2f}s"/></g>')
    by = 368 if mobile else 301
    parts += [f'<text x="{x}" y="{by}" font-size="{12 if mobile else 13}" letter-spacing="1" fill="{muted}">PIPECAT / REALTIME / MCP / RAG</text>', '</g></svg>']
    return '\n'.join(parts) + '\n'

if __name__ == '__main__':
    for dark in (False, True):
        for mobile in (False, True):
            name = 'voice-header' + ('-dark' if dark else '') + ('-mobile' if mobile else '') + '.svg'
            (ROOT / 'assets' / name).write_text(render(dark, mobile), encoding='utf-8')
