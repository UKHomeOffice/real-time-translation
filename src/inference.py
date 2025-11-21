"""
This module provides functions for automatic speech recognition (ASR) and translation using 
Hugging Face Transformers and OpenAI Whisper models, designed for use with 
AWS SageMaker Hugging Face Inference Toolkit.

AWS SageMaker Hugging Face Inference Toolkit expects specific function signatures 
for model loading and prediction.
AWS SageMaker Hugging Face Inference Toolkit expects the inference script to be 
within a `code` folder.

Required by SageMaker Hugging Face Inference Toolkit 
(see: https://github.com/aws/sagemaker-huggingface-inference-toolkit).

Functions:
    model_fn(model_dir):
        Initializes and returns a Hugging Face ASR pipeline using the specified Whisper model.
        Automatically selects device (CPU/GPU) and appropriate torch data type.
    predict_fn(data, pipe):
        Downloads an audio file from AWS S3, reads and processes it, and performs 
        transcription or translation using the provided pipeline. 
        Supports options for returning language, timestamps, and specifying the task 
        (transcribe/translate).
        Cleans up temporary files after processing.
"""
import os

import boto3
import soundfile
import torch
from transformers import pipeline


# pylint: disable=unused-argument
def model_fn(model_dir):
    """
    Initializes and returns an automatic speech recognition pipeline using the Whisper model.

    Args:
        model_dir (str): Directory path for the model (not used in this implementation, 
        but necessary for SageMaker Hugging Face Inference Toolkit compatibility).

    Returns:
        transformers.Pipeline: A Hugging Face pipeline object for automatic speech recognition,
        configured to use the 'openai/whisper-small' model, with device and torch dtype
        automatically selected based on CUDA availability.
    """
    model_name = "openai/whisper-small"

    # Set device settings
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    # Create pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        torch_dtype=torch_dtype,
        chunk_length_s=30,
        device=device,
    )
    return pipe


def predict_fn(data, pipe):
    """
    Downloads an audio file from S3, processes it, and performs transcription or 
    translation using the provided pipeline. Cleans up temporary files after processing.

    Args:
        data (dict): Dictionary containing the following keys:
            - 'processedFileBucket' (str): Name of the S3 bucket containing the audio file.
            - 'processedFileKey' (str): Key (path) to the audio file in the S3 bucket.
            - 'language' (str): Language code for transcription/translation, 
            or 'auto' for automatic detection.
            - 'return_language' (bool, optional): Whether to return detected language. 
            Defaults to False.
            - 'return_timestamps' (bool, optional): Whether to return timestamps in the output. 
            Defaults to False.
            - 'task' (str, optional): Task type, either 'transcribe' or 'translate'. 
            Defaults to 'transcribe'.
        pipe (callable): A pipeline object/function that performs transcription or translation 
        on audio data. This is typically created by the `model_fn`.

    Returns:
        str: The transcribed or translated text from the audio file.
    """
    # Create an S3 client
    s3 = boto3.client('s3')

    # Find file name
    filename = os.path.join("/tmp", data["processedFileKey"].split('/')[-1])
    # Download the file
    s3.download_file(data["processedFileBucket"], data["processedFileKey"], filename)

    print('DOWNLOADED FILE SUCCESSFULLY!')

    # Opening data file and creating input for processor
    audio_data, _ = soundfile.read(filename)

    print('SOUNDFILE READING COMPLETE')

    # setting default values
    if 'return_language' not in data:
        data['return_language'] = False
    if 'return_timestamps' not in data:
        data['return_timestamps'] = False
    if 'task' not in data:
        data['task'] = 'transcribe'
    if data['language'] == 'auto':
        data['language'] = None

    # decode token ids to text
    transcription = pipe(audio_data,
                         return_timestamps=data['return_timestamps'],
                         return_language=data['return_language'],
                         generate_kwargs = {"language":data['language'],
                                            "task": data['task']}
                        )['text']
    print('TRANSCRIPTION/TRANSLATION COMPLETE!')
    # Delete downloaded file
    try:
        os.remove(filename)
    except FileNotFoundError:
        print("File not deleted")
    return transcription
