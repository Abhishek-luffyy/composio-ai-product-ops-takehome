# 100-App API Readiness Research Agent

This submission implements an evidence-first research pipeline. It takes the 100-app seed list, fetches first-party evidence pages, extracts page text, detects authentication/API signals, and records confidence. Unknown is preferred over guessing.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python research_agent.py --input apps.csv --output agent_output.csv
```

## Workflow
Seed list -> first-party docs -> fetch/extract -> deterministic auth/API detection -> evidence URL -> confidence -> human verification.

For production, add search/browser retrieval, page snapshots, an LLM normalization pass, and a stratified verification sample.
