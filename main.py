import asyncio
import pkgutil

from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    config,
)

from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.scheduler import GraiaScheduler
from graia.scheduler.saya import SchedulerSchema, GraiaSchedulerBehaviour

loop = asyncio.new_event_loop()
bcc = Broadcast(loop=loop)
Ariadne.config(loop=loop, broadcast=bcc)
scheduler1 = GraiaScheduler(loop=loop, broadcast=bcc)
app = Ariadne(
    connection=config(
        114514,  # 你的机器人的 qq 号
        "114514",  # 填入 verifyKey
        # 以下两行是你的 mirai-api-http 地址中的地址与端口
        # 默认为 "http://localhost:8080" 如果你没有改动可以省略这两行
    ),
)
saya = app.create(Saya)
saya.install_behaviours(
    app.create(BroadcastBehaviour),
    GraiaSchedulerBehaviour(scheduler1)
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require(f"modules.{module_info.name}")

app.launch_blocking()
