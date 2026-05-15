import unittest
from importlib.util import find_spec


@unittest.skipIf(find_spec("flask") is None, "flask is not installed")
class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from backend.app import app

        cls.app = app

    def setUp(self):
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def test_write_rejects_non_json(self):
        response = self.client.post("/write", data="not-json", content_type="text/plain")

        self.assertEqual(response.status_code, 400)
        self.assertIn("请求体必须是 JSON 对象", response.get_json()["error"])

    def test_write_rejects_missing_fields(self):
        response = self.client.post("/write", json={})

        self.assertEqual(response.status_code, 400)
        self.assertIn("缺少必要字段", response.get_json()["error"])

    def test_summary_rejects_missing_fields(self):
        response = self.client.post("/summary", json={})

        self.assertEqual(response.status_code, 400)
        self.assertIn("缺少必要字段", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
