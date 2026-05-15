import importlib
import os
import unittest


class ConfigTestCase(unittest.TestCase):
    def test_csv_env_filters_empty_values(self):
        os.environ["GPT_AVAILABLE_MODELS"] = "gpt-4o, ,gpt-4o-mini,"

        import config

        config = importlib.reload(config)

        self.assertEqual(config.API_SETTINGS["gpt"]["available_models"], ["gpt-4o", "gpt-4o-mini"])


if __name__ == "__main__":
    unittest.main()
