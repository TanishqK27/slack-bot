import os
from dotenv import load_dotenv
from flask import Flask, request, make_response
import hashlib
import hmac
import threading

from bot_help import main as help1

from bot_zero import main as main0
from bot_one import main as main1
from bot_two import main as main2
from bot_three import main as main3
from bot_four import main as main4
from bot_five import main as main5
from bot_six import main as main6

load_dotenv()
app = Flask(__name__)


@app.route('/slack/help', methods=['POST'])
def slack_help():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    user_id = request.form.get('user_id')

    thread = threading.Thread(target=help1, args=(user_id,))
    thread.start()
    return make_response("Request received and is being processed", 202)


@app.route('/slack/0', methods=['POST'])
def slack_0():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main0, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)

@app.route('/slack/1', methods=['POST'])
def slack_1():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main1, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)

@app.route('/slack/2', methods=['POST'])
def slack_2():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main2, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)

@app.route('/slack/3', methods=['POST'])
def slack_3():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main3, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)

@app.route('/slack/4', methods=['POST'])
def slack_4():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main4, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)


@app.route('/slack/5', methods=['POST'])
def slack_5():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main5, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)


@app.route('/slack/6', methods=['POST'])
def slack_6():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    user_id = request.form.get('user_id')

    # Start a new thread to perform GPU usage calculations and pass the user_id
    thread = threading.Thread(target=main6, args=(user_id,))
    thread.start()

    return make_response("Request received and is being processed...", 202)
