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
load_dotenv()

# Datadog credentials
DD_SITE = os.environ.get("DD_SITE")
DD_API_KEY = os.environ.get("DD_API_KEY")
DD_APP_KEY = os.environ.get("DD_APP_KEY")

# Slack credentials
API_TOKEN = os.getenv('SLACK_BOT_TOKEN')
CHANNEL_NAME = '#cluster-bot-testing-usage'

# Slack client
client = slack.WebClient(token=API_TOKEN)


def post_message(message):
    response = client.chat_postMessage(channel=CHANNEL_NAME, text=message)
    assert response["ok"], f"Error posting message: {response['error']}"


def open_and_fill_spreadsheet(data: List[List[str]], sheet_name: str) -> gspread.Spreadsheet:
    # Use the OAuth2 credentials to authorize gspread
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    json_creds_str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    json_creds_dict = json.loads(json_creds_str)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds_dict, scope)
    client = gspread.authorize(creds)

    # Open the existing Google Sheets file
    spreadsheet = client.open(sheet_name)

    # Open the first sheet of the spreadsheet
    sheet = spreadsheet.get_worksheet(0)

    # Clear all existing data in the sheet
    sheet.clear()

    # Fill the sheet with your data
    sheet.insert_rows(data, row=1)

    return spreadsheet


def share_spreadsheet_with_link(spreadsheet: gspread.Spreadsheet) -> str:
    # Change the sharing settings to 'anyone with the link can view'
    spreadsheet.share('', perm_type='anyone', role='reader')

    # Return the URL of the Google Sheets file
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit"


