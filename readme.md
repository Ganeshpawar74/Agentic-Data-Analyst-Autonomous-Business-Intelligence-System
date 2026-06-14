# Agentic Data Analyst: Autonomous Business Intelligence System

A multi-agent AI platform that converts natural-language business questions into SQL queries, anomaly-detection alerts, time-series forecasts, and executive-ready reports — built end-to-end with a focus on **governed, reproducible analytics pipelines** and **minimal to no human intervention** across recurring analytical workflows.

This project mirrors how enterprise BI automation works in practice: ingest data, validate and transform it under governance controls, run multi-layer analysis, and surface findings to non-technical stakeholders through automated dashboards and reports — with no manual data review required.

---

## Why This Project

Most analytics workflows still rely on manual data review, ad-hoc queries, and one-off reporting — creating bottlenecks every time a stakeholder needs an answer. This system eliminates that entirely.

Every query passes through **multi-layer validation, audit logging, and reconciliation checks** before results are surfaced — so outputs are consistent, governance-ready, and trustworthy even as underlying data changes. The goal was to build the kind of **operational automation platform** that replaces recurring manual effort with a single, reliable, self-running analytics stack.

---

## Key Highlights

- **Minimal to no human intervention** — natural language → SQL/Pandas → analysis → visualization → report, fully orchestrated by a Planner Agent with no manual steps required across recurring workflows
- **Operational automation at scale** — handles recurring business questions automatically, surfacing trends, risks, and opportunities without waiting for analyst availability
- **Data governance built in** — validation, audit trail logging, and reconciliation checks run at every pipeline stage to ensure reproducible, audit-ready outputs
- **Anomaly detection and proactive alerting** — IsolationForest, Z-score, and IQR-based detection flags risks and outliers before they escalate, enabling proactive rather than reactive decision-making
- **Stakeholder-ready outputs** — every analysis exported as polished PDF/HTML reports or live Streamlit dashboards, built for non-technical business stakeholders
- **Modular, production-grade architecture** — ingestion, transformation, analysis, and reporting are cleanly separated layers; each independently extensible without breaking the rest of the system

---

## Architecture Overview

```
User Query (Natural Language)
    │
    ▼
Planner Agent  ──  decomposes question into sub-tasks, routes to specialists
    │
    ├──► Data Analysis Agent      (Pandas + NumPy + DuckDB)
    ├──► Query Generation Agent   (SQL + Pandas codegen via Mistral AI)
    ├──► Anomaly Detection Agent  (IsolationForest + Z-score + IQR)
    ├──► Forecasting Agent        (Prophet + ARIMA)
    ├──► Visualization Agent      (Plotly)
    ├──► Insight Agent            (business narrative generation)
    ├──► Recommendation Agent     (actionable next steps)
    └──► Report Generation Agent  (PDF + HTML + Markdown)
         │
         ▼
    Governance Layer  (audit logging, reconciliation checks, validation)
    RAG Pipeline      (HuggingFace Embeddings + ChromaDB)
    Memory            (Redis + LangGraph)
    Dashboard         (Streamlit)
```

The **Planner Agent** decomposes a business question into sub-tasks and routes them to specialized agents — each with a single responsibility. Every result passes through the **Governance Layer** before reaching stakeholders, ensuring outputs are consistent, reproducible, and audit-ready.

---

## What This Automates

| Manual Process | What the System Does Instead |
|---|---|
| Analyst writes SQL for each question | Query Generation Agent produces SQL/Pandas automatically |
| Manual data validation before reporting | Reconciliation checks + audit logging run at every pipeline stage |
| Analyst builds charts after analysis | Visualization Agent selects and renders the right chart type |
| Weekly reports assembled by hand | Report Agent compiles findings into PDF/HTML automatically |
| Anomaly investigation triggered by complaints | Anomaly Detection Agent proactively flags risks before escalation |
| Forecasting done ad hoc in Excel | Forecasting Agent runs Prophet/ARIMA on schedule |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Mistral AI (mistral-large-latest) |
| **Embeddings** | HuggingFace (sentence-transformers/all-MiniLM-L6-v2) |
| **Agent Framework** | LangGraph + LangChain |
| **Vector DB** | ChromaDB |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **Data Processing** | Pandas, NumPy, DuckDB, SciPy |
| **Visualization** | Plotly |
| **Database** | PostgreSQL (metadata) |
| **Caching / Memory** | Redis |
| **Anomaly Detection** | Scikit-learn (IsolationForest), Z-score, IQR |
| **Forecasting** | Prophet, statsmodels (ARIMA) |
| **Containerization** | Docker + Docker Compose |
| **Monitoring** | LangSmith |

