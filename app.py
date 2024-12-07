import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient
from slack_sdk.signature import SignatureVerifier
from flask import Flask, request, jsonify
from threading import Thread

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

client = WebClient(token=SLACK_BOT_TOKEN)
verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Handles incoming Slack events
    """

    if not verifier.is_valid_request(request.get_data(), request.headers):
        return jsonify({"error": "Invalid request"}), 403
    
    data = request.json

    # Event handler
    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            thread = Thread(target=handle_mention, args=(event,))
            thread.start()
        
    return jsonify({"status": "OK"})

