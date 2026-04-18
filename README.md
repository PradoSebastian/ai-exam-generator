# AI Exam Generator

Short README with steps to prepare exam materials and export them to PDF.

## Steps

1. Fill `notebook` and `reference_exams`
   - Create the folders if they don't exist and add your source files (markdown, notebooks, images, references).
   - Example structure:
     - netebook/
     - reference_exams/

2. Ask Claude to define a new Markdown file
   - Prompt example you can send to Claude:
     > "Create a new Markdown file named `exam_<topic>.md` with sections: Title, Instructions, Questions, Answers, References. Use clear headings and include any images as relative links."
   - Save the returned content into the desired `.md` file inside your repo.

3. Convert the Markdown file to PDF
   - Use the Markdown-to-PDF tool: https://apitemplate.io/pdf-tools/convert-markdown-to-pdf/
   - Follow the site or API instructions to upload/submit your `.md` and obtain a PDF output.

## Configuration

Before running the application, create an `.env` file in the project root with the following required environment variables:

```bash
GEMINI_MODEL=gemini-2.5-flash          # Gemini model to use
MODEL_TEMPERATURE=0.7                  # Generation temperature (0.0 - 1.0)
GOOGLE_GENAI_USE_VERTEXAI=0            # Set to 0 for API Key, 1 for Vertex AI
GEMINI_API_KEY=xxx                     # Your Gemini API Key
FILES_PATH=resources/input             # Folder with input images
RESULTS_PATH=resources/output          # Folder for Markdown output
INCLUDE_ANSWERS=False                  # Include answers in output (True/False)
```

## Running the Application

You can run the main application using uv:

```bash
uv run main.py
```

## Launching Claude Code

To start Claude Code using ollama:

```bash
ollama launch code
```

Example prompt:
```
Quiero generar un examen en español usando esta informacion @Tercero/Ciencias/resources/notebooks/Unit_2.mc usando un examen de referencia como: @Tercero/Ingles/results/2026-03-23_Unit_2_exam.md y colocalo en @Tercero/Ciencias/results\ como un md
```

## Notes

- Keep assets (images, attachments) referenced with relative paths so the converter can include them.
- Name files clearly (e.g., `exam_math_2026.md`) to avoid confusion when batch converting.
