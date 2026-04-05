import os
import json
from datetime import datetime
from storage.db import get_last_macro_trend
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
        model='gemini-2.5-pro-exp-03-25',
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
    Score articles relative to each other, not on an absolute scale. The best article in this batch should score 9-10, the worst relevant one should score 4-5. Avoid clustering all scores in the 7-8 range. Force meaningful differentiation between scores.
    
    Articles:
    {json.dumps(curated_articles, indent=2)}
    """
    client = get_client()
    response = client.models.generate_content(
        model='gemini-2.5-pro-exp-03-25',
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
        
    last_trend = get_last_macro_trend()
    trend_context = f"\n    Last week's macro trend was: {last_trend}. Either confirm this trend is continuing with new evidence, or identify what has changed.\n" if last_trend else ""
    
    prompt = f"""
    You are a macro-analyst. Read the following AI-related articles and write a 2-3 sentence macro trend paragraph explaining what all of this points to this week.{trend_context}
    Return only the paragraph text smoothly readable. Do NOT use markdown.
    
    Articles:
    {json.dumps(scored_articles, indent=2)}
    """
    client = get_client()
    response = client.models.generate_content(
        model='gemini-2.5-pro-exp-03-25',
        contents=prompt
    )
    return response.text.strip()

def generate_ideas(top_articles):
    if not top_articles:
        return ""
    prompt = f"""
    You are a product idea generator for a solo builder with no team, no funding, and no interest in marketing or content creation. You build faceless, monetizable products.
    Given these high-signal AI/tech articles, generate 2-3 product ideas. Each idea MUST pass all 3 of these filters before being included:

    Someone will pay for this within 30 days of launch — there is clear, immediate demand
    A solo developer can build the MVP in under 4 weeks using AI tools
    The idea is directly aligned with a current market movement visible in the signals

    If an idea fails any filter, discard it and find a better one.
    For each idea that passes all 3 filters, output:
    [Product Name]
    What: [one line, specific and concrete — not vague]
    Customer: [exact person who pays, not "businesses" or "developers"]
    Why they pay now: [what makes this urgent in the next 30 days]
    Money: [specific monetization — price point, model]
    MVP time: [honest estimate in weeks]
    Filter check: ✅ 30-day demand | ✅ Solo buildable | ✅ Signal aligned
    Be brutally honest. It is better to output 1 strong idea than 3 weak ones.
    
    Articles:
    {json.dumps(top_articles, indent=2)}
    """
    client = get_client()
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro-exp-03-25',
            contents=prompt
        )
        
        out_text = response.text.strip()
        if not out_text:
            return ""
            
        return f"💡 BUILDER OPPORTUNITIES\n\n{out_text}"
    except Exception as e:
        print(f"Error generating ideas: {e}")
        return ""

def format_discord_brief(scored_articles, macro_trend, initial_count, ideas_text=""):
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
    
    if ideas_text:
        brief += f"{ideas_text}\n\n"
        
    brief += f"📊 BREAKDOWN\n🔴 High impact (8+): {high_count} 🟡 Medium (5-7): {med_count} ⚪ Filtered out: {filtered_count}"
    
    return brief

def run_summarizer(articles):
    print("Agent 1: Curating articles...")
    curated = curate_articles(articles)
    
    if not curated:
        return None, None
        
    print("Agent 2: Scoring and analyzing...")
    scored = score_and_analyze(curated)
    
    if not scored:
        return None, None
        
    print("Agent 3: Synthesizing macro trend...")
    trend = synthesize_trend(scored)
    
    print("Agent 4: Generating product ideas...")
    top_scored = [a for a in scored if a.get('score', 0) >= 8]
    ideas_text = generate_ideas(top_scored)
    
    print("Formatting brief...")
    brief = format_discord_brief(scored, trend, len(articles), ideas_text)
    return brief, trend
