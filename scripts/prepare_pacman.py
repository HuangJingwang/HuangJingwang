"""Create still contribution graphs for visitors who request reduced motion."""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ET.register_namespace('', 'http://www.w3.org/2000/svg')

def still_graph(svg):
    root = ET.fromstring(svg)
    for parent in root.iter():
        for child in list(parent):
            if child.tag.rsplit('}', 1)[-1] in ('animate', 'animateTransform', 'animateMotion', 'set'):
                parent.remove(child)
    return ET.tostring(root, encoding='unicode')

if __name__ == '__main__':
    for theme in ('', '-dark'):
        source = ROOT / 'assets' / f'pacman-contribution-graph{theme}.svg'
        target = ROOT / 'assets' / f'pacman-contribution-graph{theme}-still.svg'
        target.write_text(still_graph(source.read_text(encoding='utf-8')), encoding='utf-8')
