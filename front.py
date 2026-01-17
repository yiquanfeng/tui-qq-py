from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog
from qq_cli import test_send, receive_messages
import asyncio


class QQApp(App):
    
    def compose(self) -> ComposeResult:
        yield RichLog(id="chat_log", highlight=True, markup=True)
        yield Input(placeholder="Type your message here...", type="text", id="message_input")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        message = event.value
        event.input.value = ""
        # 显示自己发送的消息
        self.query_one("#chat_log", RichLog).write(f"[bold green]Me:[/bold green] {message}")
        await test_send(message)

    def append_message(self, msg):
        """回调函数，用于接收新消息并渲染到 UI"""
        chat_log = self.query_one("#chat_log", RichLog)
        if hasattr(msg, 'group_id'):
            chat_log.write(f"[bold blue]Group {msg.group_id}[/bold blue] | [bold yellow]{msg.sender['nickname']}:[/bold yellow] {msg.message[0]['data']['text']}")
        else:
            chat_log.write(f"[bold magenta]Private {msg.sender['nickname']}:[/bold magenta] {msg.message[0]['data']['text']}")

    async def on_mount(self) -> None:
        # 在后台启动监听任务，并传入 UI 更新的回调
        asyncio.create_task(receive_messages(on_message_callback=self.append_message))

if __name__ == "__main__":
    app = QQApp()
    app.run()