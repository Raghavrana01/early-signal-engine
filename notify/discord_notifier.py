import requests

def send_brief(webhook_url, brief_text):
    if not webhook_url:
        print("Webhook URL not provided. Skipping Discord brief.")
        return

    # Check if brief is larger than 2000 chars. If so, split by newlines roughly.
    messages = []
    chunk = ""
    for line in brief_text.split('\n'):
        if len(chunk) + len(line) + 1 > 1900:
            messages.append(chunk.strip())
            chunk = line + "\n"
        else:
            chunk += line + "\n"
            
    if chunk.strip():
        messages.append(chunk.strip())

    count_sent = 0
    for i, msg in enumerate(messages):
        payload = {"content": msg}
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            count_sent += 1
        except requests.exceptions.RequestException as e:
            print(f"Failed to send brief to Discord (Part {i+1}/{len(messages)}): {e}")

    print(f"Sent {count_sent} brief chunks to Discord.")

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
