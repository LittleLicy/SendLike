from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived
import aiohttp
import os

"""
在收到私聊或群聊消息"赞我"时，自动点赞用户名片
"""

# 注册插件
@register(name="AutoLike", description="自动点赞用户名片[开发]", version="0.1", author="笨笨")
class AutoLikePlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.host = host
        self.api_base_url = os.getenv("ONEBOT_API_URL", "http://localhost:3000") #llonebot默认http端口3000

    async def initialize(self):
        pass

    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        if msg.startswith("赞我"):
            sender_id = ctx.event.sender_id
            await self.send_like(sender_id, times=10)  # 设定点赞次数为10
            ctx.add_return("reply", ["已经为你点赞了10次，记得回赞捏~"])
            ctx.prevent_default()
        if msg.startswith("超我"):
            sender_id = ctx.event.sender_id
            await self.send_like(sender_id, times=10)  # 设定点赞次数为10
            ctx.add_return("reply", ["已经为你超了10次，记得回赞捏~"])
            ctx.prevent_default()

    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        if msg.startswith("赞我"):
            sender_id = ctx.event.sender_id
            await self.send_like(sender_id, times=10)  # 设定点赞次数为10
            ctx.add_return("reply", ["已经为你点赞了10次，记得回赞捏~"])
            ctx.prevent_default()
        if msg.startswith("超我"):
            sender_id = ctx.event.sender_id
            await self.send_like(sender_id, times=10)  # 设定点赞次数为10
            ctx.add_return("reply", ["已经为你超了10次，记得回赞捏~"])
            ctx.prevent_default()

    async def send_like(self, user_id, times=1):
        payload = {
            "user_id": user_id,
            "times": times  # 正确传递 times 参数
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.api_base_url}/send_like", json=payload) as response:
                    if response.status == 200:
                        self.ap.logger.info(f"成功为用户 {user_id} 点赞 {times} 次！")
                    else:
                        error_data = await response.json()
                        self.ap.logger.error(f"点赞失败，状态码: {response.status}, 错误信息: {error_data}")
            except aiohttp.ClientError as e:
                self.ap.logger.error(f"网络请求失败: {e}") #如果你的监听端口不正确的话

    def __del__(self):
        pass
