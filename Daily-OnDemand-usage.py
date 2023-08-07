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
        "avg:stabilityapi.endpoint.generations{host:internal.api.stability.ai} by {engine,host}.as_rate()"
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

print(instances_in_service2)
def print_instances_stats(instances_in_service2):
    # Create a dictionary for the name replacements

    name_replacements = {
        'engine:esrgan-v1-x2plus,host:internal.api.stability.ai': 'ESRGAN',
        'engine:stable-diffusion-xl-beta-v2-2-2,host:internal.api.stability.ai': 'SDXLB',
        'engine:stable-diffusion-xl-1024-v0-9,host:internal.api.stability.ai': 'SDXL0.9',
        'engine:stable-diffusion-xl-tiling-v2-2,host:internal.api.stability.ai': 'SDXLT',
        'engine:stable-diffusion-xl-1024-v1-0,host:internal.api.stability.ai': 'SDXL1.0'
    }

    # Initialize the result string with the table header
    result = f'{"Engine":<6} | {"Avg":<5} | {"Min":<5} | {"Max":<5}\n'
    result += '-'*32 + '\n'  # Add a line under the header

    for series_data in instances_in_service['series']:
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
def print_project_stats(generations_table):
    # Create a dictionary for the name replacements
    name_replacements = {
        'engine:esrgan-v1-x2plus,host:internal.api.stability.ai': 'ESRGAN',
        'engine:stable-diffusion-xl-beta-v2-2-2,host:internal.api.stability.ai': 'SDXLB',
        'engine:stable-diffusion-xl-1024-v0-9,host:internal.api.stability.ai': 'SDXL0.9',
        'engine:stable-diffusion-xl-tiling-v2-2,host:internal.api.stability.ai': 'SDXLT',
        'engine:stable-diffusion-xl-1024-v1-0,host:internal.api.stability.ai': 'SDXL1.0'
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

def calculate_average_RPS(generations_avg):
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



# Load environment variables from .env file




# Get Slack token from environment variables
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Specify Slack channel in the code
SLACK_CHANNEL = "#cluster-bot-testing"

# Initialize a Web API client
slack_client = slack.WebClient(token=SLACK_TOKEN)

# Get the metrics
total_generations = calculate_total_generations(generations_sum)
average_rps = calculate_average_RPS(generations_avg)
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