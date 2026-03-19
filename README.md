# 📊 Data Summarizer for LLMs

> **Generate compact, context-rich dataset summaries optimized for Large Language Models (Gemini, ChatGPT, Claude).**

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Polars](https://img.shields.io/badge/Polars-Fast-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://github.com/abguven/data-summarizer-llm/actions/workflows/ci.yml/badge.svg)

---

## ⚡ TL;DR — 3 steps, no Python required

```bash
git clone https://github.com/abguven/data-summarizer-llm.git
cd data-summarizer-llm

make demo        # Try with sample data right away
```

> No `make`? Use `./run.sh --demo` (Linux/Mac) or see the [manual commands](#-manual-docker-commands) below.

Drop your own files in `data/input/` then run `make run`. Summaries land in `data/output/`.

---

## 🧐 Why this tool?

When working with LLMs (like Gemini or Claude), you often need to provide context about your data without uploading the entire 100MB CSV file (which consumes tokens and context window).

This tool reads your datasets (CSV, Excel, JSON, Parquet) and generates a **lightweight Markdown summary** containing:

- ✅ Column names & Types
- ✅ Missing values percentage
- ✅ Unique value counts
- ✅ **ASCII Distributions** for numeric columns (`▂▃▅█`)
- ✅ Sample values

You can then simply copy-paste or attach this Markdown summary to your LLM prompt.

---

## 🏁 Getting started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running. That's it.

### Step 1 — Clone

```bash
git clone https://github.com/abguven/data-summarizer-llm.git
cd data-summarizer-llm
```

### Step 2 — Add your data

Drop your files (`.csv`, `.xlsx`, `.json`, `.parquet`) into:

```text
data/input/      <-- your files go here
```

The `data/input/` and `data/output/` folders already exist in the repo. No need to create them.

### Step 3 — Run

```bash
make run
```

That's it. Summaries appear in `data/output/` as `SUMMARY_<filename>.md`.

---

## 🎮 Available commands

| Command | Description |
| --- | --- |
| `make run` | Summarize all files in `data/input/` |
| `make demo` | Try with sample data (CSV + JSON included) |
| `make test` | Run the functional test suite |
| `make build` | Build the Docker image locally (for development) |
| `make help` | Show all commands |

---

## 📄 Example output

Given a file `employees.csv`, the tool generates `SUMMARY_employees.csv.md`:

```markdown
# 📊 Dataset Summary: employees.csv
- **Rows:** 1000
- **Columns:** 5

## 🧱 Column Details
| Column    | Type    | Missing | Unique | Stats / Distribution            | Examples               |
|-----------|---------|---------|--------|---------------------------------|------------------------|
| name      | String  | 0.0%    | 1000   |                                 | Alice, Bob, Charlie    |
| age       | Int64   | 2.0%    | 45     | Min:18 Max:75 Avg:42 `▂▃▅█▅▃▂` | 25, 30, 35             |
| city      | String  | 0.5%    | 23     |                                 | Paris, Lyon, Marseille |
| salary    | Float64 | 0.0%    | 850    | Min:2000 Max:9500 Avg:4800 `▂▃▄▅▆` | 3200.0, 4500.0     |
| is_active | Boolean | 0.0%    | 2      |                                 | true, false            |
```

Paste this directly into your LLM prompt instead of the full CSV.

---

## 🛠️ Features

- **Blazing Fast:** Built on top of **Polars** (Rust-based DataFrame library).
- **Format Support:** `.csv`, `.parquet`, `.json`, `.xlsx`, `.xls`.
- **Robust Excel:** Includes a fallback mechanism (FastExcel → Xlsx2csv) to handle complex or older Excel files.
- **Privacy First:** Runs entirely locally in a container. No data leaves your machine.
- **Batch Processing:** Analyzes all files in the `input` directory at once.

---

## 🔧 Manual Docker commands

No `make` or `./run.sh`? Use these directly.

**Linux / Mac:**

```bash
docker run --rm \
  -v "$(pwd)/data/input:/app/data/input" \
  -v "$(pwd)/data/output:/app/data/output" \
  abguven/data-summarizer:latest
```

**Windows (PowerShell):**

```powershell
docker run --rm `
  -v "${PWD}/data/input:/app/data/input" `
  -v "${PWD}/data/output:/app/data/output" `
  abguven/data-summarizer:latest
```

---

## 📦 For developers

If you want to modify the source code:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (adjust paths if needed)
python src/summarize_dataset.py
```

To build and test your local image:

```bash
make build
bash tests/run_tests.sh data-summarizer:local
```

---

## 🤝 Contributing

Feel free to open issues or submit PRs! Ideas welcome:

- SQL database support
- More advanced statistics
- Output formats (JSON, HTML)

---

*Created by [abguven](https://github.com/abguven) for Data Engineering workflows.*
