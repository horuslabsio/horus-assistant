import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient
from slack_sdk.signature import SignatureVerifier
from flask import Flask, request, jsonify
from threading import Thread

from agent.main import query_agent

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

    # Handle Slack URL verification
    if "challenge" in data:
        return jsonify(
            {"challenge": data["3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"]}
        )

    # Event handler
    if "event" in data:
        event = data["event"]
        if event.get("type") == "app_mention":
            print("Agent was mentioned!")
            thread = Thread(target=handle_mention, args=(event,))
            thread.start()

    return jsonify({"status": "OK"})


def handle_mention(event):
    """
    Handles app_mention events
    """
    user = event["user"]
    channel = event["channel"]
    text = event.get("text", "")

    mention_text = text.split(maxsplit=1)[1] if len(text.split()) > 1 else ""

    # query the agent
    try:
        response = query_agent(mention_text)
        send_message(channel, response, thread_ts=event.get("ts"))
    except Exception as e:
        print(f"Error processing query: {e}")
        send_message(
            channel,
            "Sorry, I encountered an error processing your request.",
            thread_ts=event.get("ts"),
        )


def send_message(channel, text, thread_ts=None):
    """
    Sends a message to a Slack channel
    """
    try:
        client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)
    except SlackApiError as e:
        print(f"Error sendig message: {e.response['error']}")


if __name__ == "__main__":
    app.run(port=8000)
