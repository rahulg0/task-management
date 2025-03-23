from dotenv import load_dotenv
import json
import os
# import boto3
load_dotenv()

def lambda_handler(event, context):
    task_id = event.get("id")
    task_title = event.get("title")
    user = event.get("user")
    if task_id and task_title:
        message = f"[AWS Lambda] Task Completed: '{task_title}' (ID: {task_id}) by {user}"
        print(message)
        return {"status": "success", "message": message}
    return {"status": "error", "message": "Invalid event data"}
