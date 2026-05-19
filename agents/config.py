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
    """Build an LLM config with DeepSeek (free, via OpenRouter) as primary
    and Groq llama-3.3-70b-versatile as fallback.  ag2 tries each entry in
    config_list in order, moving to the next on rate-limit or error."""
    config_list = []

    openrouter_key = _get_secret("OPENROUTER_API_KEY")
    if openrouter_key:
        config_list.append({
            "model": "deepseek/deepseek-v4-flash:free",
            "api_key": openrouter_key,
            "base_url": "https://openrouter.ai/api/v1",
            "api_type": "openai",
        })

    groq_key = _get_secret("GROQ_API_KEY")
    if groq_key:
        config_list.append({
            "model": "llama-3.3-70b-versatile",
            "api_key": groq_key,
            "base_url": "https://api.groq.com/openai/v1",
            "api_type": "openai",
        })

    if not config_list:
        # Last-resort placeholder so the app at least starts and shows a clear error
        config_list.append({
            "model": "llama-3.3-70b-versatile",
            "api_key": "",
            "base_url": "https://api.groq.com/openai/v1",
            "api_type": "openai",
        })

    return {
        "config_list": config_list,
        "temperature": 0.7,
    }

LLM_CONFIG = None  # use get_llm_config() at call time
