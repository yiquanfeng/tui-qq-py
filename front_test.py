from textual_image.widget import Image
from textual.containers import Vertical, VerticalScroll
from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual import on


class MessageWidget(Static):
    """自定义消息 Widget，包含文本和可选的图片"""

    def __init__(self, text: str, image_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._text = text
        self._image_path = image_path

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(self._text)
            if self._image_path:
                yield Image(image=self._image_path, classes="small-image")



class test(App):
    CSS_PATH = "styles.css"

    def compose(self) -> ComposeResult:
        self.message_container = VerticalScroll()
        with self.message_container:
            yield MessageWidget(
                "Hello, this is a test message with an image and a video.",
                image_path="./imgs/946CBACF42B4BB947C9EF1ABC131564A.jpg"
            )
        yield Input(placeholder="Type here...", type="text")
    

if __name__ == "__main__":
    test().run()