def calculate_gpu_usage_info(avg_response, sum_response, overall_response):
    waste_rate_total = 0
    dollars_wasted_total = 0
    percentage_total = 0
    project_info = []
    total_gpu_usage_sum = {}  # To store the total GPU usage for each project in sum_response
    total_data_points = {}  # To store the total number of data points for each project in sum_response
    avg_gpu_usage = {}  # To store the average GPU usage for each project in avg_response
    total_gpu_usage_time_hours = {}
    overall_percentage_total = 0
    total_nodes = 0
    overall_gpu_sum = 0
    overall_gpu_count = 0
    # To store the information for each project

    # Calculate average GPU usage and total GPU usage for all data points in avg_response and sum_response respectively
    for series_data in avg_response['series']:
        project_name = series_data['expression'].split('{project:')[1].split(',')[0]
        pointlist = series_data['pointlist']
        if project_name == 'music_gen':
            continue

        total_gpu_sum = 0  # To store the total GPU usage for the project
        num_points = len(pointlist)  # To store the total number of data points for the project

        for point in pointlist:
            if hasattr(point, 'value') and point.value[1] is not None:
                total_gpu_sum += point.value[1]

        # Calculate the average GPU usage for the project
        if num_points > 0:
            avg_gpu_usage[project_name] = total_gpu_sum / num_points
        else:
            avg_gpu_usage[project_name] = 0

    # a# Calculate and print the total GPU usage and average GPU usage for each project in sum_response
    for series_data in sum_response['series']:
        project_name = series_data['expression'].split('{project:')[1].split(',')[0]

        pointlist = series_data['pointlist']
        if project_name == 'music_gen':
            continue

        total_gpu_usage_sum[project_name] = 0
        total_data_points[project_name] = 0

        for point in pointlist:
            if hasattr(point, 'value') and point.value[1] is not None:
                total_gpu_usage_sum[project_name] += point.value[1]  # Add the second value (GPU usage) to the total
                total_data_points[project_name] += 1  # Increment the number of data points

        # Calculate the total GPU usage time in hours for each project
        project_pointlist = []

        for point in pointlist:
            if hasattr(point, 'value') and point.value[1] is not None:
                timestamp_ms = point.value[0]
                timestamp_datetime = datetime.fromtimestamp(
                    timestamp_ms / 1000.0)  # Convert to seconds and create datetime
                value = point.value[1]
                formatted_time = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime as desired
                project_pointlist.append({'timestamp': formatted_time, 'value': value})

        total_gpu_usage_time_hours[project_name] = 0

        for i in range(len(project_pointlist)):
            if project_pointlist[i]['value'] is not None:
                total_gpu_usage_time_hours[
                    project_name] += 5  # Add 5 minutes to the total GPU usage time for each valid point

        # Convert total minutes to hours (with decimals if not a whole number)

        total_gpu_usage_time_hours[project_name] /= 60
        percentage_gpu_usage = (avg_gpu_usage[project_name] - 48) / 3.

        percentage_gpu_usage = abs(percentage_gpu_usage)
        nodes_used = (total_gpu_usage_sum[project_name] / total_data_points[project_name]) / (
                avg_gpu_usage[project_name] * 8)
        nodes_used = round(nodes_used)

        total_nodes += nodes_used
        print(nodes_used)
        print('nodes', total_nodes)

        percentage_total = percentage_gpu_usage * nodes_used
        overall_percentage_total += percentage_total

        print('Overall percentage total:', overall_percentage_total)

        a = (avg_gpu_usage[project_name])
        b = (total_gpu_usage_sum[project_name] / total_data_points[project_name])
        # Calculate Waste Rate
        waste_rate = (1 - ((a - 48) / 350)) * b / a * 1.3
        waste_rate_total += waste_rate
        dollars_wasted = (1 - ((a - 48) / 350)) * b / a * 1.3 * total_gpu_usage_time_hours[project_name]
        dollars_wasted_total += dollars_wasted
        # Save the project information
        project_info.append({

            'project_name': project_name,
            'avg power': a,
            'sum power': b,
            'percentage_gpu_usage': percentage_gpu_usage,
            'nodes_used': nodes_used,
            'total_gpu_usage_time_hours': total_gpu_usage_time_hours,
            'waste_rate': waste_rate,
            'dollars_wasted': dollars_wasted
        })

    for series_data in overall_response['series']:
        pointlist = series_data['pointlist']
        if project_name == 'music_gen':
            continue

        for point in pointlist:
            overall_gpu_count += 1
            if hasattr(point, 'value') and point.value[1] is not None:
                overall_gpu_sum += point.value[1]

    number = overall_gpu_sum / overall_gpu_count

    average_percentage_overall_gpu_util = (number - 48) / 3.5

    total_average_power = sum(avg_gpu_usage.values())
    print("Total average power:", number)
    num_projects = len(avg_gpu_usage)
    print('Overall percentage of GPU utilisation', average_percentage_overall_gpu_util)
    average_waste_rate = waste_rate_total / num_projects
    print('Average waste rate is:', average_waste_rate)
    print('Total dollars wasted:', dollars_wasted_total)

    # Sort the projects by dollars wasted in descending order

    project_info.sort(key=lambda x: x['dollars_wasted'], reverse=True)
    message_data = project_info.copy()

    # Get the maximum length of project_name for pretty formatting
    max_name_length = max(len(result['project_name']) for result in project_info[:10])

    # Define the format string for the table rows, taking into account the max_name_length
    row_format = "{:<11} | {:>4} | {:>3} | {:>2}"

    # Create the table header using the same row format
    header = row_format.format('Project Name', '%GPU', 'Nod', 'Hr')
    header += "\n" + "-" * len(header)  # Add a line under the header

    # Format the project information
    messages = [header]

    for result in project_info[:10]:
        # Only take the first 10 results
        message = row_format.format(
            result['project_name'][:11],  # Truncate project_name to 15 characters
            f"{result['percentage_gpu_usage']:.0f}%",  # No decimal places for percentage
            f"{result['nodes_used']}",
            f"{(int(result['total_gpu_usage_time_hours'][result['project_name']]))*0.4:.0f}"  # No decimal places for hours
        )
        messages.append(message)
    overall_report = f"*LAST 1H EXTERNAL GPU UTILISATION REPORT (NORMAL PRIORITY)*\n\n"
    overall_report += "*Overview:*\n"
    overall_report += "In today's report, we present the external GPU utilization statistics for the system in the last 1 hours. " \
                      "The following insights offer a comprehensive view of how GPU resources were utilized " \
                      "across various projects. \n\n"
    overall_report += "Overall GPU Utilization:\n"
    overall_report += f"*- Average GPU power draw across all projects:*  {number:.2f} watts\n"

    overall_report += f'*- Average percentage GPU usage:* {average_percentage_overall_gpu_util:.2f}%\n'

    overall_report += f"*Table which shows the top 10 projects*\n"
    overall_report += f'Note the empty project name is idle, unused nodes.'
    # Join the messages together

    full_message = overall_report + "```" + "\n".join(messages) + "```"

    # Add a closing line
    full_message += "\nPlease take necessary actions to mitigate wastage."
    full_message += f"\nCheck out the full report: https://docs.google.com/spreadsheets/d/1_OgKcbKw58ZEgIc4IJ4Epzs4CvW0FZIpLOiQE1Zoe04/edit#gid=0"

    return full_message, message_data, number, average_percentage_overall_gpu_util


