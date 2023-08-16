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
from flask import Flask
import json
app = Flask(__name__)


# Slack credentials
API_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_NAME = '#proj-cluster-usage'

# Slack client
client = slack.WebClient(token=API_TOKEN)


def post_message(message):
    response = client.chat_postMessage(channel=CHANNEL_NAME, text=message)
    assert response["ok"], f"Error posting message: {response['error']}"

def main():

    # Create the report
    message_data = f"""
*CLUSTER USAGE BOT USER GUIDE*:
    
This is a cluster bot, that will give a daily report on all projects, giving overall usage details, and 
showing the Project Name, %GPU Utilisation, Number of Nodes Used and Number of Hours Run in the last 24H.
In order to filter, you can use the following slash commands to see more:
    
*/0:* Last 24H Report for all projects
*/1:* Last 24H Report for all internal projects on SM2
*/2:* Last 24H Report for all internal projects on SM2 (g40)
*/3:* Last 24H Report for all internal projects on SM2 (g80)
*/4:* Last 24H Report for all external projects on External Cluster
*/5:* Last 24H Report for ClipDrop inference on CW Cluster
*/6:* Last 24H Report for On Demand Cluster Usage
    

    
    """

    try:
        post_message(message_data)
    except Exception:
        print('Error')

if __name__ == "__main__":
    app.run(debug=True)