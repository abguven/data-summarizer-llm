# 📊 Data Summarizer for LLMs

> **Generate compact, context-rich dataset summaries optimized for Large Language Models (Gemini, ChatGPT, Claude).**

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Polars](https://img.shields.io/badge/Polars-Fast-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://github.com/abguven/data-summarizer-llm/actions/workflows/ci.yml/badge.svg)

## 🧐 Why this tool?
When working with LLMs (like Gemini or Claude), you often need to provide context about your data without uploading the entire 100MB CSV file (which consumes tokens and context window).

This tool reads your datasets (CSV, Excel, JSON, Parquet) and generates a **lightweight Markdown summary** containing:
- ✅ Column names & Types
- ✅ Missing values percentage
- ✅ Unique value counts
- ✅ **ASCII Distributions** for numeric columns (` ▂▃▅█`)
- ✅ Sample values

You can then simply copy-paste or attach this Markdown summary to your LLM prompt.

---

## 🚀 Quick Start (Docker)

No Python installation required. Just use Docker.

### 1. Structure
Create two folders on your computer:
```
my_project/
├── input/   <-- Put your CSV/Excel files here
└── output/  <-- Summaries will appear here
```

### 2. Run
**Windows (PowerShell):**
```powershell
docker run --rm `
  -v "${PWD}/input:/app/data/input" `
  -v "${PWD}/output:/app/data/output" `
  abguven/data-summarizer:latest
```

**Linux / Mac:**
```bash
docker run --rm \
  -v "$(pwd)/input:/app/data/input" \
  -v "$(pwd)/output:/app/data/output" \
  abguven/data-summarizer:latest
```

---

## 🛠️ Features

- **Blazing Fast:** Built on top of **Polars** (Rust-based DataFrame library).
- **Format Support:** `.csv`, `.parquet`, `.json`, `.xlsx`, `.xls`.
- **Robust Excel:** Includes a fallback mechanism (FastExcel -> Xlsx2csv) to handle complex or older Excel files.
- **Privacy First:** Runs entirely locally in a container. No data leaves your machine.
- **Batch Processing:** Analyzes all files in the `input` directory at once.

---

## 📦 Installation (For Developers)

If you want to modify the code or run it without Docker:

```bash
# Clone the repo
git clone https://github.com/abguven/data-summarizer-llm.git
cd data-summarizer-llm

# Install dependencies
pip install -r requirements.txt

# Run
python src/summarize_dataset.py
```
*(Note: You'll need to adjust input/output paths in the script if running locally without Docker)*

---

## 🤝 Contributing
Feel free to open issues or submit PRs if you want to add support for SQL databases or more advanced statistics!

---
*Created by [abguven](https://github.com/abguven) for Data Engineering workflows.*
