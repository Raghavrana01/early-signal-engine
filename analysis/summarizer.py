import os
import json
from datetime import datetime
from google import genai

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found in environment")
    return genai.Client(api_key=api_key)

def clean_json(text):
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    return text.strip()

def curate_articles(articles):
    if not articles:
        return []
    prompt = f"""
    You are an AI curation assistant.
    Review the following {len(articles)} articles and filter them down to the top 10 most relevant to AI builders and investors. 
    Remove noise like job posts, self-promotion threads, and meta-discussions.
    Return ONLY a JSON list of the selected articles. Each object MUST exactly maintain 'title', 'link', and 'source' from the original.
    Do not return any other text outside the JSON array.
    
    Articles:
    {json.dumps(articles, indent=2)}
    """
    client = get_client()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    try:
        return json.loads(clean_json(response.text))
    except Exception as e:
        print(f"Error parsing curated JSON: {e}\nRaw: {response.text}")
        return []

def score_and_analyze(curated_articles):
    if not curated_articles:
        return []
    prompt = f"""
    You are an AI scoring agent and analyst. 
    For each of the following articles, assign a score from 1-10 based on:
    - Direct impact on builders (new tools/APIs/models)
    - Direct impact on investors (funding/acquisitions/valuations)
    - Speed of opportunity (how fast is this actionable)
    Also write one 2-sentence "why it matters" and one "opportunity" line.
    Return ONLY a JSON list of the articles. Each object MUST have:
    'title', 'link', 'source', 'score' (number 1-10), 'category', 'why', 'opportunity'.
    Do not return any other text outside the JSON array.
    
    Articles:
    {json.dumps(curated_articles, indent=2)}
    """
    client = get_client()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    try:
        return json.loads(clean_json(response.text))
    except Exception as e:
        print(f"Error parsing scored JSON: {e}\nRaw: {response.text}")
        return []

def synthesize_trend(scored_articles):
    if not scored_articles:
        return "No notable macro trend detected this period due to insufficient data."
    prompt = f"""
    You are a macro-analyst. Read the following AI-related articles and write a 2-3 sentence macro trend paragraph explaining what all of this points to this week.
    Return only the paragraph text smoothly readable. Do NOT use markdown.
    
    Articles:
    {json.dumps(scored_articles, indent=2)}
    """
    client = get_client()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text.strip()

def format_discord_brief(scored_articles, macro_trend, initial_count):
    high_count = sum(1 for a in scored_articles if a.get('score', 0) >= 8)
    med_count = sum(1 for a in scored_articles if 5 <= a.get('score', 0) < 8)
    filtered_count = initial_count - len(scored_articles)

    today = datetime.now().strftime("%Y-%m-%d")
    
    brief = f"⚡ EARLY SIGNAL BRIEF — {today}\n\n🏆 SIGNAL RANKINGS\n\n"
    
    for article in scored_articles:
        score = article.get('score', 0)
        indicator = "🔴" if score >= 8 else ("🟡" if score >= 5 else "⚪")
        
        brief += f"{indicator} [{score}/10] {article.get('title', 'Unknown')}\n"
        brief += f"Category: {article.get('category', 'General')}\n"
        brief += f"Why it matters: {article.get('why', '')}\n"
        brief += f"Opportunity: {article.get('opportunity', '')}\n"
        brief += f"Link: {article.get('link', '')}\n\n"
        
    brief += f"🧠 MACRO TREND\n{macro_trend}\n\n"
    brief += f"📊 BREAKDOWN\n🔴 High impact (8+): {high_count} 🟡 Medium (5-7): {med_count} ⚪ Filtered out: {filtered_count}"
    
    return brief

def run_summarizer(articles):
    print("Agent 1: Curating articles...")
    curated = curate_articles(articles)
    
    if not curated:
        return None
        
    print("Agent 2: Scoring and analyzing...")
    scored = score_and_analyze(curated)
    
    if not scored:
        return None
        
    print("Agent 3: Synthesizing macro trend...")
    trend = synthesize_trend(scored)
    
    print("Formatting brief...")
    brief = format_discord_brief(scored, trend, len(articles))
    return brief
