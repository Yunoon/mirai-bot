import random

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
from graia.ariadne.model import Group, Member

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler import timers

from graia.scheduler.saya import SchedulerSchema

channel = Channel.current()


@channel.use(SchedulerSchema(timers.crontabify("1 * * * *")))
async def clear_jrrp(app: Ariadne):
    file = open('jrrp.txt', 'w')
    file.write("1|2\n")

