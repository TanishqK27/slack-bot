from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from dotenv import load_dotenv
import os
import slack
import json
from datetime import datetime
from statistics import mean
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from dotenv import load_dotenv
import slack
from gspread_formatting import *
from flask import Flask, request, make_response
import hashlib
import hmac
import json
import threading

app = Flask(__name__)
load_dotenv()

DD_SITE = os.environ.get("DD_SITE")
DD_API_KEY = os.environ.get("DD_API_KEY")
DD_APP_KEY = os.environ.get("DD_APP_KEY")

configuration = Configuration(api_key={
    'apiKeyAuth': DD_API_KEY,
    'appKeyAuth': DD_APP_KEY
})
configuration.host = f"https://api.{DD_SITE}"


def print_overall_usage_stats(a):
    # Extract average value from MetricsQueryResponse
    overall_gpu_count = 0
    overall_gpu_sum = 0
    for series_data in a['series']:
        pointlist = series_data['pointlist']
        for point in pointlist:
            overall_gpu_count += 1
            if hasattr(point, 'value') and point.value[1] is not None:
                overall_gpu_sum += point.value[1]

    percentage = overall_gpu_sum/overall_gpu_count

    average_percentage_overall_gpu_util = (percentage - 48) / 3.5

    return average_percentage_overall_gpu_util
def main():
    load_dotenv()

    DD_SITE = os.environ.get("DD_SITE")
    DD_API_KEY = os.environ.get("DD_API_KEY")
    DD_APP_KEY = os.environ.get("DD_APP_KEY")

    configuration = Configuration(api_key={
        'apiKeyAuth': DD_API_KEY,
        'appKeyAuth': DD_APP_KEY
    })
    configuration.host = f"https://api.{DD_SITE}"

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        a = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "abs(avg:nvml.power_usage{availability-zone:cw-prod})"
        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        b = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "sum:nvml.power_usage{availability-zone:cw-prod}"
        )

    percentage = print_overall_usage_stats(a)

    SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL = "#cluster-bot-testing"
    slack_client = slack.WebClient(token=SLACK_TOKEN)

    # Create the report
    report = f"""
    *LAST 24H CW USAGE*: {percentage:.2f}%

    """

    try:
        # Post the message to the Slack channel
        response = slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=report)
    except Exception as e:
        print(f"Error posting message: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)