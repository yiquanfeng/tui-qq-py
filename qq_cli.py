import argparse
import websockets
import asyncio
import json
from settings import settings
from message import sendGroupMessage, sendPrivateMessage
from textual import log
from loguru import logger
from parser import parse_ws_message
from typing import Callable

class QQClient:
    def __init__(self, ws_url: str, token: str):
        self.ws_url = ws_url
        self.header = {
            "Authorization": f"{token}"
        }
        self.websocket = None
    
    async def connect(self):
        if self.websocket is None:
            try: 
                self.websocket = await websockets.connect(self.ws_url, additional_headers=self.header)
            except Exception as e:
                log(f"Failed to connect to WebSocket server: {e}")
                return
        log("Connected to WebSocket server.")
    
    async def parse_message(self):
        pass

    async def listen(self, callback: Callable):
        await self.connect()
        if self.websocket is not None:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    if settings.debug_mode:
                        logger.debug(f"Received message: {data}")
                    parse_data = await parse_ws_message(data)
                    if callback and parse_data:
                        log("Calling back with parsed data.")
                        await callback(parse_data)
                except Exception as e:
                    log(f"Error processing message: {e}")
                    # 继续循环，不要因为一条消息解析失败就断开监听
        else:
            log("WebSocket connection is not established.")
    
    async def send_private(self, user_id: int, message: str):
        if self.websocket is None:
            await self.connect()
            log("independent connected for sending private message.")
        if self.websocket is not None:
            log("may reuse existing connection for sending private message.")
            msg = sendPrivateMessage(user_id, message)
            try:
                await self.websocket.send(json.dumps(msg.__dict__))
                log(f"Sent private message to {user_id}: {message}")
            except Exception as e:
                log(f"Failed to send message: {e}")
                self.websocket = None # Reset connection on failure
        else:
            log("WebSocket connection is not established.")
    
    async def send_group(self, group_id: int, message: str):
        if self.websocket is None:
            await self.connect()
            log("independent connected for sending group message.")
        if self.websocket is not None:
            log("may reuse existing connection for sending group message.")
            msg = sendGroupMessage(group_id, message)
            await self.websocket.send(json.dumps(msg.__dict__))
            log(f"Sent group message to {group_id}: {message}")
        else:
            log("WebSocket connection is not established.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QQ CLI Tool")
    parser.add_argument("--msg", type=str, help="Message to send")
    parser.add_argument("--user", type=int, help="User ID to send message to")
    parser.add_argument("--group", type=int, help="Group ID to send message to")
    parser.add_argument("--receive", type=bool, help="Receive messages", default=False)

    args = parser.parse_args()
    client = QQClient(settings.ws_url, settings.token)
    if args.receive:
        settings.debug_mode = True
        asyncio.run(client.listen(callback=None))
    elif args.msg and args.user:
        asyncio.run(client.send_private(args.user, args.msg))
    elif args.msg and args.group:
        asyncio.run(client.send_group(args.group, args.msg))
    else:
        log("Invalid arguments. Use --help for more information.")
        pass
