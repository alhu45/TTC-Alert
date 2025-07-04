# The purpose of this code is creating a backend server to allow twilio to fetch data from MongoDB everytime the word "alert" is sent to the number 

from flask import Response
from flask import Flask, request
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

# 1. Initialize Flask app
app = Flask(__name__)
load_dotenv()

# 2. MongoDB connectivity setup
mongo_uri = os.getenv("MONGODB")
client = MongoClient(mongo_uri)
db = client["ttc"]
alerts_collection = db["alerts"]

# 3. Creating a POST request to the http route /sms (Start with ngrok http 4000 in terminal so local server backend runs on the internet so Twilio can access it)
@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "").strip().lower() # Fetching last alert message
    resp = MessagingResponse() # Creating XML Based Response so Twilio will understand

    # Logic for when the user texts "alert" to the number
    if "alert" in incoming_msg:
        latest_alert = alerts_collection.find_one(sort=[("timestamp", -1)])
        if latest_alert:
            description = latest_alert.get("description", "No description")
            message = f"TTC ALERT:\n{description}"
        else:
            message = "No recent TTC alerts found."
    else:
        message = "Send 'alert' to receive the latest TTC alert."

    # Sending the reply to Twilio so it can send the text to the messenger 
    resp.message(message)
    return Response(str(resp), mimetype="application/xml")

# 4. Running the backend
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)



