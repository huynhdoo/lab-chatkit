# ChatKit Starter Template (FastHTML Version)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![FastHTML](https://img.shields.io/badge/Built_with-FastHTML-blue)
![OpenAI API](https://img.shields.io/badge/Powered_by-OpenAI_API-orange)

FastHTML version of the ChatKit starter application. Uses FastHTML for the backend and HTMX for dynamic interactions.

## What You Get

- FastHTML backend with ChatKit web component integration
- API endpoint for creating ChatKit sessions
- Configuration file for starter prompts, theme, placeholder text, and greeting message
- HTMX-based dynamic interactions without build tools

## Getting Started

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your environment file

```bash
cp .env.example .env
```

Get your workflow ID from [Agent Builder](https://platform.openai.com/agent-builder) after clicking "Publish".

Get your OpenAI API key from [OpenAI API Keys](https://platform.openai.com/api-keys).

### 4. Configure ChatKit credentials

Update `.env` with:

- `OPENAI_API_KEY` — Your OpenAI API key (must be in same org/project as Agent Builder)
- `CHATKIT_WORKFLOW_ID` — The workflow ID from Agent Builder (starts with `wf_...`)
- (optional) `CHATKIT_API_BASE` — Custom base URL for ChatKit API

### 5. Run the app

```bash
python app/main.py
```

Or with uvicorn:

```bash
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000`

## Project Structure

```
openai-chatkit-fasthtml/
├── app/
│   ├── main.py           # FastHTML app entry point
│   ├── routes.py         # API routes
│   ├── config.py         # Configuration
│   └── static/           # Static assets (CSS, JS)
├── .env.example
├── .env                  # Environment variables
├── requirements.txt
└── README.md
```

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
ruff format .
ruff check . --fix
```
