import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from llm_client.client import LLMClient
from llm_client.config import LLMSettings, load_settings
from llm_client.providers import parse_provider_response


class TestLLMClient(unittest.TestCase):
    def test_load_settings_reads_env(self):
        with patch("llm_client.config.getenv") as mocked_getenv:
            mocked_getenv.side_effect = lambda key, default=None: {
                "LLM_PROVIDER": "gemini",
                "LLM_MODEL": "gemini-2.0-flash",
                "GEMINI_API_KEY": "abc123",
            }.get(key, default)
            settings = load_settings()
            self.assertEqual(settings.provider, "gemini")
            self.assertEqual(settings.model, "gemini-2.0-flash")
            self.assertEqual(settings.api_key, "abc123")

    def test_invalid_provider_raises(self):
        with self.assertRaises(ValueError):
            LLMClient(settings=LLMSettings(provider="unknown", model="x", api_key="key"))

    def test_parse_provider_response_openai(self):
        payload = {
            "choices": [{"message": {"content": "Hola desde OpenAI"}}]
        }
        self.assertEqual(parse_provider_response("openai", payload), "Hola desde OpenAI")

    def test_parse_provider_response_anthropic(self):
        payload = {
            "content": [
                {"type": "text", "text": "Hola desde Anthropic"},
                {"type": "text", "text": " y más"},
            ]
        }
        self.assertEqual(parse_provider_response("anthropic", payload), "Hola desde Anthropic y más")

    def test_parse_provider_response_gemini(self):
        payload = {
            "candidates": [{
                "content": {"parts": [{"text": "Hola desde Gemini"}, {"text": "!"}]}
            }]
        }
        self.assertEqual(parse_provider_response("gemini", payload), "Hola desde Gemini!")

    def test_generate_sync_uses_async_path(self):
        client = LLMClient(settings=LLMSettings(provider="gemini", model="gemini-2.0-flash", api_key="key"))
        client._request = AsyncMock(return_value={"candidates": [{"content": {"parts": [{"text": "Respuesta"}]}}]})
        self.assertEqual(client.generate("Pregunta"), "Respuesta")


if __name__ == "__main__":
    unittest.main()
