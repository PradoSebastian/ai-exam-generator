install:
	uv sync

image_reader:
	uv run main.py

exam_generator:
	uv run exam_generator_flow.py

ollama-claude:
	ollama launch claude --model gemma4:31b-cloud
