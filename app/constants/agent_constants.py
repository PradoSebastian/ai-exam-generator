import logging
import dotenv
import os

from google.adk.agents.context_cache_config import ContextCacheConfig
import google.genai.types as types

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)

GEMINI_MODEL=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MODEL_TEMPERATURE=float(os.getenv("MODEL_TEMPERATURE", 0.7))
INCLUDE_ANSWERS=os.getenv("INCLUDE_ANSWERS", "true").lower() == "true"

FILES_PATH=os.getenv("FILES_PATH", "files")

RESULTS_PATH=os.getenv("RESULTS_PATH", "results")

APP_NAME="image_transformer_app"

USER_ID="local_user"

INCLUDE_ANSWERS_KEY="include_answers"

# Output keys
IMAGE_READER_OUTPUT_KEY="image_reader_output"
EXAM_GENERATOR_OUTPUT_KEY="exam_generator_output"

# File names
IMAGE_READER_OUTPUT_FILE_NAME="image_reader_output"
EXAM_GENERATOR_OUTPUT_FILE_NAME="exam_generator_output"

RETRY_CONFIG = types.HttpRetryOptions(
    attempts=3,
    exp_base=5,
    initial_delay=10,
    max_delay=60,
    http_status_codes=[429, 500, 503, 504]
)

GENERAL_CONTENT_MODEL_CONFIG = types.GenerateContentConfig(
    temperature=MODEL_TEMPERATURE,
    http_options=types.HttpOptions(retry_options=RETRY_CONFIG),
    thinking_config=None
)

CONTEXT_CACHE_CONFIG = ContextCacheConfig(
    min_tokens = 8292,
    ttl_seconds = 3600,
    cache_intervals = 20,
)