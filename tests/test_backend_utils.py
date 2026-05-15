import unittest
from unittest.mock import patch

from backend.backend_utils import get_model_config_from_provider_model


class BackendUtilsTestCase(unittest.TestCase):
    def test_get_model_config_rejects_bad_format(self):
        with self.assertRaisesRegex(ValueError, "provider/model"):
            get_model_config_from_provider_model("gpt-4o-mini")

    def test_get_model_config_rejects_unknown_provider(self):
        with self.assertRaisesRegex(ValueError, "未知模型供应商"):
            get_model_config_from_provider_model("unknown/model")

    def test_get_model_config_rejects_unconfigured_model(self):
        import config

        settings = {
            **config.API_SETTINGS,
            "gpt": {
                **config.API_SETTINGS["gpt"],
                "available_models": ["gpt-4o-mini"],
            },
        }
        with patch.object(config, "API_SETTINGS", settings):
            with self.assertRaisesRegex(ValueError, "未配置可用模型"):
                get_model_config_from_provider_model("gpt/not-configured")


if __name__ == "__main__":
    unittest.main()
