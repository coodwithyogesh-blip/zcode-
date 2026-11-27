# KHUDA AI — Personal AI Workspace

A browser-based personal AI workspace published with GitHub Pages.

## Current features
- Gemini and OpenAI chat connections; configurable OpenAI-compatible endpoints for other providers/models.
- Session-only API keys: keys are held in memory and are not written to this repository or browser storage.
- Local knowledge library for text/code files, simple keyword retrieval, source labels and JSON export.
- Optional folder attachment in browsers supporting the File System Access API. The app can write a backup to `KHUDA_AI_STORAGE/knowledge.json` in the selected folder.
- Public URL import when the remote site allows browser CORS access.
- Conversation history and scope notes stored in this browser.
- Security Lab notes for authorized bug-bounty learning.

## Publish on GitHub Pages
1. Open repository **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. The existing `.github/workflows/static.yml` workflow deploys the repository root after a push to `main`.
4. Open the Pages URL shown in Settings → Pages after the workflow succeeds.

## Run locally
Open `index.html` in a modern browser. For folder attachment, URL import and best compatibility, serve it over HTTPS or localhost. GitHub Pages provides HTTPS automatically.

## Important limitations
- This is a static, single-user browser app. It has no server-side backend, user authentication, server-side secret storage, scheduled agent, or background job runner.
- API keys are only held in JavaScript memory for the current tab. Browser API calls may be blocked by provider CORS policy. For a public or multi-user deployment, add an authenticated backend and keep provider keys server-side.
- Knowledge is retrieval-based (RAG), not model-weight fine-tuning. The app searches local text and supplies relevant excerpts to the selected model.
- Supported text formats: TXT, MD, JSON, CSV, HTML, XML, YAML, common source-code text and LOG. One file is limited to 1 MB. PDF/DOCX parsing is not included yet.
- URL learning only works when the target allows browser CORS. This app does not bypass access controls.
- Folder access depends on browser support and the permission granted by the user. Browser storage can be cleared by the browser; export backups regularly.
- Security Lab is a notes and learning area only. It does not scan or exploit targets. Test only systems for which you have explicit authorization.

## Privacy
Files are processed in the browser. When you send a prompt, the question and selected matching knowledge excerpts are sent to the AI provider configured by you. Review that provider's privacy and retention terms before use. Never upload secrets or sensitive third-party data without permission.
