"""
Module: test_inference.py

This module contains unit tests for the `model_fn` and `predict_fn` functions from the `inference` module.
The tests use the pytest framework and unittest.mock for patching dependencies and simulating various scenarios.

Test coverage includes:
- Initialization of the inference pipeline with CUDA and CPU settings in `model_fn`.
- Transcription and translation workflows in `predict_fn`, including handling of default and custom options.
- Verification of S3 file download, audio file reading, pipeline invocation, and file cleanup.
- Handling of file deletion errors (FileNotFoundError) during cleanup.

Each test is designed to validate the correct behavior of the inference functions under different conditions and input parameters.
"""
from unittest.mock import patch, MagicMock

import torch

from src.inference import model_fn, predict_fn


@patch("src.inference.pipeline")
@patch("torch.cuda.is_available")
def test_model_fn_cuda_available(mock_cuda_available, mock_pipeline):
    """
    Test that `model_fn` initializes the pipeline with CUDA settings when a GPU is available.
    """
    mock_cuda_available.return_value = True
    mock_pipe_instance = MagicMock()
    mock_pipeline.return_value = mock_pipe_instance

    result = model_fn("/some/model/dir")

    mock_pipeline.assert_called_once_with(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        torch_dtype=torch.float16,
        chunk_length_s=30,
        device="cuda:0",
    )
    assert result == mock_pipe_instance


@patch("src.inference.pipeline")
@patch("torch.cuda.is_available")
def test_model_fn_cpu(mock_cuda_available, mock_pipeline):
    """
    Test that `model_fn` initializes the pipeline with CPU settings when a GPU is not available.
    """
    mock_cuda_available.return_value = False
    mock_pipe_instance = MagicMock()
    mock_pipeline.return_value = mock_pipe_instance

    result = model_fn("/some/model/dir")

    mock_pipeline.assert_called_once_with(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        torch_dtype=torch.float32,
        chunk_length_s=30,
        device="cpu",
    )
    assert result == mock_pipe_instance


@patch("src.inference.os.remove")
@patch("src.inference.soundfile.read")
@patch("src.inference.boto3.client")
def test_predict_fn_transcribe_defaults(mock_boto3_client, mock_soundfile_read, mock_os_remove):
    """
    Test that `predict_fn` performs transcription with default options and cleans up the file.
    """
    mock_s3 = MagicMock()
    mock_boto3_client.return_value = mock_s3
    mock_soundfile_read.return_value = (["audio"], None)
    mock_pipe = MagicMock()
    mock_pipe.return_value = {"text": "transcribed text"}

    data = {
        "processedFileBucket": "bucket",
        "processedFileKey": "audio.wav",
        "language": "auto"
    }

    result = predict_fn(data, mock_pipe)

    mock_s3.download_file.assert_called_once_with("bucket", "audio.wav", "/tmp/audio.wav")
    mock_soundfile_read.assert_called_once_with("/tmp/audio.wav")
    mock_pipe.assert_called_once()
    mock_os_remove.assert_called_once_with("/tmp/audio.wav")
    assert result == "transcribed text"


@patch("src.inference.os.remove")
@patch("src.inference.soundfile.read")
@patch("src.inference.boto3.client")
def test_predict_fn_translate_with_options(mock_boto3_client, mock_soundfile_read, mock_os_remove):
    """
    Test that `predict_fn` performs translation with specified options and cleans up the file.
    """
    mock_s3 = MagicMock()
    mock_boto3_client.return_value = mock_s3
    mock_soundfile_read.return_value = (["audio"], None)
    mock_pipe = MagicMock()
    mock_pipe.return_value = {"text": "translated text"}

    data = {
        "processedFileBucket": "bucket",
        "processedFileKey": "audio.wav",
        "language": "en",
        "return_language": True,
        "return_timestamps": True,
        "task": "translate"
    }

    result = predict_fn(data, mock_pipe)

    mock_s3.download_file.assert_called_once_with("bucket", "audio.wav", "/tmp/audio.wav")
    mock_soundfile_read.assert_called_once_with("/tmp/audio.wav")
    mock_pipe.assert_called_once_with(
        ["audio"],
        return_timestamps=True,
        return_language=True,
        generate_kwargs={"language": "en", "task": "translate"}
    )
    mock_os_remove.assert_called_once_with("/tmp/audio.wav")
    assert result == "translated text"


@patch("src.inference.os.remove", side_effect=FileNotFoundError)
@patch("src.inference.soundfile.read")
@patch("src.inference.boto3.client")
def test_predict_fn_file_not_found_cleanup(mock_boto3_client, mock_soundfile_read, mock_os_remove):
    """
    Test that `predict_fn` handles FileNotFoundError when deleting the file.
    """
    mock_s3 = MagicMock()
    mock_boto3_client.return_value = mock_s3
    mock_soundfile_read.return_value = (["audio"], None)
    mock_pipe = MagicMock()
    mock_pipe.return_value = {"text": "some text"}

    data = {
        "processedFileBucket": "bucket",
        "processedFileKey": "audio.wav",
        "language": "auto"
    }

    result = predict_fn(data, mock_pipe)

    mock_s3.download_file.assert_called_once_with("bucket", "audio.wav", "/tmp/audio.wav")
    mock_soundfile_read.assert_called_once_with("/tmp/audio.wav")
    mock_pipe.assert_called_once()
    mock_os_remove.assert_called_once_with("/tmp/audio.wav")
    assert result == "some text"
