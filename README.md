# AI Exam Generator

An AI-powered system designed to automatically generate school exams from images of student notebooks and reference exams. Built using the Google Agent Development Kit (ADK) and Gemini models, it transforms raw educational materials into structured, professional exam documents in Markdown and PDF formats.

## Requirements
- Python 3.12+
- Libraries:
  - `google-adk>=1.31.1`
  - `markdownify>=1.2.2`
- Google Studio AI account (free tier)
- `UV` installed in your local device

### Optionals
- `Make` installed in your local device
- Free tier suscription for `API Template` (for PDFs generation)

## Project Architecture
The application follows a modular service-oriented architecture built on the Google ADK:

- **Orchestration Layer**: `main.py` and `exam_generator_flow.py` act as the entry points, initializing services and triggering the processing pipeline.
- **Service Layer**: `ImageService` coordinates the overall workflow, managing image reading and agent execution.
- **Agent System**: A set of specialized LLM agents (Reader, Generator, Coordinator) that handle specific cognitive tasks.
- **Utility Layer**: A collection of helpers for image conversion (`ImageUtil`), path management (`PathUtil`), and Markdown export (`MarkdownUtil`).
- **Configuration**: Centralized settings managed through `.env` and `app/constants/agent_constants.py`.

## AI Agents
The system is powered by a suite of specialized agents built with the Google ADK:

- **Image Reader Agent**: Processes raw images of notebooks and reference exams, transforming them into a structured Markdown format. It extracts key information and organizes content with visual cues.
- **Exam Generator Agent**: Takes the structured Markdown output from the Image Reader and generates a comprehensive school exam. It can create multiple question types (multiple choice, fill-in-the-blanks, etc.) based on the reference material.
- **Coordinator Agent**: Acts as the orchestrator of the entire workflow, managing the delegation and data flow between the reader and generator agents to ensure a consistent end-to-end process.

## Agent Interaction Flow
The agents operate in a sequential pipeline to transform raw images into a final exam:

1. **Input Phase**: The `Coordinator Agent` identifies the target images and reference materials.
2. **Extraction Phase**: The `Image Reader Agent` processes the images and outputs a structured Markdown representation of the student's notes and reference exams.
3. **Synthesis Phase**: This structured Markdown is passed to the `Exam Generator Agent`, which applies pedagogical logic to create a balanced and relevant exam.
4. **Output Phase**: The final generated exam is saved as a Markdown file in the configured results directory.

## Configuration

Before running the application, create an `.env` file in the project root with the following required environment variables:

```bash
# Gemini Configuration
GEMINI_MODEL=gemini-2.5-flash          # Gemini model to use
MODEL_TEMPERATURE=0.7                  # Generation temperature (0.0 - 1.0)
GEMINI_API_KEY=xxx                     # Your Gemini API Key
GOOGLE_GENAI_USE_VERTEXAI=0            # Set to 0 for API Key, 1 for Vertex AI

# Paths Configuration
FILES_PATH=resources/input             # Folder with input images (must be inside of app directory)
RESULTS_PATH=resources/output          # Folder for Markdown output (will be inside of app directory)
CSV_IMAGE_FILE_PATH=images.csv        # CSV file with image info (relative to FILES_PATH)
CSV_CUSTOM_CHARACTERS_FILE_PATH=custom_characters.csv # CSV with custom chars (relative to FILES_PATH)
SPECIAL_CONSIDERATIONS_FILE_PATH=special_considerations.txt # Special considerations file (relative to FILES_PATH)

# Application Settings
INCLUDE_ANSWERS=False                  # Include answers in output (True/False)
AVOID_IMAGE_READING=false             # Skip image reading process (true/false)

# API Template (PDF Export) Configuration
API_TEMPLATE_URL=https://rest.apitemplate.io/v2/ # Base URL for API Template
API_TEMPLATE_API_KEY=NONE              # Your API Template API Key
API_TEMPLATE_MD_TO_PDF_ENDPOINT=create-pdf-from-markdown # Endpoint for MD to PDF conversion
```

## Steps

0. Install dependencies
   - MAKE: `make install`
   - UV: `uv sync`

1. Fill `notebooks` and `reference_exams` to your input folder described in `FILES_PATH`
   - Create the folders if they don't exist and add your source files (markdown, notebooks, images, references).
   - Example structure:
     - netebook/
     - reference_exams/
   - Order does not matter for artifactory registry.
   - Optional files can be helpful:
      - custom_characters.csv (two column csv containing `<character_name>;<image_url>` rows, without headers)
      - images.csv (two column csv containing `<object_reference_name>;<image_url>` rows, without headers)
      - special_considerations.txt (txt containing additional indications more specific for the exam generation)

2. Run the program using
   - MAKE: `make exam_generator`
   - UV: `uv run exam_generator_flow.py`

This would generate the MD files into the `RESULTS_PATH`.

3. Convert the Markdown file to PDF
   - **Manual Method**: Use the Markdown-to-PDF tool: https://apitemplate.io/pdf-tools/convert-markdown-to-pdf/
   - **Automatic Method (Optional)**: You can automate PDF generation by integrating with the API Template API.
     - API Documentation: [Create PDF from Markdown](https://apitemplate.io/apiv2/#tag/API-Integration/operation/create-pdf-from-markdown)
     - Configuration: Add your `API_TEMPLATE_API_KEY` to the `.env` file.
     - **Disclaimer**: The free tier provides 50 PDF generations per month.

## Notes

- Keep assets (images, attachments) referenced with relative paths so the converter can include them.
- Name files clearly (e.g., `exam_math_2026.md`) to avoid confusion when batch converting.
