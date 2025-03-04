import pytest
from src.utils import get_user_model, get_padding
from src.config import WATCH_MODELS, DEFAULT_PADDING

class DummyContext:
    user_data = {}

@pytest.fixture
def dummy_context():
    return DummyContext()

def test_get_user_model_default(dummy_context):
    model = get_user_model(dummy_context)
    assert model == WATCH_MODELS['series_45mm']

def test_get_user_model_set(dummy_context):
    dummy_context.user_data['watch_model'] = WATCH_MODELS['ultra_2']
    model = get_user_model(dummy_context)
    assert model == WATCH_MODELS['ultra_2']

def test_get_padding_default(dummy_context):
    padding = get_padding(dummy_context)
    assert padding == DEFAULT_PADDING

def test_get_padding_set(dummy_context):
    dummy_context.user_data['padding'] = 50
    padding = get_padding(dummy_context)
    assert padding == 50
