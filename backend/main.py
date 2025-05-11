import boto3
import json
from newspaper import Article

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
)

MODEL_ID = "meta.llama4-maverick-17b-instruct-v1:0"  # Confirm the correct model ID

def lambda_handler(event, context):
    try:
        # Parse the URL from the API Gateway event body
        body = json.loads(event.get("body", "{}"))
        url = body.get("url", "")

        if not url:
            return {"statusCode": 400, "body": json.dumps({"error": "URL is required."})}

        # Extract article content
        article = Article(url)
        article.download()
        article.parse()

        prompt_text = f"Summarize the following article into concise bullet points:\n\n{article.text[:3000]}"

        # Prepare Bedrock Converse API request
        conversation_request = {
            "messages": [{"role": "user", "content": [{"text": prompt_text}]}],
            "inferenceConfig": {
                "temperature": 0.5,
                "topP": 0.9,
                "maxTokens": 300
            }
        }

        # Call Bedrock Converse API
        response = bedrock_client.converse(
            modelId=MODEL_ID,
            messages=conversation_request["messages"],
            inferenceConfig=conversation_request["inferenceConfig"]
        )

        summary_text = response["output"]["message"]["content"][0]["text"].strip()

        return {
            "statusCode": 200,
            "body": json.dumps({"summary": summary_text}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
