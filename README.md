# Early Signal Engine

An automated, multi-source AI news aggregator powered by a 4-agent Gemini pipeline that drops highly curated, actionable intelligence straight into your Discord.

## What It Does
The engine acts as a background pipeline that periodically scans 10 leading technology sources for the latest AI-related developments. It stores them persistently in a SQLite database, intelligently ignores duplicate entries, pipes the latest results through a robust Google Gemini AI analysis layer, and broadcasts a filtered, scored, and synthesized brief directly into your Discord channel.

## Data Sources
The engine natively digests signals from:
- **RSS Publications:** TechCrunch, MIT Tech Review, The Verge, Ars Technica, Wired, VentureBeat
- **arXiv API:** Latest top papers tracking `cs.AI` and `cs.LG`
- **Reddit RSS Feeds:** Top daily posts from `r/artificial`, `r/MachineLearning`, and `r/singularity`

## The 4-Agent Pipeline
When the engine runs, the newest 20 signals are passed through this fully autonomous LLM orchestration:
1. 🕵️ **Agent 1 (Curator):** Aggressively filters the raw array to drop noise (job posts, meta-threads, self-promotion) and isolates the true signals.
2. ⚖️ **Agent 2 (Scorer/Analyst):** Computes an out-of-10 actionability score evaluating Builder Impact, Investor Impact, and Speed of Actionability. Extracts "Why it Matters" and "Opportunity".
3. 🧠 **Agent 3 (Synthesizer):** Analyzes the highly-scored shortlist and computes the weekly macro trend.
4. 💡 **Agent 4 (Idea Generator):** Slices off the hottest signals (score `8+`) and generates 2-3 concrete, realistic SaaS/product ideas for solo builders complete with monetization strategies and MVP timelines.

## Tech Stack
- **Python 3.11** (Core Logic)
- **Google Gemini 2.5 Flash** (via `google-genai` SDK for blazing fast logical reasoning)
- **SQLite** (Persistent, lightweight deduplication storage)
- **APScheduler** (Background chron orchestration)
- **Discord Webhooks** (Asynchronous delivery routing)

## Setup instructions
1. **Clone Repo** 
   ```bash
   git clone https://github.com/Raghavrana01/early-signal-engine.git
   cd early-signal-engine
   ```
2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**
   Create a `.env` file in the project root encoded in `UTF-8` and add your keys:
   ```env
   DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
4. **Run the Engine**
   ```bash
   python main.py
   ```
   *The script will immediately fire a test message to verify the webhook, fetch data, run the AI summarizer, and then lock your terminal in a suspended state that triggers the pipeline every 3 hours. Stop it with `Ctrl+C`.*

## Output Format
The final payload sent to your Discord channel is cleanly formatted exactly like this:
- **🏆 SIGNAL RANKINGS:** Color-coded (🔴 `8+`, 🟡 `5-7`, ⚪ `<5`) itemized lists of all analyzed news with the score, category, why it matters, and direct link.
- **🧠 MACRO TREND:** A dense paragraph tracking where the market is moving based on this batch's news.
- **💡 BUILDER OPPORTUNITIES:** Extracted startup ideas mapping out the What, Customer, Monetization, and execution timeline.
- **📊 BREAKDOWN:** A footer calculating exactly how many signals hit high, medium, and how many items were forcibly filtered out by the Curator.
