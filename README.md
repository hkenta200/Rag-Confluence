# RAG-Confluence

**RAG Architecture**
<img width="1033" height="579" alt="RAG-confluence" src="https://github.com/user-attachments/assets/5276e463-b734-4993-ba20-302f5e6b9a3c" />

This project ingests Confluence pages into a PostgreSQL-backed vector store and exposes a chat interface for answering queries using LangChain and the OpenAI API.

## Features

- Ingest Confluence content by space key
- Upload and index plain text files
- Use a FastAPI backend with LangChain retrieval and OpenAI embeddings
- Store vectors in PostgreSQL + PGVector
- Frontend React app for chat-based querying
- Docker Compose setup for local development

## Tech stack

- Frontend: React
- Backend: FastAPI
- Vector database: PostgreSQL + PGVector
- Embeddings / LLM: OpenAI via LangChain
- Container orchestration: Docker Compose

## Getting started

### 1. Copy environment variables

Create a local environment file from the example:

```bash
cp backend/.env.example backend/.env
```

Then update `backend/.env` with your own values.

### 2. Required environment variables

In `backend/.env`, set:

- `OPENAI_API_KEY`
- `CONFLUENCE_BASE_URL`
- `CONFLUENCE_EMAIL`
- `CONFLUENCE_API_TOKEN`
- `CONFLUENCE_SPACE_KEY` (optional)
- `POSTGRES_PASSWORD`

The Docker Compose setup also uses these defaults unless overridden:

- `POSTGRES_USER=postgres`
- `POSTGRES_DB=rag_db`
- `POSTGRES_HOST=db`
- `POSTGRES_PORT=5432`

### 3. Start the app with Docker Compose

From the project root:

```bash
docker compose up --build
```

This starts:

- PostgreSQL database on `localhost:5432`
- Backend API on `http://localhost:8000`
- Frontend app on `http://localhost:3000`

### 4. Use the app

- Open the frontend: `http://localhost:3000`
- Send a POST request to ingest Confluence pages:

```bash
curl -X POST http://localhost:8000/ingest \
  -H 'Content-Type: application/json' \
  -d '{"space_key": "YOUR_SPACE_KEY", "limit": 500}'
```

- Send a chat query:

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"query": "What is the deployment process?", "k": 4}'
```

- Upload a text file for indexing:

```bash
curl -F "file=@example.txt" http://localhost:8000/ingest-file
```

## Query flow

1. The frontend sends the user question to `POST /chat`.
2. The backend loads the saved `PGVector` vector store from PostgreSQL.
3. The top `k` matching text chunks are retrieved from the vector store.
4. The retrieved chunks are inserted into a prompt template.
5. `ChatOpenAI` is called with that prompt to generate an answer.
6. The backend returns the answer plus source metadata from the retrieved documents.

This means the app answers questions by first retrieving relevant Confluence content from the vector store, then using the LLM to generate a response based on that context.

## Local development

If you prefer not to use Docker, install dependencies manually:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

Then run the backend directly:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

Install frontend dependencies and start the React app:

```bash
cd frontend
npm install
npm start
```

## Important notes

- Do not commit `backend/.env` or any file containing real credentials.
- `backend/.env.example` is safe to track and should be used as the template.
- `.gitignore` already excludes `.env`, `.env.*`, `backend/.venv`, and `node_modules`.

## Project structure

- `backend/` – FastAPI backend with ingestion, chat, and vector store logic
- `frontend/` – React chat interface
- `docker-compose.yml` – local service orchestration
- `.gitignore` – excludes secrets and build artifacts
