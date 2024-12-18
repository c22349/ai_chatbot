from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import boto3
import json
import os
import re


sqs_queue_url = os.environ.get("SQS_QUEUE_URL")
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

sqs = boto3.client("sqs")


# アプリの初期化
app = App(
    token=slack_bot_token,
    signing_secret=slack_signing_secret,
    process_before_response=True,
)

# Slackアプリがメンションされた時
@app.event("app_mention")
def handle_app_mention_events(event, say):
    channel_id = event["channel"]
    input_text = re.sub("<@.+>", "", event["text"]).strip()

    files = event.get("files")
    if files is None:
        say("画像ファイルが添付されていません。")
        return

    file_type = files[0]["mimetype"]
    if file_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
        say("これは画像ファイルではありません。")
        return

    say("少々お待ちください...")
    file_url = files[0]["url_private_download"]
    sqs.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=json.dumps({
            "channel_id": channel_id,
            "input_text": input_text,
            "file_type": file_type,
            "file_url": file_url,
        }),
    )


# Lambdaイベントハンドラー
def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
