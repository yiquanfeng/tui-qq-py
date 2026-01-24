from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual_image.widget import Image
from qq_cli import QQClient
from settings import settings
import asyncio
from textual import log
from message import internalMessage

class ChatView(Static):
    def __init__(self, sender: str, text: str | None, image_path:str | None, **kwargs):
        super().__init__(**kwargs)
        self._sender = sender
        self._text = text
        self._image_path = image_path

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static(f"{self._sender}: ")
            with Vertical():
                if self._text:
                    yield Static(self._text)
                if self._image_path:
                    log(f"Rendering image at path: {self._image_path}")
                    yield Image(image=self._image_path, classes="small-image")

class QQApp(App):
    CSS_PATH = "styles.css"
    now_place = {
        "type": "private",
        "id": 1572087810
    }

    def compose(self) -> ComposeResult:
        self.message_container = VerticalScroll()
        with self.message_container:
            yield Static(f"Chatting with {self.now_place['id']}")
        yield Input(placeholder="Type your message here...", type="text", id="message_input").focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        message = event.value
        if not message.strip():
            return
        event.input.value = ""
        if message == "/change":
            
            await self.change_place("group", 1055065019)
            return
        # 显示自己发送的消息
        await self.message_container.mount(ChatView(sender="me", text=message, image_path=None))
        
        # send message according to now_place
        if self.now_place["type"] == "group":
            asyncio.create_task(self.client.send_group(group_id=self.now_place["id"], message=message))
        elif self.now_place["type"] == "private":
            asyncio.create_task(self.client.send_private(user_id=self.now_place["id"], message=message))
        else:
            log(f"Unknown chat type: {self.now_place['type']}")
        self.message_container.scroll_end(animate=True)

    async def change_place(self, new_type: str, new_id: int) -> None:
        self.now_place = {
            "type": new_type,
            "id": new_id
        }
        # 更新标题
        for widget in self.message_container.children:
            await widget.remove()
        await self.message_container.mount(Static(f"{self.now_place['type'].capitalize()}, Chatting with {self.now_place['id']}"))
        await self.client.get_history(type=self.now_place["type"], id=self.now_place["id"], count=10)

    async def append_message(self, msgs: list[internalMessage]) -> None:
        """回调函数，用于接收新消息并渲染到 UI"""
        for msg in msgs:
            if msg.type == 'text':
                log(f"Appending text message: {msg.data}")
                await self.message_container.mount(ChatView(sender=msg.sender, text=msg.data, image_path=None))
            elif msg.type == 'image':
                log(f"Appending image message: {msg.data}")
                await self.message_container.mount(ChatView(sender=msg.sender, text=None, image_path=msg.data))
        self.message_container.scroll_end(animate=True)

    async def on_mount(self) -> None:
        self.client = QQClient(ws_url=settings.ws_url, token=settings.token)
        ## 防止在获取历史消息时还未连接成功
        await self.client.connect()
        asyncio.create_task(self.client.listen(callback=self.append_message)) 
        await self.client.get_history(type=self.now_place["type"], id=self.now_place["id"], count=10)

if __name__ == "__main__":
    app = QQApp()
    app.run()