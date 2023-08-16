
import os
from dotenv import load_dotenv
from flask import Flask, request, make_response
import hashlib
import hmac
import threading

from SageMaker_2.Internal_Usage_SM2.Unflitered.Internal_Usage_1H import main as main_1h
from SageMaker_2.Internal_Usage_SM2.Unflitered.Internal_Usage_4H import main as main_4h
from SageMaker_2.Internal_Usage_SM2.Unflitered.Internal_Usage_5min import main as main_5min
from SageMaker_2.Internal_Usage_SM2.Unflitered.Internal_Usage_12H import main as main_12h
from SageMaker_2.Internal_Usage_SM2.Unflitered.Internal_Usage_24H import main as main_24h

from SageMaker_2.Internal_Usage_SM2.Top.Top_Internal_Usage_1H import main as topmain_1h
from SageMaker_2.Internal_Usage_SM2.Top.Top_Internal_Usage_4H import main as topmain_4h
from SageMaker_2.Internal_Usage_SM2.Top.Top_Internal_Usage_5min import main as topmain_5min
from SageMaker_2.Internal_Usage_SM2.Top.Top_Internal_Usage_12H import main as topmain_12h
from SageMaker_2.Internal_Usage_SM2.Top.Top_Internal_Usage_24H import main as topmain_24h

from SageMaker_2.Internal_Usage_SM2.Normal.Normal_Internal_Usage_1H import main as normalmain_1h
from SageMaker_2.Internal_Usage_SM2.Normal.Normal_Internal_Usage_4H import main as normalmain_4h
from SageMaker_2.Internal_Usage_SM2.Normal.Normal_Internal_Usage_5min import main as normalmain_5min
from SageMaker_2.Internal_Usage_SM2.Normal.Normal_Internal_Usage_12H import main as normalmain_12h
from SageMaker_2.Internal_Usage_SM2.Normal.Normal_Internal_Usage_24H import main as normalmain_24h

from SageMaker_2.Internal_Usage_SM2.Idle.Idle_Internal_Usage_1H import main as idlemain_1h
from SageMaker_2.Internal_Usage_SM2.Idle.Idle_Internal_Usage_4H import main as idlemain_4h
from SageMaker_2.Internal_Usage_SM2.Idle.Idle_Internal_Usage_5min import main as idlemain_5min
from SageMaker_2.Internal_Usage_SM2.Idle.Idle_Internal_Usage_12H import main as idlemain_12h
from SageMaker_2.Internal_Usage_SM2.Idle.Idle_Internal_Usage_24H import main as idlemain_24h

from SageMaker_2.External_Usage_SM2.Unfiltered.External_Usage_24H import main as exmain_24h
from SageMaker_2.External_Usage_SM2.Unfiltered.External_Usage_12H import main as exmain_12h
from SageMaker_2.External_Usage_SM2.Unfiltered.External_Usage_4H import main as exmain_4h
from SageMaker_2.External_Usage_SM2.Unfiltered.External_Usage_1H import main as exmain_1h

from SageMaker_2.External_Usage_SM2.Top.Top_External_Usage_1H import main as extopmain_1h
from SageMaker_2.External_Usage_SM2.Top.Top_External_Usage_4H import main as extopmain_4h
from SageMaker_2.External_Usage_SM2.Top.Top_External_Usage_12H import main as extopmain_12h
from SageMaker_2.External_Usage_SM2.Top.Top_External_Usage_24H import main as extopmain_24h

from SageMaker_2.External_Usage_SM2.Normal.Normal_External_Usage_1H import main as exnormalmain_1h
from SageMaker_2.External_Usage_SM2.Normal.Normal_External_Usage_4H import main as exnormalmain_4h
from SageMaker_2.External_Usage_SM2.Normal.Normal_External_Usage_12H import main as exnormalmain_12h
from SageMaker_2.External_Usage_SM2.Normal.Normal_External_Usage_24H import main as exnormalmain_24h

from SageMaker_2.External_Usage_SM2.Idle.Idle_External_Usage_1H import main as exidlemain_1h
from SageMaker_2.External_Usage_SM2.Idle.Idle_External_Usage_4H import main as exidlemain_4h
from SageMaker_2.External_Usage_SM2.Idle.Idle_External_Usage_12H import main as exidlemain_12h
from SageMaker_2.External_Usage_SM2.Idle.Idle_External_Usage_24H import main as exidlemain_24h

from SageMaker_2.On_Demand_Usage_SM2.OnDemand_24H import main as main_od24

from CW.Internal_Usage_CW.Unflitered.Internal_Usage_1H import main as cwmain_1h
from CW.Internal_Usage_CW.Unflitered.Internal_Usage_4H import main as cwmain_4h
from CW.Internal_Usage_CW.Unflitered.Internal_Usage_5min import main as cwmain_5min
from CW.Internal_Usage_CW.Unflitered.Internal_Usage_12H import main as cwmain_12h
from CW.Internal_Usage_CW.Unflitered.Internal_Usage_24H import main as cwmain_24h

load_dotenv()
app = Flask(__name__)


'''Unfiltered Internal Usages'''
@app.route('/slack/Usage24h', methods=['POST'])
def slack_usage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=main_24h)
    thread.start()



    return make_response("Processing your request...", 200)
