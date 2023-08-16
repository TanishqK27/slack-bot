
from flask import Flask

app = Flask(__name__)


def main():

    # Create the report
    report = f"""
    *CLUSTER USAGE BOT USER GUIDE*:
    
    This is a cluster bot, that will give a daily report on all projects, giving overall usage details, and 
    showing the Project Name, %GPU Utilisation, Number of Nodes Used and Number of Hours Run in the last 24H.
    In order to filter, you can use the following slash commands to see more:
    
    /0: Last 24H Report for all projects
    /1: Last 24H Report for all internal projects on SM2
    /2: Last 24H Report for all internal projects on SM2 (g40)
    /3: Last 24H Report for all internal projects on SM2 (g80)
    /4: Last 24H Report for all external projects on External Cluster
    /5: Last 24H Report for ClipDrop inference on CW Cluster
    /6: Last 24H Report for On Demand Cluster Usage
    

    
    """

    try:
        # Post the message to the Slack channel
        response = slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=report)
    except Exception as e:
        print(f"Error posting message: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)