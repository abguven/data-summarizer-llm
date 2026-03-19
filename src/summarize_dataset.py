#!/usr/bin/env python3
"""
Dataset Summarizer for LLMs
-------------------------------------
Reads a dataset (CSV, JSON, Excel, Parquet) using Polars
and generates a compact Markdown summary optimized for
Large Language Models (LLMs) like Gemini, ChatGPT, or Claude.
"""

import polars as pl
import os
import sys
import logging
import math

# Path Configuration (Hardcoded for Docker environment)
INPUT_DIR = "/app/data/input"
OUTPUT_DIR = "/app/data/output"
LOG_DIR = "/app/logs"
LOG_FILE = os.path.join(LOG_DIR, "execution.log")

# Logging Configuration
def setup_logging():
    handlers = [logging.StreamHandler(sys.stdout)]
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        handlers.append(logging.FileHandler(LOG_FILE))
    except PermissionError:
        pass  # Log directory not writable (e.g. no -v logs mount), stdout only
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )

def get_ascii_histogram(series: pl.Series, bins: int = 10) -> str:
    """Generates a simple ASCII histogram for a numeric column."""
    try:
        # Drop nulls
        s = series.drop_nulls()
        if s.len() == 0:
            return ""
        
        min_val = s.min()
        max_val = s.max()
        if min_val == max_val:
            return ""

        # Use Polars internal hist function
        hist_df = s.hist(bin_count=bins)
        counts = hist_df["count"].to_list()
        
        # Normalize for display (Bars with 8 levels)
        # Characters:  ▂▃▄▅▆▇█
        blocks = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        max_count = max(counts)
        if max_count == 0:
            return ""
            
        bar_str = ""
        for c in counts:
            idx = int((c / max_count) * 8)
            idx = min(idx, 8)
            bar_str += blocks[idx]
            
        return f"`{bar_str}`"
    except Exception as e:
        logging.warning(f"⚠️ Could not generate histogram: {e}")
        return ""

def load_dataset(filepath: str) -> pl.DataFrame:
    ext = os.path.splitext(filepath)[1].lower()
    logging.info(f"📂 Reading file: {os.path.basename(filepath)}")
    
    try:
        if ext == ".csv":
            return pl.read_csv(filepath, ignore_errors=True, try_parse_dates=True)
            
        elif ext == ".parquet":
            return pl.read_parquet(filepath)
            
        elif ext == ".json":
            return pl.read_json(filepath)
            
        elif ext in [".xlsx", ".xls"]:
            # Robust Excel Strategy
            try:
                # Attempt 1: Fast engine (fastexcel)
                return pl.read_excel(filepath)
            except Exception as e_fast:
                logging.warning(f"⚠️ 'fastexcel' failed on {os.path.basename(filepath)} ({e_fast})... Trying compatible engine.")
                try:
                    # Attempt 2: Compatible engine (xlsx2csv)
                    return pl.read_excel(filepath, engine="xlsx2csv")
                except Exception as e_csv:
                     # Attempt 3: Brute force sheet 1
                    logging.warning(f"⚠️ 'xlsx2csv' failed... Trying explicit sheet_id=1.")
                    return pl.read_excel(filepath, sheet_id=1, engine="xlsx2csv")

        else:
            logging.error(f"❌ Unsupported format: {ext}")
            return None
            
    except Exception as e:
        logging.error(f"❌ CRITICAL ERROR on {filepath}: {e}")
        return None

def analyze_and_summarize(df: pl.DataFrame, filename: str):
    analysis = []
    
    NUMERIC_TYPES = [pl.Int8, pl.Int16, pl.Int32, pl.Int64, 
                     pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64, 
                     pl.Float32, pl.Float64]
    
    logging.info(f"🔍 Analyzing {filename} ({df.height} rows, {df.width} cols)")

    for col in df.columns:
        s = df[col]
        col_info = {
            "name": col,
            "type": str(s.dtype),
            "missing": f"{s.null_count() / df.height:.1%}",
            "unique": s.n_unique(),
            "stats": "",
            "examples": str(s.drop_nulls().head(3).to_list()).replace("[", "").replace("]", "")
        }

        # Numeric Stats & Histogram
        if s.dtype in NUMERIC_TYPES:
            col_info["stats"] = f"Min:{s.min():.2f} Max:{s.max():.2f} Avg:{s.mean():.2f}"
            histo = get_ascii_histogram(s)
            if histo:
                col_info["stats"] += f" Dist:{histo}"

        analysis.append(col_info)
    
    generate_markdown(df, analysis, filename)

def generate_markdown(df: pl.DataFrame, analysis: list, original_filename: str):
    output_filename = f"SUMMARY_{original_filename}.md"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    md = [f"# 📊 Dataset Summary: {original_filename}\n"]
    md.append(f"- **Rows:** {df.height:,}")
    md.append(f"- **Columns:** {df.width}")
    md.append("\n## 🧱 Column Details\n")
    md.append("| Column | Type | Missing | Unique | Stats / Distribution | Examples |")
    md.append("|---|---|---|---|---|---|")
    
    for row in analysis:
        md.append(f"| {row['name']} | {row['type']} | {row['missing']} | {row['unique']} | {row['stats']} | {row['examples']} |")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    
    logging.info(f"✅ Summary generated: {output_path}")

def main():
    setup_logging()
    
    if not os.path.exists(INPUT_DIR):
        logging.error(f"Input directory not found: {INPUT_DIR}")
        return

    files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
    
    if not files:
        logging.warning("⚠️ No files found in data/input")
        return

    for file in files:
        if file.startswith("."): continue # Ignore hidden files
        
        file_path = os.path.join(INPUT_DIR, file)
        df = load_dataset(file_path)
        
        if df is not None:
            analyze_and_summarize(df, file)

if __name__ == "__main__":
    main()