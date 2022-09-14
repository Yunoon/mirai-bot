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


def share_info():
    message = ""
    speach_list = ["Name|114514"]

    with open("speach.txt", "r") as file:
        current_list = file.read().split("|")
        current_week = int(current_list[0])  # 1
        current_person = int(current_list[1])  # 1
        file.close()

    message += ("=" * 10 + f"第{current_week}次分享" + "=" * 10 + "\n")
    current_week += 1

    flag = int(current_person) % 13
    message += ("分享人：" + speach_list[flag - 1].split("|")[0] + "、" + speach_list[flag].split("|")[0] + "\n")

    with open('speach.txt', 'w') as file:
        file.write(str(current_week) + "|" + str(current_person + 2))
        file.close()
    return message, speach_list[flag - 1].split("|")[1], speach_list[flag].split("|")[1]



# 定时任务
group_id = 114514  # 要定时发送消息的群号


# @channel.use(SchedulerSchema(timers.crontabify("30 18 * * 6,0")))
@channel.use(SchedulerSchema(timers.crontabify("* * * * * *")))
async def morning(app: Ariadne):
    messages, person_1, person_2 = share_info()

    await app.send_group_message(
        group_id,
        MessageChain(messages, At(target=int(person_1)), At(target=int(person_2)))
    )