---

## Agents

| Agent | Method | Responsibility |
|-------|--------|----------------|
| Planner | Mistral Large | Decomposes business questions into executable sub-tasks |
| Data Analysis | Code execution | Statistical analysis, EDA, KPI computation |
| Query Generation | Mistral Large | Generates SQL/Pandas code from natural language |
| Anomaly Detection | IsolationForest + Z-score + IQR | Flags outliers, risks, and data quality issues |
| Forecasting | Prophet + ARIMA | Time-series demand and trend forecasting |
| Visualization | Rule-based + Mistral | Selects and builds the right chart type |
| Insight | Mistral Large | Translates results into business narrative |
| Recommendation | Mistral Large | Produces actionable next steps for stakeholders |
| Report | Mistral Large | Compiles all findings into client-ready PDF/HTML reports |

---

## Project Structure

```
Agentic_Bi/
├── agents/          # LangGraph agent definitions (planner, analysis, query, anomaly, forecast, report)
├── analytics/       # Core analytics logic (data_processor, anomaly_detector, forecasting, statistical_analysis)
├── backend/         # FastAPI service (routes, models, config, security)
├── frontend/        # Streamlit dashboard (pages, components, styles)
├── rag/             # RAG pipeline (loader, chunker, embedder, retriever)
├── memory/          # Redis-backed conversation memory
├── reports/         # PDF/HTML/Markdown report builders
├── vectorstore/     # ChromaDB integration
├── database/        # Schema, session management
├── deployment/      # Docker Compose, Dockerfiles, nginx
├── tests/           # Agent, analytics, and RAG test suites
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### 1. Clone & Configure

```bash
git clone https://github.com/Ganeshpawar74/Agentic-Data-Analyst-Autonomous-Business-Intelligence-System
cd agentic-data-analyst
cp .env.example .env
# Add your API keys to .env
```

### 2. API Keys Required

```env
MISTRAL_API_KEY=your_mistral_key
HUGGINGFACE_API_TOKEN=your_hf_token    # optional, for private models
LANGSMITH_API_KEY=your_langsmith_key   # optional, for tracing
```

### 3. Run with Docker

```bash
docker-compose up --build
```

### 4. Run Locally

```bash
pip install -r requirements.txt

# Terminal 1 — Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && streamlit run app.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload datasets (CSV / Excel / JSON) |
| POST | `/analyze` | Run full agent analysis pipeline |
| POST | `/query` | Natural language → SQL query |
| POST | `/chat` | Conversational analytics interface |
| POST | `/generate-report` | Generate PDF/HTML executive report |
| POST | `/forecast` | Time-series forecasting (Prophet / ARIMA) |
| POST | `/rag-upload` | Upload knowledge base documents |
| GET | `/dashboard` | Live dashboard data |

---

## Testing

```bash
python tests/test_agents.py
python tests/test_analytics.py
python tests/test_rag.py
```

---

## Key Design Decisions

**Why multi-agent over a single LLM call?**
Single-call approaches collapse under complex queries — the model tries to analyze, query, visualize, and narrate simultaneously, producing inconsistent outputs. Separating responsibilities into specialized agents with a Planner routing between them produces more reliable, auditable, and extensible results.

**Why governance at every stage?**
In real enterprise BI, a single bad data point in a stakeholder report erodes trust in the entire system. Validation and reconciliation checks at each pipeline stage — not just at ingestion — ensures that any data quality issue is caught and flagged before it reaches an executive dashboard or PDF report.

**Why Prophet + ARIMA together?**
Prophet handles seasonality and trend decomposition well but struggles with short, irregular series. ARIMA complements it on structured time series with clear autocorrelation. Running both and surfacing the better-fit model gives more robust forecasting across diverse business datasets.

---

## What I'd Build Next

- **Role-based access control** for multi-user and client-specific deployments
- **Configurable governance rules** per dataset — currently validation logic is hardcoded; making it declarative would generalize the system across industries
- **Query caching layer** for repeated questions to reduce LLM API costs on high-volume deployments
- **Scheduled pipeline runs** — trigger the full agent pipeline on a cron schedule so dashboards refresh automatically without any user prompt