# Your existing code here
# You should return project_info at the end of this function

def main():
    configuration = Configuration(api_key={
        'apiKeyAuth': DD_API_KEY,
        'appKeyAuth': DD_APP_KEY
    })
    configuration.host = f"https://api.{DD_SITE}"

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        sum_response = api_instance.query_metrics(
            int((datetime.now() + relativedelta(hours=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "sum:dcgm.power_usage{qos:normal,availability-zone:external} by {project}"
        )
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        avg_response = api_instance.query_metrics(
            int((datetime.now() + relativedelta(hours=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "avg:dcgm.power_usage{qos:normal,availability-zone:external} by {project}"
        )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        overall_response = api_instance.query_metrics(
            int((datetime.now() + relativedelta(hours=-1)).timestamp()),
            int(datetime.now().timestamp()),
            "abs(avg:dcgm.power_usage{qos:normal,availability-zone:external})"
        )

    message_data, gpu_usage_info, number, average_percentage_overall_gpu_util = calculate_gpu_usage_info(avg_response,
                                                                                                         sum_response,
                                                                                                         overall_response)

    # Convert your data into a 2D list
    data = []

    # Add the report text to the data
    data.append(["LAST 1H EXTERNAL GPU UTILISATION REPORT (NORMAL PRIORITY)"])
    data.append(["Overview:"])
    data.append([
        "In today's report, we present the external GPU utilization statistics for the system in the last 1 hours. The following insights offer a comprehensive view of how GPU resources were utilized across various projects."])
    data.append(["Overall GPU Utilization:"])
    data.append([f"- Average GPU power draw across all projects:  {number:.2f} watts"])
    data.append([f'- Average percentage GPU usage: {average_percentage_overall_gpu_util:.2f}%'])
    data.append(["Table which shows the top 10 projects"])
    data.append(["Note the empty project name is idle, unused nodes."])

    # Add an empty row for spacing
    data.append([])

    # Add the table headers
    data.append(['Project Name', '% GPU Usage', 'Nodes Used', 'Hours'])

    for result in gpu_usage_info[:10]:
        data.append([
            result['project_name'],
            f"{result['percentage_gpu_usage']:.2f}%",
            f"{result['nodes_used']}",
            f"{(result['total_gpu_usage_time_hours'][result['project_name']])   :.2f} hours"
        ])

    # Open the existing Google Sheets file and fill it with new data
    spreadsheet = open_and_fill_spreadsheet(data, 'LAST 1H EXTERNAL GPU UTILISATION REPORT (NORMAL PRIORITY)')
    # Get the worksheet
    worksheet = spreadsheet.get_worksheet(0)

    # Format A2
    fmt = CellFormat(textFormat=TextFormat(bold=True, fontSize=14))
    format_cell_range(worksheet, "A2:A2", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "A3:A3", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "A4:A4", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "A5:A6", fmt)

    # Format A7
    fmt = CellFormat(textFormat=TextFormat(bold=True, fontSize=14))
    format_cell_range(worksheet, "A7:A7", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=True, fontSize=14))
    format_cell_range(worksheet, "A7:A7", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "A8:A8", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "B11:B20", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "C11:C20", fmt)

    fmt = CellFormat(textFormat=TextFormat(bold=False, fontSize=12))
    format_cell_range(worksheet, "D11:D20", fmt)

    # Format A9:D9 to be grey and bold
    fmt = CellFormat(textFormat=TextFormat(bold=True, fontSize=12))
    format_cell_range(worksheet, "A10:D10", fmt)

    # Format A10:A20 to be grey and bold
    fmt = CellFormat(textFormat=TextFormat(bold=True, fontSize=12))
    format_cell_range(worksheet, "A10:A20", fmt)

    # Get the shareable link
    link = share_spreadsheet_with_link(spreadsheet)

    # Add the link to your message
    post_message(message_data)


if __name__ == "__main__":
    app.run(debug=True)