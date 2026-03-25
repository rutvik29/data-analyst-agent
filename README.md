# 📊 Data Analyst Agent

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-FF6B35?style=flat)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Ask questions about your data in plain English.** The agent writes SQL, executes it, analyzes results with pandas, generates charts, and explains insights — all in one shot.

## ✨ Highlights

- 🗣️ **Natural language → SQL** — powered by GPT-4o with schema-aware prompting
- 🔁 **Self-correcting loop** — if SQL fails, the agent reads the error and tries again
- 📈 **Auto visualization** — generates Plotly charts based on query results
- 🧮 **Pandas analysis** — describes statistics, detects trends, flags anomalies
- 🔌 **Multi-DB support** — PostgreSQL, MySQL, SQLite, BigQuery, Snowflake
- 💬 **Streamlit chat UI** — interactive multi-turn conversation with your data

## Demo

```
User: "Which product category had the highest revenue last quarter, broken down by month?"

Agent: [analyzes schema] → [writes SQL] → [executes] → [plots bar chart] →
       "Electronics led Q4 with $2.4M total revenue. December was the peak month (+31% MoM)
        driven by holiday promotions. Laptops alone accounted for 67% of category revenue."
```

## Quick Start

```bash
git clone https://github.com/rutvik29/data-analyst-agent
cd data-analyst-agent
pip install -r requirements.txt
cp .env.example .env  # add OPENAI_API_KEY + DATABASE_URL

streamlit run ui/app.py
```

## Architecture

```
User Question
      │
      ▼
┌───────────────┐   schema    ┌───────────────┐
│ Schema Loader │ ──────────▶ │  SQL Writer   │
└───────────────┘             └───────┬───────┘
                                      │ SQL
                                      ▼
                              ┌───────────────┐
                    error ◀── │   Executor    │ ──▶ DataFrame
                    (retry)   └───────────────┘
                                      │
                              ┌───────▼───────┐
                              │   Analyzer    │ ──▶ Stats + Insights
                              └───────┬───────┘
                                      │
                              ┌───────▼───────┐
                              │  Visualizer   │ ──▶ Plotly Chart
                              └───────────────┘
```

## License

MIT © Rutvik Trivedi
