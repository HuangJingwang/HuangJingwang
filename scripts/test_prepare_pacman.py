import unittest
import xml.etree.ElementTree as ET
from prepare_pacman import still_graph

class StillGraphTests(unittest.TestCase):
    def test_removes_svg_animation_and_preserves_cells(self):
        svg = '<svg xmlns="http://www.w3.org/2000/svg"><rect fill="green"><animate attributeName="fill" values="green;white" /></rect><g><animateTransform attributeName="transform" /><circle r="4" /></g></svg>'
        root = ET.fromstring(still_graph(svg))
        tags = [node.tag.rsplit('}', 1)[-1] for node in root.iter()]
        self.assertEqual(tags, ['svg', 'rect', 'g', 'circle'])
        self.assertEqual(root[0].get('fill'), 'green')

if __name__ == '__main__':
    unittest.main()
