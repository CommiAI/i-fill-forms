# I-Fill-Forms

## Quick Setup

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (for Qdrant vector database)

### Installation

1. Clone the repository and navigate to backend:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
# Or using uv
uv init
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# OR if using uv
uv sync
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY or GROQ_API_KEY (required)
```

5. Start Qdrant vector database:
```bash
docker-compose up -d
```

6. Run the backend:
```bash
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

## Stopping Services

```bash
# Stop the backend server: Ctrl+C
# Stop Qdrant database:
docker-compose down
```