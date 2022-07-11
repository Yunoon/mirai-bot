import random

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
from graia.ariadne.model import Group, Member

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain, member: Member):
    """

    :param app:
    :type app:
    :param group:
    :type group:
    :param message:
    :type message:
    :param member:
    :type member:
    :return:
    :rtype:
    """
    if str(message) == "jrrp":

        # 利用读取写入文件的方式来记录，主要是懒，不想连数据库。
        file_list = open("jrrp.txt", 'r').read().split("\n")  # 取出文件中所有的内容
        jrrp_list = [i.split("|") for i in file_list][:-1]  # 处理数据

        # 判断用户是否已查询今日运势
        for i in jrrp_list:
            # 存在的话直接发送数据后，返回即可
            if i[1] == str(member.id):
                luck_num = i[0]
                await app.send_message(
                    group,
                    MessageChain(f"您今日的运势为：{luck_num}/100", At(member.id)),
                )
                return

        # 打开文件进行追加
        file_write = open("jrrp.txt", 'a')
        # 随机获取(虽然是伪随机)
        luck_num = random.randint(0, 100)
        # 写入时末尾添加换行，为了处理数据。
        file_write.write(str(luck_num) + "|" + str(member.id) + "\n")
        file_write.close()
        await app.send_message(
            group,
            MessageChain(f"您今日的运势为：{luck_num}/100", At(member.id)),
        )
