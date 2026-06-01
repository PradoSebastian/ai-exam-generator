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
AVOID_IMAGE_READING=os.getenv("AVOID_IMAGE_READING", "false").lower() == "true"
FILES_PATH=os.getenv("FILES_PATH", "resources/input")
RESULTS_PATH=os.getenv("RESULTS_PATH", "resources/output")
CSV_IMAGE_FILE_PATH=f"{FILES_PATH}/" + os.getenv("CSV_IMAGE_FILE_PATH", "images.csv")
CSV_CUSTOM_CHARACTERS_FILE_PATH=f"{FILES_PATH}/" + os.getenv("CSV_CUSTOM_CHARACTERS_FILE_PATH", "custom_characters.csv")
SPECIAL_CONSIDERATIONS_FILE_PATH=f"{FILES_PATH}/" + os.getenv("SPECIAL_CONSIDERATIONS_FILE_PATH", "special_considerations.txt")

APP_NAME="image_transformer_app"

USER_ID="local_user"

GENERATED_FOLDER = "generated"
GENERATED_DEFAULT_FILE_NAME = "resulted_markdown"

# Output keys
IMAGE_READER_OUTPUT_KEY="image_reader_output"
EXAM_GENERATOR_OUTPUT_KEY="exam_generator_output"

# Context Keys
INCLUDE_ANSWERS_KEY="include_answers"
IMAGE_ARTIFACTS_KEY="image_artifacts"
IMAGE_REFERENCES_KEY="image_references"

CUSTOM_CHARACTERS_KEY="custom_characters"
MARKDOWN_ARTIFACTS_KEY="markdown_artifacts"
SPECIAL_CONSIDERATIONS_KEY="special_considerations"

# File names
IMAGE_READER_OUTPUT_FILE_NAME="image_reader_output_file"
EXAM_GENERATOR_OUTPUT_FILE_NAME="exam_generator_output_file"

# API Template config
API_TEMPLATE_URL=os.getenv("API_TEMPLATE_URL", "https://rest.apitemplate.io/v2/")
API_TEMPLATE_API_KEY=os.getenv("API_TEMPLATE_API_KEY", "NONE")
API_TEMPLATE_MD_TO_PDF_ENDPOINT=os.getenv("API_TEMPLATE_MD_TO_PDF_ENDPOINT", "create-pdf-from-markdown")

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