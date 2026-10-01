import os
from dotenv import load_dotenv

load_dotenv()

def _get_secret(key: str) -> str:
    val = os.environ.get(key, "")
    if not val:
        try:
            import streamlit as st
            val = st.secrets.get(key, "")
        except Exception:
            pass
    return val

# Free OpenRouter models, tried in order. Free models share a rate-limited
# upstream pool, so ag2 moves to the next entry when one returns a 429.
FREE_MODELS = [
    "qwen/qwen3.8-27b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
]

def get_llm_config() -> dict:
    """Build an LLM config of free OpenRouter models with fallbacks."""
    api_key = _get_secret("OPENROUTER_API_KEY")
    config_list = [
        {
            "model": model,
            "api_key": api_key,
            "base_url": "https://openrouter.ai/api/v1",
            "api_type": "openai",
            "price": [0, 0],
        }
        for model in FREE_MODELS
    ]

    return {
        "config_list": config_list,
        "temperature": 0.7,
    }

LLM_CONFIG = None  # use get_llm_config() at call time