@app.route('/slack/Usage12h', methods=['POST'])
def slack_usage12h():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=main_12h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/Usage4h', methods=['POST'])
def slack_usage4h():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=main_4h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/Usage1h', methods=['POST'])
def slack_usage1h():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=main_1h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/Usage5min', methods=['POST'])
def slack_usage5min():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=main_5min)
    thread.start()

    return make_response("Processing your request...", 200)

'''Top Internal Usages'''
@app.route('/slack/TopUsage24h', methods=['POST'])
def slack_topusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=topmain_24h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/TopUsage12h', methods=['POST'])
def slack_topusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=topmain_12h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/TopUsage4h', methods=['POST'])
def slack_topusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=topmain_4h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/TopUsage1h', methods=['POST'])
def slack_topusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=topmain_1h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/TopUsage5min', methods=['POST'])
def slack_topusage5min():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=topmain_5min)
    thread.start()

    return make_response("Processing your request...", 200)

'''Normal Internal Usages'''



@app.route('/slack/NormalUsage24h', methods=['POST'])
def slack_normalusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=normalmain_24h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/NormalUsage12h', methods=['POST'])
def slack_normalusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=normalmain_12h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/NormalUsage4h', methods=['POST'])
def slack_normalusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=normalmain_4h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/NormalUsage1h', methods=['POST'])
def slack_normalusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=normalmain_1h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/NormalUsage5min', methods=['POST'])
def slack_normalusage5min():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=normalmain_5min)
    thread.start()

    return make_response("Processing your request...", 200)


'''Idle Internal Usages'''

@app.route('/slack/IdleUsage24h', methods=['POST'])
def slack_idleusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=idlemain_24h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleUsage12h', methods=['POST'])
def slack_idleusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=idlemain_12h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleUsage4h', methods=['POST'])
def slack_idleusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=idlemain_4h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleUsage1h', methods=['POST'])
def slack_idleusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=idlemain_1h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleUsage5min', methods=['POST'])
def slack_idleusage5min():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=idlemain_5min)
    thread.start()

    return make_response("Processing your request...", 200)




'''Unfiltered External Usages'''
@app.route('/slack/ExUsage24h', methods=['POST'])
def slack_exusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exmain_24h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/ExUsage12h', methods=['POST'])
def slack_exusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exmain_12h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/ExUsage4h', methods=['POST'])
def slack_exusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exmain_4h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/ExUsage1h', methods=['POST'])
def slack_exusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exmain_1h)
    thread.start()

    return make_response("Processing your request...", 200)


'''Top External Usages'''
@app.route('/slack/TopExUsage24h', methods=['POST'])
def slack_topexusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=extopmain_24h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/TopExUsage12h', methods=['POST'])
def slack_topexusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=extopmain_12h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/TopExUsage4h', methods=['POST'])
def slack_topexusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=extopmain_4h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/TopExUsage1h', methods=['POST'])
def slack_topexusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=extopmain_1h)
    thread.start()

    return make_response("Processing your request...", 200)


'''Normal External Usages'''
@app.route('/slack/NormalExUsage24h', methods=['POST'])
def slack_normalexusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exnormalmain_24h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/NormalExUsage12h', methods=['POST'])
def slack_normalexusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exnormalmain_12h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/NormalExUsage4h', methods=['POST'])
def slack_normalexusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exnormalmain_4h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/NormalExUsage1h', methods=['POST'])
def slack_normalexusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exnormalmain_1h)
    thread.start()

    return make_response("Processing your request...", 200)

'''Idle External Usages'''

@app.route('/slack/IdleExUsage24h', methods=['POST'])
def slack_idleexusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exidlemain_24h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleExUsage12h', methods=['POST'])
def slack_idleexusage12h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exidlemain_12h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleExUsage4h', methods=['POST'])
def slack_idleexusage4h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exidlemain_4h)
    thread.start()

    return make_response("Processing your request...", 200)

@app.route('/slack/IdleExUsage1h', methods=['POST'])
def slack_idleexusage1h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=exidlemain_1h)
    thread.start()

    return make_response("Processing your request...", 200)



'''Unfiltered On Demand Usages'''
@app.route('/slack/od24h', methods=['POST'])
def slack_od24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=main_od24)
    thread.start()

    return make_response("Processing your request...", 200)


''' CW Unfiltered Internal Usages'''
@app.route('/slack/CWUsage24h', methods=['POST'])
def slack_cwusage24h():
    # Validate the request from Slack
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    # Start a new thread to perform GPU usage calculations
    thread = threading.Thread(target=cwmain_24h)
    thread.start()



    return make_response("Processing your request...", 200)
@app.route('/slack/CWUsage12h', methods=['POST'])
def slack_cwusage12h():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=cwmain_12h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/CWUsage4h', methods=['POST'])
def slack_cwusage4h():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=cwmain_4h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/CWUsage1h', methods=['POST'])
def slack_cwusage1h():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=cwmain_1h)
    thread.start()

    return make_response("Processing your request...", 200)
@app.route('/slack/CWUsage5min', methods=['POST'])
def slack_cwusage5min():
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode(f"v0:{timestamp}:{request.get_data().decode()}")

    slack_signing_secret = bytes(os.getenv('SLACK_SIGNING_SECRET'), 'utf-8')
    hashed_req = 'v0=' + hmac.new(slack_signing_secret, req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hashed_req, signature):
        return make_response("Invalid request", 403)

    thread = threading.Thread(target=cwmain_5min)
    thread.start()

    return make_response("Processing your request...", 200)