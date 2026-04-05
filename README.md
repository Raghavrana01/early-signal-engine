# Early Signal Engine

An AI news aggregator designed to silently fetch and store the latest AI developments, then ping you via Discord.

## What It Does
The engine acts as an automated pipeline that periodically scans various data sources for new AI-related articles, research papers, and forum discussions. It stores these in a local SQLite database, intelligently ignores duplicate entries, and broadcasts newly discovered signals into a Discord channel for your review.

## Tech Stack
- **Python 3** (Core Logic)
- **SQLite** (Persistent, lightweight storage)
- **APScheduler** (Background scheduled execution)
- **feedparser / requests** (Ingestion and API delivery)
- **python-dotenv** (Environment variable management)

## Data Sources
- **RSS Publications:** TechCrunch AI, MIT Tech Review AI, The Verge AI, Ars Technica AI
- **arXiv API:** Latest top papers in `cs.AI` and `cs.LG`
- **Reddit RSS Feeds:** Top posts from `r/artificial`, `r/MachineLearning`, and `r/singularity`

## Local Setup
1. **Clone Repo** 
   ```bash
   git clone https://github.com/Raghavrana01/early-signal-engine.git
   cd early-signal-engine
   ```
2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add Discord Webhook**
   Create a `.env` file in the project root encoded in `UTF-8` and add your webhook URL:
   ```env
   DISCORD_WEBHOOK_URL=your_webhook_url_here
   ```
4. **Run the Engine**
   ```bash
   python main.py
   ```
   *The script will immediately fire a test message to verify the webhook, fetch all data, and then lock your terminal in a suspended state that triggers the pipeline every 3 hours. Stop it with `Ctrl+C`.*
