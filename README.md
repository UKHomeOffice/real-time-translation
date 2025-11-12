[![kics](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/kics.yml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/kics.yml)
[![trivy](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/trivy.yml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/trivy.yml)
[![terraform](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/terraform.yaml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/terraform.yaml)

# Real-Time Translation

Real-Time Translation leverages Transcription Translation AI models to transcribe and translate audio, exposed via API and a UK Gov Web Frontend.

# Architecture Overview

* SageMaker to host the OpenAI Whisper model
* AWS DynamoDB, S3 for storage
* AWS Step Functions, AWS Lambda for Orchestration
* AWS API Gaetway for APIs
* Amazon Cognito for authentication
* Nunjuck, Javascript and the [UK Gov FrontEnd framework](https://frontend.design-system.service.gov.uk/) for FrontEnd

# Language Support

**<50% word error rate (WER)**
Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

# Transcription Translation Models Used

* https://github.com/openai/whisper

# Run Commands 

# Developing the Real-Time Translation API

To work on developing the core Real-Time Translation API, run the below command which will deploy the service as an isolated Terraform Workspace:
```bash
$ make WHISPER_ENDPOINT_NAME=<endpoint_name> WORKSPACE_NAME=<tf_workspace_name>
```

To destroy your Workspace and tear down the resources:
```bash
make destroy-terraform-workspace WHISPER_ENDPOINT_NAME=<endpoint_name> WORKSPACE_NAME=<tf_workspace_name>
```







