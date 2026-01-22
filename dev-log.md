## 1. 开发一个cli的后端版本
先写后端，因为前端的框架如果切换语言的化，实现起来会有很大的不同  
但是后端的逻辑十分相似。使用cli的化，可以最大程度摆脱图形化的困扰  
实现可用性
cli的开发太过于顺利，应该是官网的东西比较现成导致的

## 2. 基本前端和后端结合


## 发布计划
计划把群组列表，获取消息历史，发送图片这三个功能完善之后，发布0.0.1版本
之后的事情就再说

# Textual example解析
1. dictionary
这个实例我觉得写的真不错

## extra
在公司尝试使用最新版napcat部署应用的时候，发现一些不方便使用的点
1. 没有requirements.txt ，记得还有pyhon socket包
2. 新版napcat强制需要token验证，需要在header里面添加

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