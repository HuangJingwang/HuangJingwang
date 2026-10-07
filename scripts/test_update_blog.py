import unittest
from update_blog import latest_posts, update_readme

class BlogTests(unittest.TestCase):
    def test_latest_by_date_not_feed_order(self):
        feed = '<rss><channel>' + ''.join(f'<item><title>{title}</title><link>https://www.asterh.me/posts/{day}</link><pubDate>{day:02d} Sep 2026 00:00:00 GMT</pubDate></item>' for day, title in [(1, 'Old'), (20, '[Newest]'), (10, 'Middle'), (15, 'Third')]) + '</channel></rss>'
        posts = latest_posts(feed)
        self.assertEqual([p[0] for p in posts], ['[Newest]', 'Third', 'Middle'])
        result = update_readme('before\n<!-- BLOG-POST-LIST:START -->\nstale\n<!-- BLOG-POST-LIST:END -->\nafter', posts)
        self.assertIn(r'\[Newest\]', result)
        self.assertTrue(result.endswith('after'))
        self.assertNotIn('stale', result)

    def test_empty_feed_keeps_previous_content(self):
        with self.assertRaises(ValueError):
            latest_posts('<rss><channel /></rss>')

    def test_rejects_non_web_links(self):
        feed = '<rss><channel><item><title>Bad</title><link>javascript:alert(1)</link><pubDate>01 Sep 2026 00:00:00 GMT</pubDate></item></channel></rss>'
        with self.assertRaises(ValueError):
            latest_posts(feed)

if __name__ == '__main__':
    unittest.main()
