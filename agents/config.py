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

def get_llm_config() -> dict:
    """Build an LLM config with Qwen3.8 27B (free, via OpenRouter)."""
    config_list = [{
        "model": "qwen/qwen3.8-27b:free",
        "api_key": _get_secret("OPENROUTER_API_KEY"),
        "base_url": "https://openrouter.ai/api/v1",
        "api_type": "openai",
    }]

    return {
        "config_list": config_list,
        "temperature": 0.7,
    }

LLM_CONFIG = None  # use get_llm_config() at call time
