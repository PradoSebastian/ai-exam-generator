install:
	uv sync

run image_reader:
	uv run main.py

ollama-claude:
	ollama launch claude
