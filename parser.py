from message import receivePrivateMessage, receiveGroupMessage
from loguru import logger

async def parse_ws_mesage(json_message: dict):
    msg = None
    if json_message.get('post_type') == 'message':
        if json_message['message_type'] == 'private':
            msg = receivePrivateMessage(json_message)
        elif json_message['message_type'] == 'group':
            msg = receiveGroupMessage(json_message)
        type = msg.message[0]['type']
        if type == 'text':
            text_msg = msg.message[0]['data']['text']
            logger.info(f"Received text message: {text_msg}")
        elif type == 'image':
            image_url = msg.message[0]['data'].get('url')
            image_name = msg.message[0]['data'].get('file')
            await downloader(image_url, 'image', image_name)
            logger.info(f"Received image message: {image_url}")
        elif type == 'at':
            pass
        elif type == 'reply':
            pass
        elif type == 'face':
            pass
        elif type == 'mface':
            pass
        elif type == 'dice':
            pass
        elif type == 'rps':
            pass
        elif type == 'poke':
            pass
        elif type == 'record':
            pass
        elif type == 'video':
            pass
        elif type == 'file':
            pass
        ## 卡片消息
        elif type == 'json':
            pass
        elif type == 'music':
            pass
        elif type == 'forward':
            pass
        else:
            logger.info(f"Unknown message type: {type}")
        return msg
    elif json_message['post_type'] == 'meta_event':
        logger.info("this is a meta event")
        return None
    elif json_message['post_type'] == 'message_sent':
        logger.info("message sent event")
        return None
    
async def downloader(url: str, type: str, file_name: str):
    import aiohttp
    import aiofiles
    import time
    save_path = f"imgs/{file_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    f = await aiofiles.open(save_path, mode='wb')
                    await f.write(await response.read())
                    await f.close()
                    logger.info(f"Downloaded file from {url} to {save_path}")
                else:
                    logger.error(f"Failed to download file from {url}. Status code: {response.status}")
        return save_path
    except Exception as e:
        logger.error(f"Exception occurred while downloading file from {url}: {e}")
        return None