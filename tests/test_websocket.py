import pytest
import asyncio
from unittest.mock import AsyncMock
from utils.ws_manager import WSManager


@pytest.mark.asyncio
async def test_ws_connect_disconnect():
    manager = WSManager()

    # mock websocket
    ws = AsyncMock()

    poll_id = "123"

    # test connect
    await manager.connect(poll_id, ws)
    ws.accept.assert_awaited_once()  # czy wywołał accept()
    assert ws in manager.connections[poll_id]  # czy dodał do listy

    # test disconnect
    manager.disconnect(poll_id, ws)
    assert ws not in manager.connections[poll_id]  # czy usunął z listy


@pytest.mark.asyncio
async def test_ws_broadcast():
    manager = WSManager()

    # dwa mocki websocket
    ws1 = AsyncMock()
    ws2 = AsyncMock()
    poll_id = "123"

    await manager.connect(poll_id, ws1)
    await manager.connect(poll_id, ws2)

    message = {"event": "vote", "data": {"answer_id": 1}}

    # broadcast
    await manager.broadcast(poll_id, message)

    ws1.send_json.assert_awaited_once_with(message)
    ws2.send_json.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_ws_broadcast_no_connections():
    manager = WSManager()

    poll_id = "nonexistent"
    message = {"event": "vote", "data": {"answer_id": 1}}

    await manager.broadcast(poll_id, message)
