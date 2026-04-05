# 🔍 Early Signal Engine
> An autonomous AI intelligence system that monitors the AI/tech landscape 24/7, ranks signals by impact, and delivers actionable briefs directly to Discord — architected and shipped solo.
🟢 **Live** — deployed on Railway, running autonomously every 3 hours

## What It Does
The Early Signal Engine is an autonomous intelligence pipeline. It continuously ingests raw data from 10 distinct industry sources, filters out noise, and processes the remaining data through a 4-agent Google Gemini pipeline. Every three hours, it delivers a deeply analyzed, ranked intelligence brief directly to a Discord webhook, complete with synthesized macro trends and extracted product opportunities.

## The 4-Agent Pipeline
1. **Curator:** Aggressively filters raw arrays to drop noise, low-signal threads, and self-promotion.
2. **Scorer/Analyst:** Ranks true signals out of 10 based on immediate builder impact, investor implications, and speed of actionability.
3. **Synthesizer:** Analyzes the highly-scored shortlist to compute the weekly macro trend.
4. **Idea Generator:** Maps the hottest signals (`8+` score) against strict filters to extract directly monetizable, solo-buildable software product opportunities.

## Data Sources

| Source | Type | Coverage |
| --- | --- | --- |
| TechCrunch & The Verge | RSS | Mainstream AI breaking news and product launches |
| MIT Tech Review | RSS | Deep-dive technological analysis and breakthroughs |
| Ars Technica | RSS | High-fidelity technical reporting |
| Wired & VentureBeat | RSS | Enterprise ecosystem shifts and venture capital moves |
| arXiv | API | Direct academic paper ingest tracking `cs.AI` and `cs.LG` |
| Reddit | RSS | Grassroots sentiment parsing across `/r/MachineLearning`, `/r/artificial`, and `/r/singularity` |

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python 3.11 | Core logic runtime and orchestration |
| Google Gemini 2.5 Flash | High-speed, context-heavy LLM reasoning pipeline (via `google-genai` SDK) |
| SQLite | Persistent, lightweight deduplication storage |
| APScheduler | Background cron job execution |
| Discord Webhooks | Asynchronous notification delivery |

## Sample Output

```text
⚡ EARLY SIGNAL BRIEF — 2026-04-05

🏆 SIGNAL RANKINGS

🔴 [9/10] Meta open-sources Llama 4 for developers
Category: Core Infrastructure
Why it matters: Open-source models matching frontier capabilities forces compute optimization down market.
Opportunity: Build high-margin fine-tuning workflows for enterprise data over standard Llama 4 weights.
Link: https://example.com/llama4

🧠 MACRO TREND
Capital is rotating heavily away from foundational training layers and entirely into application-layer vertical software capable of autonomous agentic operation, driven by tumbling inference costs.

💡 BUILDER OPPORTUNITIES

1. RAG-as-a-Service for Independent Auditors
What: Plug-and-play local LLM inference ingestion for legacy financial PDF standards
Customer: Boutique accounting firms running small compute footprints
Why they pay now: Legacy OCR tools are slow; Llama 4 handles 100k tokens locally at zero marginal cost.
Money: $499/mo per firm
MVP time: 2 weeks
Filter check: ✅ 30-day demand | ✅ Solo buildable | ✅ Signal aligned

📊 BREAKDOWN
🔴 High impact (8+): 1 🟡 Medium (5-7): 3 ⚪ Filtered out: 16
```

## Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Raghavrana01/early-signal-engine.git
   cd early-signal-engine
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   DISCORD_WEBHOOK_URL=your_discord_webhook_url
   ```
4. **Run the engine**
   ```bash
   python main.py
   ```

## Architecture
The system pairs persistent local storage with background cron orchestration to achieve zero-maintenance uptime. SQLite was chosen over heavy relational databases for isolated, robust state management that seamlessly deduplicates URLs across successive runs. Utilizing RSS for web feeds entirely eliminates scraping fragility and authentication limits compared to traditional HTML parsing or bloated official APIs. Gemini 2.5 Flash operates natively due to its massive context window and lightning-fast sequential inference, keeping latency negligible when chaining the 4-agent prompts. APScheduler acts as a background native daemon, allowing the engine to run quietly as a worker without complex message queues or load balancers.

## Built By
Raghav Rana — AI Engineer building systems that create real information edge for investors and builders  
GitHub: [github.com/Raghavrana01](https://github.com/Raghavrana01)
