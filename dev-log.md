## log
计划把群组列表，获取消息历史，发送图片这三个功能完善之后，发布0.0.1版本
之后的事情就再说
2025.1.22
开发好了既可以塞图片和文字的聊天窗口
![alt text](./image-and-text.png)

需要确定前后端通信的协议
前段只需要知道消息是什么，该如何渲染即可
| data_type | text | imgae | at | reply | face | mface | dice | rps | poke | record | video | file | json | music | forward |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
| data | pure_text | image_path | "qqid,all" | id | id | {emoji_id, emoji_pack_id, key} | 

sender: nickname



## bugs
1. front运行时出现不存在的消息和日志系统不兼容问题
```
Received message: {'status': 'ok', 'retcode': 0, 'data': {'message_id': 947845524}, 'message': '', 'wording': '', 'echo': 'no use?', 'stream': 'normal-action'}
[23:24:08] INFO                                                                                                                                                                                 qq_cli.py:49
Error processing message: 'post_type'
```
目前只能在listen中添加try机制
```
try:
    data = json.loads(message)
    log(f"Received message: {data}")
    parse_data = await parse_ws_message(data)
    if callback and parse_data:
        log("Calling back with parsed data.")
        await callback(parse_data)
except Exception as e:
    log(f"Error processing message: {e}")
    # 继续循环，不要因为一条消息解析失败就断开监听
```
并且现在textual的日志报错和我需要使用logger调试的日志系统并不兼容，这让我有点烦

搞明白了，今天在折腾获取消息历史的时候，发送消息之后websocket服务器会有回复消息，格式就是上面的奇怪的消息。
我当时觉得它奇怪是因为，我同时开了另外一个进程连接同一个websocket服务器，我觉得websocket应该会广播这个消息，但是没有
只会发给发起请求的那个进程，哈哈，原来是我socket通信没学透，这里每一个连接在服务器端都会创造一个socket来区分不同的连接
所以我的listen函数，除了解析message和message sent，meta之外，还要解析请求的回传