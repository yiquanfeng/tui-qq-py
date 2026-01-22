from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import VerticalScroll, Vertical, Horizontal
from textual_image.widget import Image
from qq_cli import QQClient
from settings import settings
import asyncio
from textual import log


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

    def compose(self) -> ComposeResult:
        self.message_container = VerticalScroll()
        with self.message_container:
            yield Static("Chatting with Spriple")
        yield Input(placeholder="Type your message here...", type="text", id="message_input")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        message = event.value
        if not message.strip():
            return
        event.input.value = ""
        # 显示自己发送的消息
        await self.message_container.mount(ChatView(sender="me", text=message, image_path=None))
        
        # 异步发送，不阻塞 UI 或 listen 任务
        asyncio.create_task(self.client.send_private(user_id=1572087810, message=message))
        # self.message_container.scroll_end(animate=False)

    async def append_message(self, msg):
        """回调函数，用于接收新消息并渲染到 UI"""
        if msg['type'] == 'text':
            log(f"Appending text message: {msg['resource']}")
            await self.message_container.mount(ChatView(sender=msg['sender'], text=msg['resource'], image_path=None))
        elif msg['type'] == 'image':
            log(f"Appending image message: {msg['resource']}")
            await self.message_container.mount(ChatView(sender=msg['sender'], text=None, image_path=msg['resource']))
        # self.message_container.scroll_end(animate=False)

    async def on_mount(self) -> None:
        self.client = QQClient(ws_url=settings.ws_url, token=settings.token)
        asyncio.create_task(self.client.listen(callback=self.append_message))

if __name__ == "__main__":
    app = QQApp()
    app.run()