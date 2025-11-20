import numpy as np
from src.inference import model_fn

# Integration test: model_fn returns a pipeline object
def test_model_fn_returns_pipeline():
    pipe = model_fn("/unused/model/dir")
    from transformers import Pipeline
    assert isinstance(pipe, Pipeline)

# Integration test: model_fn pipeline can process a short audio sample
def test_model_fn_pipeline_transcribes_short_audio():
    pipe = model_fn("/unused/model/dir")
    # Generate a short silent audio sample (1 second, 16000 Hz)
    audio = np.zeros(16000, dtype=np.float32)
    result = pipe(audio)
    assert "text" in result
    assert isinstance(result["text"], str)