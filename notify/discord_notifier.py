import requests

def send_digest(webhook_url, articles):
    if not articles:
        print("No new articles to send to Discord.")
        return
        
    if not webhook_url:
        print("Webhook URL not provided. Skipping Discord notification.")
        return

    # Group articles by source
    grouped = {}
    for article in articles:
        source = article.get('source', 'Unknown')
        if source not in grouped:
            grouped[source] = []
        grouped[source].append(article)

    # Build the messages, keeping them under the 2000 character limit
    messages = []
    current_message = ""

    for source, source_articles in grouped.items():
        chunk = f"**{source}**\n"
        for article in source_articles:
            title = article.get('title', 'No Title')
            link = article.get('link', '#')
            bullet = f"- {title}\n  {link}\n"
            chunk += bullet
        
        chunk += "\n"

        # Check if adding this chunk exceeds 2000 chars limit (leave some buffer)
        if len(current_message) + len(chunk) > 1900:
            if current_message:
                messages.append(current_message)
            # If a single chunk is somehow > 1900, we should technically split it further, 
            # but for our purposes we'll append it carefully.
            while len(chunk) > 1900:
                messages.append(chunk[:1900])
                chunk = chunk[1900:]
            current_message = chunk
        else:
            current_message += chunk

    if current_message.strip():
        messages.append(current_message.strip())

    # Send each message to the webhook
    count_sent = 0
    for i, msg in enumerate(messages):
        payload = {"content": msg}
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            count_sent += 1
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to Discord (Part {i+1}/{len(messages)}): {e}")
            
    print(f"Sent {count_sent} notification messages to Discord.")

def send_test_message(webhook_url):
    if not webhook_url:
        print("Webhook URL not provided. Skipping Discord test message.")
        return
        
    payload = {"content": "✅ Early Signal Engine connected successfully!"}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("Sent test message to Discord.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send test message to Discord: {e}")
