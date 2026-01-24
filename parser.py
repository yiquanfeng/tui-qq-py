from textual import log
from message import internalMessage
from typing import List

async def parse_ws_message(json_message: dict) -> List[internalMessage] | None:
    msgs = []
    if 'post_type' in json_message:
        if json_message.get('post_type') == 'message':
            sender = json_message['sender']['nickname']
            data = ""
            for msg in json_message.get('message', []):
                type = msg.get('type')
                if type == 'text':
                    text_msg = msg['data']['text']
                    log(f"Received text message: {text_msg}")
                    data = text_msg
                elif type == 'image':
                    image_url = msg['data'].get('url')
                    image_name = msg['data'].get('file')
                    await downloader(image_url, 'image', image_name)
                    data = f"imgs/{image_name}"
                    log(f"Received image message: {image_url}")
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
                    log(f"Unknown message type: {type}")
                msgs.append(internalMessage(type, data, sender))
            return msgs   

        elif json_message['post_type'] == 'meta_event':
            log("this is a meta event")
            return None
        elif json_message['post_type'] == 'message_sent':
            log("message sent event")
            return None
        elif json_message['post_type'] == 'notice':
            log("this is a notice event")
            return None
    ## response message
    elif 'retcode' in json_message:
        if 'messages' in json_message.get('data', {}):
            for mesgs in json_message.get('data', {}).get('messages', []):
                sender = mesgs.get('sender', {}).get('nickname', 'unknown')
                for msg in mesgs.get('message', []):
                    type = msg.get('type')
                    data = ""
                    if type == 'text':
                        text_msg = msg['data']['text']
                        log(f"Received history text message: {text_msg}")
                        data = text_msg
                    elif type == 'image':
                        image_url = msg['data'].get('url')
                        image_name = msg['data'].get('file')
                        await downloader(image_url, 'image', image_name)
                        data = f"imgs/{image_name}"
                        log(f"Received history image message: {image_url}")
                    else:
                        log(f"Unknown history message type: {type}")
                msgs.append(internalMessage(type, data, sender))
        return msgs
    else:
        log(f"Unknown post_type: {json_message}")
        return None
    
async def downloader(url: str, type: str, file_name: str):
    import aiohttp
    import aiofiles
    save_path = f"imgs/{file_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    f = await aiofiles.open(save_path, mode='wb')
                    await f.write(await response.read())
                    await f.close()
                    log(f"Downloaded file from {url} to {save_path}")
                else:
                    log(f"Failed to download file from {url}. Status code: {response.status}")
        return save_path
    except Exception as e:
        log(f"Exception occurred while downloading file from {url}: {e}")
        return None