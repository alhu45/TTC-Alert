from flask import Response, Flask, request
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)
load_dotenv()

# MongoDB setup
mongo_uri = os.getenv("MONGODB")
client = MongoClient(mongo_uri)
db = client["ttc"]
alerts_collection = db["alerts"]

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()

    if "alert" in incoming_msg:
        all_alerts = alerts_collection.find().sort("timestamp", -1)
        message_header = "TTC ALERTS:\n\n"
        total_message = message_header

        for alert in all_alerts:
            description = alert.get("description", "No description")[:200]
            alert_text = f"{description}\n\n"

            # Reserve space for Twilio trial prefix (~60 chars buffer)
            if len(total_message) + len(alert_text) > 1450:
                total_message += "[Truncated to fit SMS limit]"
                break

            total_message += alert_text

        if total_message == message_header:
            total_message += "No recent TTC alerts found."
    else:
        total_message = "Send 'alert' to receive all current TTC alerts."

    resp.message(total_message)
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
