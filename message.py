from typing import Dict

class receivePrivateMessage:
    def __init__(self, data: Dict):
        self.time = data["time"]
        self.post_type = data["post_type"]
        self.message_type = data["message_type"]
        self.sub_type = data["sub_type"]
        self.message_id = data["message_id"]
        self.user_id = data["user_id"]
        self.message = data["message"]
        self.raw_message: str = data["raw_message"]
        self.font = data["font"]
        self.sender: Dict = data["sender"]
        self.self_id = data["self_id"]

class receiveGroupMessage(receivePrivateMessage):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.group_id = data["group_id"]


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
        