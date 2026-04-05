# 🔍 Early Signal Engine
> An autonomous AI intelligence system that monitors the AI/tech landscape 24/7, ranks signals by impact, and delivers actionable briefs directly to Discord — architected and shipped solo.

🟢 **Live** — deployed on Railway, running autonomously every 3 hours

## What It Does
The engine continuously ingests structural noise from 17 disparate data sources and distills it entirely via a 4-agent Gemini evaluation pipeline. It aggressively deduplicates watchlist queries and filters macro trends while dynamically adjusting internal scoring parameters based on signal memory and cross-source trending detection. Finally, it formats localized insights, generates immediately actionable product opportunities, and delivers rich intelligence briefs continuously to Discord alongside a weekly analytical email digest.

## The 4-Agent Pipeline
- **Agent 1: Curator** — Aggressively filters noise, promotional threads, and meta-discussions, yielding the top 10 relevant materials.
- **Agent 2: Scorer/Analyst** — Benchmarks and scores articles competitively within the batch based on speed-to-implementation and immediate investment impact.
- **Agent 3: Synthesizer** — Evaluates macro trends persistently using historical signal memory to confirm momentum changes versus noise.
- **Agent 4: Idea Generator** — Ideates hyperspecific, monetizable micro-products achievable solo within 30 days based explicitly on current high-signal velocity.

## Features
- **Watchlist Alerts Grouped by Article:** Intercept tracking keywords dynamically grouped into arrays beside unified article targets.
- **Cross-Source Trending Detection:** Flags signals natively overlapping across a minimum of 3 hits and 2 distinct external sources.
- **Signal Memory Across Runs:** Caches synthesis memory locally to track macro ecosystem shifts definitively over time.
- **Brief Quality Scoring:** Persists breakdown rates across runs to algorithmically evaluate the pipeline's filtering severity.
- **Auto-Archive 30 Days:** Maintains streamlined database optimization via SQLite self-clearing queries.
- **Weekly Email Digest:** Delivers a rolling 7-day intelligence wrap-up analyzing brief quality averages via standard SMTP.
- **24/7 Deployment:** Runs efficiently, consistently, and autonomously on a 3-hour cron basis via Railway.

## Data Sources

| Source | Type | Coverage |
| :--- | :--- | :--- |
| **TechCrunch AI** | RSS | Mainstream AI advancements and venture funding |
| **MIT Tech Review AI** | RSS | Deep academic and policy analysis |
| **The Verge AI** | RSS | Consumer AI, hardware, and tech culture |
| **Ars Technica AI** | RSS | Technical breakdowns and IT sector shifts |
| **Wired AI** | RSS | Tech-ecosystem culture and high-level trends |
| **VentureBeat AI** | RSS | Enterprise AI deployments and automation |
| **Hacker News** | RSS | Ground-level builder feedback and open-source |
| **r/LocalLLaMA** | RSS | Edge models, local inference, open-weights |
| **Import AI** | RSS | High-signal newsletter from Jack Clark |
| **The Batch** | RSS | Machine learning news from Andrew Ng |
| **LessWrong** | RSS | AI alignment, rationalist theory, x-risk |
| **Bloomberg Technology** | RSS | Macro market movements and capital flow |
| **Reuters Technology** | RSS | Objective global and regulatory tech news |
| **GitHub Trending** | RSS | Repositories gaining immediate traction |
| **arXiv (cs.CL/cs.CV...)** | API | Primary research papers before publication |
| **Reddit (r/MachineLearning)** | API | Academic and peer-level ML discourse |
| **Reddit (r/technology)** | API | General public sentiment and tech news |

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core backend processing language |
| **Google Gemini Flash** | Low-latency 4-agent LLM intelligence modeling (`gemini-2.5-flash`) |
| **SQLite3** | Local persistence, deduplication, and caching |
| **APScheduler** | Async interval looping and pipeline cron management |
| **Discord Webhooks** | Interfacing frontend execution reports directly into chat |
| **smtplib / email** | Constructing and authenticating weekly SMTP data digests |
| **Railway** | Production-level 24/7 autonomous deployment environment |

## Sample Output

```text
🔥 TRENDING ACROSS SOURCES

🔥 "Anthropic" — mentioned in 6 articles across 4 sources
🔥 "agent" — mentioned in 5 articles across 2 sources

🚨 WATCHLIST ALERTS

🔑 ["acquisition", "Anthropic"] — Anthropic buys biotech startup Coefficient Bio in $400M deal
🔑 ["raises"] — Open-weights foundation startup raises $20M Series A

⚡ EARLY SIGNAL BRIEF — 2026-04-05

🏆 SIGNAL RANKINGS

🔴 [9/10] Meta drops new completely localized 8B foundational model parameter set
Category: Open-Source Models
Why it matters: Brings immediate high-accuracy reasoning to edge devices natively over WebGL. Destroys API reliance for single-developer applications.
Opportunity: Build local-only, hyper-private productivity wrappers targeting B2B verticals avoiding HIPAA compliance friction entirely.
Link: https://example.com/meta-8b

🧠 MACRO TREND
Last week indicated early hardware consolidation; this is drastically accelerating. Local-inference optimization papers are climbing to the top natively while enterprise applications emphasize local clusters over API rentals.

💡 BUILDER OPPORTUNITIES

[Local Chat PDF Scanner B2B Plugin]
What: Desktop widget parsing massive localized legal caches via edge models
Customer: Tier 3 legal aid consulting groups with tight OPSEC margins
Why they pay now: Costs scale logarithmically at rest for on-device reasoning
Money: $30/mo subscription native desktop key
MVP time: 2 weeks
Filter check: ✅ 30-day demand | ✅ Solo buildable | ✅ Signal aligned

📊 BREAKDOWN
🔴 High impact (8+): 2 🟡 Medium (5-7): 3 ⚪ Filtered out: 12
```

## Setup

1. **Clone the repository:**
   `git clone https://github.com/Raghavrana01/early-signal-engine.git`
2. **Navigate to the directory:**
   `cd early-signal-engine`
3. **Install dependencies:**
   `pip install -r requirements.txt`
4. **Configure environment variables:**
   Create a `.env` file referencing your keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   DISCORD_WEBHOOK_URL=your_discord_webhook_url
   EMAIL_FROM=your_dispatch_email
   EMAIL_TO=your_target_email
   EMAIL_PASSWORD=your_smtp_app_password
   ```
5. **Start the Engine:**
   `python main.py`

## Architecture
The system is built inherently around low-drag execution over heavy complexity. SQLite handles immediate deduplication via unique constraint drops internally without the bulk of a standalone PostgreSQL instance. `gemini-2.5-flash` natively fulfills the cost, latency, and reasoning context requirements enabling rapid chained executions inside a 4-agent structure. RSS APIs are extensively chosen to pull real-time, deterministic structured data quickly rather than fragile web-scraping DOMs. Everything is orchestrated over a strict continuous `APScheduler` loop, deploying natively to a lightweight Railway container designed to fail safely and iterate reliably completely unattended.

## Built By
Raghav Rana — AI Engineer building systems that create real information edge for investors and builders.
