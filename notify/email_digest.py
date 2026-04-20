import os
import smtplib
from email.message import EmailMessage
from storage.db import get_avg_scores, get_recent_macro_trends

def send_weekly_digest():
    email_from = os.environ.get("EMAIL_FROM")
    email_to = os.environ.get("EMAIL_TO")
    email_password = os.environ.get("EMAIL_PASSWORD")
    
    if not email_from or not email_to or not email_password:
        print("Email credentials not configured, skipping digest")
        return
        
    print("Gathering data for weekly digest...")
    avg_scores = get_avg_scores()
    recent_trends = get_recent_macro_trends(days=7)
    
    if not recent_trends:
        trends_html = "<li>No macro trends recorded this week.</li>"
        trends_text = "- No macro trends recorded this week.\n"
    else:
        trends_html = "".join([f"<li>{item['trend']}</li>" for item in recent_trends])
        trends_text = "".join([f"- {item['trend']}\n" for item in recent_trends])
        
    subject = "Early Signal Engine - Weekly Digest"
    
    html_content = f"""
    <html>
      <head></head>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 10px;">Early Signal Engine Weekly Digest</h2>
        
        <h3>📊 Weekly Pipeline Averages</h3>
        <ul>
          <li><b>🔴 High Impact Signals (8+):</b> {avg_scores['high']} / run</li>
          <li><b>🟡 Medium Impact Signals (5-7):</b> {avg_scores['medium']} / run</li>
          <li><b>⚪ Noise (Filtered Out):</b> {avg_scores['filtered']} / run</li>
        </ul>
        
        <h3>🧠 Macro Trend Evolution (Last 7 Days)</h3>
        <ul>
            {trends_html}
        </ul>
        <br>
        <p style="color: #888;"><small>Automated dispatch from Early Signal Engine.</small></p>
      </body>
    </html>
    """
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to
    
    # Fallback plain text
    msg.set_content(f"Early Signal Engine Weekly Digest\n\nPipeline Averages (per run):\n- High Impact: {avg_scores['high']}\n- Medium Impact: {avg_scores['medium']}\n- Filtered: {avg_scores['filtered']}\n\nMacro Trend Evolution:\n{trends_text}")
    
    # HTML version
    msg.add_alternative(html_content, subtype='html')

    try:
        print(f"Sending digest email to {email_to} via smtp.gmail.com...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to, msg.as_string())
        print("Weekly digest email sent successfully.")
    except Exception as e:
        print(f"Failed to send weekly digest email: {e}")

