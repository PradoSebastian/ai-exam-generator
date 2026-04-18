# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sistema para generar exámenes escolares a partir de imágenes de cuadernos y exámenes de referencia usando agents de Google ADK (Agent Development Kit) con modelos Gemini.

## Commands

### Run the Application

```bash
uv run main.py
```

### Install Dependencies

```bash
uv sync
```

### Development Dependencies

Dependencies are managed via `pyproject.toml`:
- `google-adk`: Framework de agents de Google
- `markdownify`: Conversión a Markdown

## Architecture

### Entry Point (`main.py`)

Orquesta asíncrona que inicializa `ImageService` y dispara el procesamiento de imágenes.

### Service Layer (`app/business/`)

**`image_service.py`**: Servicio principal que coordina el flujo de trabajo.
- Lee imágenes desde `FILES_PATH` (configurable via `.env`)
- Inicializa `AgentRunner` con `ImageReaderAgent`
- Envía las imágenes al agente LLM
- Guarda la respuesta en Markdown vía `MarkdownUtil`

### Agent System (`app/agent/`)

Basado en Google ADK (Agent Development Kit). Arquitectura de agents LLM:

**`image_reader_agent.py`**: Agente LLM que procesa imágenes.
- Modelo: Gemini (configurable via `GEMINI_MODEL` env var)
- Prompt: `IMAGE_READER_PROMPT` - transforma imágenes a estructura Markdown
- Extrae texto de cuadernos y exámenes, organiza con emojis/iconos
- Guarda output automáticamente via `after_agent_callback`
- Responde a flag `INCLUDE_ANSWERS` para incluir/ocultar respuestas

**`exam_generator_agent.py`**: Agente LLM para generar exámenes.
- Recibe Markdown de `ImageReaderAgent`
- Genera exámenes estructurados basados en contenido de referencia
- Soporta múltiples tipos de preguntas (opción múltiple, completar, etc.)

**`coordinator_agent.py`**: Agente coordinador (extensible).
- Hereda de `BaseAgent` de ADK
- Actualmente delega a `ImageReaderAgent`, preparado para orquestar múltiples agents

**`config/runner.py`**: `AgentRunner` - orquestador de ejecución.
- Usa `InMemorySessionService` para sesiones efímeras
- Maneja `Runner` de ADK con configuración de retry y context cache
- Inyecta estado inicial (`INCLUDE_ANSWERS_KEY`)

### Utilities (`app/util/`)

**`image.py`**: `ImageUtil` - lectura de imágenes.
- Soporta: jpg, png, gif, bmp, tiff, webp
- Convierte imágenes a `types.Part` de Google GenAI
- Escaneo recursivo de directorios

**`md.py`**: `MarkdownUtil` - escritura de archivos Markdown.
- Genera archivos con timestamp: `{file_name}-{date}.md`
- Output a `RESULTS_PATH` (configurable via `.env`)

**`path.py`**: `PathUtil` - resolución de paths relativos al proyecto.

### Constants (`app/constants/`)

**`agent_constants.py`**: Configuración centralizada.
- Variables desde `.env`: `GEMINI_MODEL`, `MODEL_TEMPERATURE`, `INCLUDE_ANSWERS`
- Paths: `FILES_PATH` (input), `RESULTS_PATH` (output)
- Keys de estado: `IMAGE_READER_OUTPUT_KEY`, `EXAM_GENERATOR_OUTPUT_KEY`
- Configuración de retry HTTP para API de Gemini

### Prompts (`app/agent/prompt/`)

Definiciones de prompts para agents:
- `image_reader_prompt.py`: Instrucciones para extracción de contenido de imágenes
- `exam_generator_prompt.py`: Instrucciones para generación de exámenes

## Configuration

### Environment Variables (`.env`)

```bash
GEMINI_MODEL=gemini-2.5-flash          # Modelo Gemini a usar
MODEL_TEMPERATURE=0.7                  # Temperatura de generación
GEMINI_API_KEY=xxx                     # API Key de Gemini
GOOGLE_GENAI_USE_VERTEXAI=0            # 0=API Key directa, 1=Vertex AI

FILES_PATH=resources/input             # Carpeta de imágenes de entrada
RESULTS_PATH=resources/output          # Carpeta de resultados Markdown

INCLUDE_ANSWERS=False                  # Incluir respuestas en output
```

## Flujo de Trabajo Manual (Estructura de Carpetas)

El proyecto también soporta un flujo manual de organización de materiales escolares:

```
Tercero/
├── Ingles/
│   ├── resources/
│   │   ├── notebooks/          # Fotos de cuadernos del estudiante
│   │   └── reference_exams/   # Exámenes de referencia de otros
│   └── results/                 # Exámenes generados (Markdown)
└── Frances/
    └── ... (misma estructura)
```

### Proceso Manual

1. **Guardar imágenes**: `Tercero/{Asignatura}/resources/{notebooks|reference_exams}/`
   - Nomenclatura: `YYYY-MM-DD_descripcion.jpg`

2. **Generar exámenes**: El agente lee imágenes, extrae contenido y genera Markdown en `results/`

3. **Idioma**: Los exámenes se generan en el idioma de la asignatura (Inglés/Francés)

## Extension Points

- **Nuevos agents**: Extender `BaseAgent` de ADK, registrar en `AgentRunner`
- **Nuevos prompts**: Agregar en `app/agent/prompt/`, importar en agente
- **Nuevos tipos de archivo**: Extender `ImageUtil` para soportar más formatos
- **Persistencia**: Reemplazar `InMemorySessionService` con implementación persistente

## Notas Técnicas

- Framework: Google ADK (`google-adk`) sobre Python 3.12+
- Gestor de dependencias: `uv` (no pip directo)
- Async/await: Todo el flujo de agents es asíncrono
- Logging: Configurado en `agent_constants.py` (nivel INFO por defecto)
