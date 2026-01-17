import argparse
from loguru import logger
import websockets
import asyncio
import json
from settings import settings
from message import receivePrivateMessage, receiveGroupMessage, sendGroupMessage, sendPrivateMessage


def call_api():
    return
def parse_json():
    return

def parse_ws_mesage(json_message: dict):
    if json_message['post_type'] == 'message':
        if json_message['message_type'] == 'private':
            msg = receivePrivateMessage(json_message)
            logger.info(f"Private message from {msg.user_id}: {msg.message}")
        elif json_message['message_type'] == 'group':
            msg = receiveGroupMessage(json_message)
            logger.info(f"Group message in {msg.group_id} from {msg.user_id}: {msg.message}")
        else:
            logger.warning(f"Unknown message type: {json_message['message_type']}")
    elif json_message['post_type'] == 'meta_event':
        pass
    else:
        logger.warning(f"Unknown post type: {json_message['post_type']}")
    return


async def receive_messages():
    logger.info("Receiving messages...")
    ## send的时候也许可以复用这个连接
    async with websockets.connect(settings.ws_url) as websocket:
        while True:
            raw_msg = await websocket.recv()
            data = json.loads(raw_msg)
            logger.debug(f"Received message: {data}")
            parse_ws_mesage(data)

async def send_private_message(user_id: int, message: str):
    async with websockets.connect(settings.ws_url) as websocket:
        msg = sendPrivateMessage(user_id, message)
        await websocket.send(json.dumps(msg.__dict__))
        logger.info(f"Sent private message to {user_id}: {message}")

async def send_group_message(group_id: int, message: str):
    async with websockets.connect(settings.ws_url) as websocket:
        msg = sendGroupMessage(group_id, message)
        await websocket.send(json.dumps(msg.__dict__))
        logger.info(f"Sent group message to {group_id}: {message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QQ CLI Tool")
    parser.add_argument("--msg", type=str, help="Message to send")
    parser.add_argument("--user", type=int, help="User ID to send message to")
    parser.add_argument("--group", type=int, help="Group ID to send message to")
    parser.add_argument("--receive", type=bool, help="Receive messages", default=False)

    args = parser.parse_args()

    if args.receive:
        asyncio.run(receive_messages())
    elif args.msg and args.user:
        asyncio.run(send_private_message(args.user, args.msg))
    elif args.msg and args.group:
        asyncio.run(send_group_message(args.group, args.msg))
    else:
        logger.error("Invalid arguments. Use --help for more information.")
        pass