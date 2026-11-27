# KHUDA AI — Learning & Execution Agent

KHUDA AI is evolving from a static chat page into a personal agent with persistent knowledge, a file workspace, and a controlled task executor.

## Project structure

- `index.html`: GitHub Pages interface. Includes chat, knowledge management, model connection, and the Learning & Execution Agent panel.
- `backend/main.py`: FastAPI service for persistent knowledge ingestion, retrieval, workspace tools, and bounded model-driven agent runs.
- `khuda_workspace/knowledge`: indexed source text, metadata, and chunks.
- `khuda_workspace/workspace`: files the agent may inspect or modify when explicitly permitted.
- `khuda_workspace/reports`: generated reports.
- `render.yaml`: Render Blueprint configuration.

Knowledge ingestion is retrieval-based learning (RAG), not model-weight fine-tuning. Original text, source metadata, and chunks persist in the backend data directory and can be retrieved in later tasks.

## Deploy on Render

1. Open Render and create a new Blueprint using this repository, or create a Python web service from the repo.
2. Render reads `render.yaml` and generates `KHUDA_ACCESS_TOKEN`. Keep this token private.
3. After deploy, open the service's `/api/health` endpoint.
4. Copy the HTTPS service URL and generated access token into KHUDA AI → Learning & Execution Agent.
5. In AI Models, connect Gemini, OpenAI, or an OpenAI-compatible provider. The model API key is sent per task and is not stored by this backend.

**Storage warning:** Render Free filesystems are ephemeral. The free instance may lose knowledge and workspace files on restart or redeploy. For durable learning, attach persistent storage on a plan that supports disks, or configure `KHUDA_DATA_DIR` to storage you control. Do not treat free Render storage as permanent.

## Agent features

- Upload text/code files into persistent backend knowledge.
- Import public HTTPS text pages.
- Retrieve matching knowledge for each task.
- Run a bounded agent loop that can list/read workspace files, search learned knowledge, write approved files, save reports, and passively inspect an explicitly scoped public URL.
- Select the AI provider and model from the existing AI Models panel.
- Agent writes are off by default and require the per-task permission checkbox.

## API

- `GET /api/health` — service status.
- `POST /api/knowledge/upload` — multipart text/code document ingestion (1 MB per file).
- `POST /api/knowledge/url` — fetch and index public HTTPS text pages.
- `POST /api/agent/run` — run a bounded tool loop with Gemini, OpenAI, or an OpenAI-compatible provider.
- `GET /api/workspace/files` — list workspace files.
- `POST /api/workspace/write` — explicitly write a workspace file.

All routes except health require `Authorization: Bearer <KHUDA_ACCESS_TOKEN>`. Model API keys are request-scoped and are not saved by the server.

## Safety boundaries

- Path traversal is blocked; agent tools operate only inside the configured workspace.
- URL ingestion accepts HTTPS only, blocks private/loopback/reserved IPs, and does not follow redirects.
- Security URL inspection is passive only and requires the hostname to appear in the written authorization scope.
- No port scanning, brute force, exploit execution, authentication bypass, destructive testing, or data exfiltration.
- Uploaded files and fetched web content are untrusted reference material, never agent instructions.
- Do not commit API keys, access tokens, or sensitive files.

## Run locally

```bash
python -m pip install -r requirements.txt
KHUDA_ALLOW_NO_AUTH=true uvicorn backend.main:app --host 127.0.0.1 --port 8000
python -m unittest discover -s tests -p 'test_*.py'
node tests/test-site.mjs
```

Only use `KHUDA_ALLOW_NO_AUTH=true` for local testing. Never enable it on a public server.

## Current limitations

- The backend is a separate service; GitHub Pages remains the static frontend.
- PDF/DOCX extraction, local Android folder sync, persistent user login/roles, background jobs, and full active security testing are not implemented yet.
- A successful agent task depends on a valid provider API key, model availability, backend connectivity, and the configured step limit.
