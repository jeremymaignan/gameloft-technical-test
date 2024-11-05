import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from controllers.campaign import campaign_bp
from controllers.player import player_bp
from services.dynamodb import DynamoDB

app = Flask(__name__)
CORS(app)

load_dotenv()

app.dynamodb = DynamoDB(
    url=os.getenv("DYNAMO_ENDPOINT"),
    region=os.getenv("AWS_REGION")
)

# Register the blueprint
app.register_blueprint(player_bp)
app.register_blueprint(campaign_bp)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
