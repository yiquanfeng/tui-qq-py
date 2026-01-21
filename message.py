from typing import Dict, List

class receivePrivateMessage:
    def __init__(self, data: Dict):
        self.time: int = data["time"]
        self.post_type: str = data["post_type"]
        self.message_type: str = data["message_type"]
        self.sub_type: str = data["sub_type"]
        self.message_id: int = data["message_id"]
        self.user_id: int = data["user_id"]
        self.message: List[Dict] = data["message"]
        self.raw_message: str = data["raw_message"]
        self.font: int = data["font"]
        self.sender: Dict = data["sender"]
        self.self_id: int = data["self_id"]

class receiveGroupMessage(receivePrivateMessage):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.group_id: int = data["group_id"]


class sendWSMessage:
    def __init__(self, action: str, id: int, messgae: str):
        self.action = action
        self.params = {
            "id": id,
            "message": messgae
        }
        self.echo = "no use?"

class sendPrivateMessage(sendWSMessage):
    def __init__(self, user_id: int, message: str):
        super().__init__("send_private_msg", user_id, message)
        self.params = {
            "user_id": user_id,
            "message": message
        }

class sendGroupMessage(sendWSMessage):
    def __init__(self, group_id: int, message: str):
        super().__init__("send_group_msg", group_id, message)
        self.params = {
            "group_id": group_id,
            "message": message
        }
        