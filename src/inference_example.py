"""Example script to test the deployed SageMaker endpoint"""
import json

import boto3


BUCKET_NAME = "PLACEHOLDER"
KEY_NAME = "PLACEHOLDER"


def main() -> None:
    """Tests the deployed SageMaker endpoint by invoking it with an example audio file"""
    sagemaker_runtime_client = boto3.client("sagemaker-runtime")
    body_data = json.dumps({
        "processedFileBucket": BUCKET_NAME,
        "processedFileKey": KEY_NAME,
        "language": "auto",
        "return_language": False,
        "return_timestamps": False,
        "task": "translate"
    }).encode("utf-8")
    response = sagemaker_runtime_client.invoke_endpoint(
        EndpointName="real-time-translation-whisper",
        Body=body_data,
        ContentType="application/json",
    )
    print(response["Body"].read().decode("utf-8"))


if __name__ == "__main__":
    main()
