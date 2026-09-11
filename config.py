"""

Application configuration for the MeshAPI-native RAG app.

All tunable values live here and are read from environment variables (loaded from
a local ``.env`` file via python-dotenv) so nothing sensitive is hard-coded. The
single most important value is ``MESH_API_KEY`` -- one MeshAPI key powers chat,
the managed RAG store, moderation, speech-to-text and text-to-speech, so there is
no vector-DB / embeddings / speech configuration to manage separately.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    
    meshapi_base_url: str = os.getenv("MESHAPI_BASE_URL", "https://api.meshapi.ai")
    meshapi_token: str = os.getenv("MESH_API_KEY") or os.getenv("MESHAPI_TOKEN") or ""
    meshapi_chat_model: str = os.getenv("MESHAPI_CHAT_MODEL", "openai/gpt-4o-mini")

    rag_top_k: int = int(os.getenv("RAG_TOP_K", "3"))

    tts_model: str = os.getenv("MESHAPI_TTS_MODEL", "hexgrad/kokoro-82m")
    tts_voice: str = os.getenv("MESHAPI_TTS_VOICE", "af_heart")
    stt_model: str = os.getenv("MESHAPI_STT_MODEL", "elevenlabs/scribe_v1")

    def validate(self) -> None:
        """Fail fast at startup if the one required credential is missing.

        Called from the FastAPI startup event so misconfiguration surfaces
        immediately with a readable message rather than deep inside an API call.
        """
        if not self.meshapi_token:
            raise RuntimeError("Missing required environment variable: MESH_API_KEY")


settings = Settings()