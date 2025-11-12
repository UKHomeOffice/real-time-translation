[![actions](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/actions.yml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/actions.yml)

# Real-Time Translation

Real-Time Translation leverages Transcription Translation AI models to transcribe and translate audio from a mobile device or laptop via a Web Frontend.

# Architecture Overview

* SageMaker to host OpenAI Whisper model
* AWS DynamoDB, S3 for storage
* AWS Step Functions for Orchestration
* Amazon Cognito for authentication
* Nunjuck, Javascript and the [UK Gov FrontEnd framework|https://frontend.design-system.service.gov.uk/] for FrontEnd

# Language Support

**<50% word error rate (WER)**
Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

# Transcription Translation Models Used

* https://github.com/openai/whisper


