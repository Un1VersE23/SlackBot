import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.slack import make_slack_blueprint, slack

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["SLACK_OAUTH_CLIENT_ID"] = os.environ.get("SLACK_OAUTH_CLIENT_ID")
app.config["SLACK_OAUTH_CLIENT_SECRET"] = os.environ.get("SLACK_OAUTH_CLIENT_SECRET")
slack_bp = make_slack_blueprint(scope=["identify", "chat:write:bot"])
app.register_blueprint(slack_bp, url_prefix="/login")

@app.route("/")
def index():
    if not slack.authorized:
        return redirect(url_for("slack.login"))
    resp = slack.post("chat.postMessage", data={
        "channel": "#general",
        "text": "ping",
        "icon_emoji": ":robot_face:",
    })
    assert resp.ok, resp.text
    return resp.text
