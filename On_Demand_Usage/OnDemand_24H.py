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



def print_instances_stats(instances_in_service):
    name_replacements = {
        'engine:api-freewilly2-70b': 'FW',
        'engine:stable-diffusion-xl-beta-v2-2-2': 'SDXLB',
        'engine:stable-diffusion-xl-1024-v0-9': 'SDXL.9',
        'engine:stable-diffusion-xl-tiling-v2-2': 'SDXLT',
        'engine:stable-diffusion-xl-1024-v1-0': 'SDXL1',
        'engine:esrgan-v1-x2plus':'ESRGAN',
        'engine:stable-diffusion-xl-1024-v0-9-ft': 'SDXL.9ft',
        'engine:stable-diffusion-xl-1024-v1-0-sgm': 'SDXL1sg',
        'engine:stable-diffusion-xl-1024-v1-0-ft': 'SDXL1ft',
        'engine:stable-diffusion-xl-1024-v1-0-comfy': 'SDXL1co',
        'engine:stable-diffusion-xl-beta-v2-2-5': 'SDXLB',
        'engine:stable-diffusion-xl-v2-2':'SDXL2.2'


    }

    # Initialize the result string with the table header
    result = f'{"Engine":<8} | {"Avg":<3} | {"Min":<3} | {"Max":<3}\n'
    result += '-' * 32 + '\n'  # Add a line under the header

    for series_data in instances_in_service['series']:
        project_name = series_data['scope']

        project_name = name_replacements.get(project_name, project_name)

        pointlist = series_data.get('pointlist', [])
        values = []

        for point in pointlist:
            if hasattr(point, 'value') and point.value[1] is not None:
                values.append(point.value[1])

        avg_value = sum(values) / len(values) if values else 0
        max_value = max(values) if values else 0
        min_value = min(values) if values else 0

        # Append the data for this project to the result string
        result += f'{project_name:<8} | {avg_value:<3.0f} | {min_value:<3.0f} | {max_value:<3.0f}\n'

    return f'```\n{result}\n```'
def print_project_stats(generations_table):
    # Create a dictionary for the name replacements
    name_replacements = {
        'engine:esrgan-v1-x2plus,host:internal.api.stability.ai': 'ESRGAN',
        'engine:stable-diffusion-xl-beta-v2-2-2,host:internal.api.stability.ai': 'SDXLB',
        'engine:stable-diffusion-xl-1024-v0-9,host:internal.api.stability.ai': 'SDXL0.9',
        'engine:stable-diffusion-xl-tiling-v2-2,host:internal.api.stability.ai': 'SDXLT',
        'engine:stable-diffusion-xl-1024-v1-0,host:internal.api.stability.ai': 'SDXL1',
        'engine:stable-diffusion-xl-1024-v1-0-ft,host:internal.api.stability.ai': 'SDXL1ft'
    }

    # Initialize the result string with the table header
    result = f'{"Engine":<6} | {"Avg":<5} | {"Min":<5} | {"Max":<5}\n'
    result += '-'*32 + '\n'  # Add a line under the header

    for series_data in generations_table['series']:
        project_name = series_data['scope']

        # Replace the project name if it's in the dictionary
        project_name = name_replacements.get(project_name, project_name)

        pointlist = series_data.get('pointlist', [])

        # Extract the values from the pointlist
        values = [point.value[1] for point in pointlist if hasattr(point, 'value') and point.value[1] is not None]

        # Calculate avg, min, and max
        avg = sum(values) / len(values) if values else 0
        min_val = min(values) if values else 0
        max_val = max(values) if values else 0

        # Append the data for this project to the result string
        result += f'{project_name:<7} | {avg:<5.2f} | {min_val:<5.2f} | {max_val:<5.2f}\n'

    # Return the result string, wrapped in a code block for Slack
    return f'```\n{result}\n```'






def calculate_total_generations(generations_sum):
    total_generation_sum = 0

    for series_data in generations_sum['series']:
        pointlist = series_data.get('pointlist', [])

        for point in pointlist:
            if hasattr(point, 'value') and point.value[1] is not None:
                total_generation_sum += point.value[1]

    return total_generation_sum

def calculate_average_RPS(generations_avg, generations_sum):
    count = 0
    sum_generation_rate = 0
    for series_data in generations_sum['series']:
        pointlist = series_data.get('pointlist', [])

        for point in pointlist:
            count += 1
            if hasattr(point, 'value') and point.value[1] is not None:
                sum_generation_rate += point.value[1]

    average_rps = sum_generation_rate/(24*60*60)

    return average_rps

def avg_available_capacity(requests_active, instances_in_service):
    count_a = 0
    count_b = 0
    a_list = []
    b_list = []
    for series_data in requests_active['series']:
        pointlist = series_data.get('pointlist', [])

        for point in pointlist:
            count_a += 1
            if hasattr(point, 'value') and point.value[1] is not None:
                a_list.append(point.value[1])

    for series_data in instances_in_service['series']:
        pointlist = series_data.get('pointlist', [])

        for point in pointlist:
            count_b += 1
            if hasattr(point, 'value') and point.value[1] is not None:
                b_list.append(point.value[1])

    c_list = [100 - (a / b * 100) for a, b in zip(a_list, b_list) if b != 0]

    # Calculating the average of list c
    average_c = sum(c_list) / len(c_list) if c_list else 0

    return average_c


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
        requests_active = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "avg:stabilityapi.endpoint.requests.active{host:internal.api.stability.ai}.as_count()"
        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        instances_in_service = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "avg:stabilityapi.endpoint.instances_in_service{host:internal.api.stability.ai}.as_count()"
        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        instances_in_service2 = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "avg:stabilityapi.endpoint.instances_in_service{*} by {engine}"
        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        generations_sum = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "sum:stabilityapi.endpoint.generations{host:internal.api.stability.ai}.as_count()"

        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        generations_avg = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "sum:stabilityapi.endpoint.generations{host:internal.api.stability.ai}.as_rate()"

        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        generations_table = api_instance.query_metrics(
            int((datetime.now() + relativedelta(days=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "sum:stabilityapi.endpoint.generations{host:internal.api.stability.ai} by {engine,host}.as_rate()"

        )

    SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL = "#cluster-usage"
    slack_client = slack.WebClient(token=SLACK_TOKEN)

    # Get the metrics
    total_generations = calculate_total_generations(generations_sum)
    average_rps = calculate_average_RPS(generations_avg, generations_sum)
    average_capacity = avg_available_capacity(requests_active, instances_in_service)
    generations_t = print_project_stats(generations_table)
    instances_t = print_instances_stats(instances_in_service2)

    # Format total generations as millions
    total_generations_millions = total_generations / 1_000_000

    # Create the report
    report = f"""
    *LAST 24H ON DEMAND REPORT*:

    - *Total number of images generated:* {total_generations_millions:.2f}M
    - *Average RPS:* {average_rps:.2f}/s
    - *Average Capacity:* {average_capacity:.2f}%

    *TABLE OF ALL ENGINES BY GENERATION/S*
    {generations_t}
    Note: SDXLB = SDXL beta, SDXLT = SDXL tiling

    *TABLE OF ALL ENGINES BY INSTANCES BY ENDPOINT*
    {instances_t}
    """

    try:
        # Post the message to the Slack channel
        response = slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=report)
    except Exception as e:
        print(f"Error posting message: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)