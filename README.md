[![terraform](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/terraform.yaml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/terraform.yaml)
[![linting](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/pylint.yaml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/pylint.yaml)
[![unit tests](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/pytest_unit.yaml/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/pytest_unit.yaml)
[![integration tests](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/pytest_integration/badge.svg)](https://github.com/UKHomeOffice/real-time-translation/actions/workflows/terrafpytest_integrationorm.yaml)

# Real-Time Translation

Real-Time Translation leverages Transcription Translation AI models to transcribe and translate audio, exposed via API and a UK Gov Web Frontend.
This repository is *NOT* production ready code. It shows a small example of the kind of technology and design pattern that is used in the Real-Time Translation project.

# Architecture Overview

* SageMaker Endpoints to host the OpenAI Whisper model

# Language Support

**<50% word error rate (WER)**
Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

# Transcription Translation Models Used

* https://github.com/openai/whisper

# Testing output

## Setup commands
1. `terraform init`
2. `terraform validate`
3. `terraform plan -var="account_number=<ACCOUNT_NUMBER>"`
4. `terraform apply -var="account_number=<ACCOUNT_NUMBER>"`

## Example inference
### Prerequisities
1. An example wav file with sampling rate 16kHz, 16 bit depth, mono audio has been uploaded to your S3 bucket of choice
2. AWS CLI has been setup
3. Placeholders have been overwritten in `src/inference_example.py`
## Commands
1. `pip install -r inference_example_requirements.txt`
2. `python3 src/inference_example.py`
