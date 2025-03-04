import pytest
from src.handlers import start

class DummyMessage:
    def __init__(self):
        self.replies = []

    async def reply_text(self, text):
        self.replies.append(text)

class DummyUpdate:
    def __init__(self, text=""):
        self.message = DummyMessage()
        self.message.text = text

class DummyContext:
    user_data = {}

@pytest.mark.asyncio
async def test_start_handler():
    update = DummyUpdate()
    context = DummyContext()
    await start(update, context)
    assert len(update.message.replies) > 0
    assert "Welcome" in update.message.replies[0]
