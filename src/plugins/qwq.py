import re

from nonebot import on_regex
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import EventMessage

from src.libraries.maimaidx_music import *
from src.libraries.qwq_function import *

qwqQQ = on_regex(r"qwq验证.*")
@qwqQQ.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        payload = {"username": re.match("验证(.*)", str(message)).groups()[0], 'qq': event.get_user_id()}
        response = await verifyQQ(payload)
        await qwqQQ.send(response.getMessage())
    except Exception as e:
        print(e)
        await qwqQQ.send("指令实现过程出错，请联系管理员。")


getSongIDName = on_regex(r"是什么歌$")


@getSongIDName.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        aliasName = re.match("(.*)(是什么歌)$", str(message)).groups()[0]
        payload = {"text": aliasName}
        response: list = await getSongByAlias(payload)
        listLen = len(response)
        if listLen == 0:
            await getSongIDName.send("没有歌曲拥有此别称！")
        elif listLen == 1:
            # 调用自己的函数，生成并输出歌曲图片
            songId = str(response[0]['songId'])
            songPhoto = "这是一张ID为" + songId + "叫做" + total_list.by_id(songId).title + "的歌曲的图片！"
            #

            await getSongIDName.send(songPhoto)
        else:
            myStr = "以下是拥有\"" + aliasName + "\"别称的歌曲：\n"
            for i in response:
                myStr += "ID：" + str(i['songId']) + ",歌曲名：《" + total_list.by_id(str(i['songId'])).title + "》\n"
            await getSongIDName.send(myStr)
    except Exception as e:
        print(e)
        await getSongIDName.send("指令实现过程出错，请联系管理员。")

addAlias = on_regex(r"添加别称 [0-9]* .*")


@addAlias.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        inf = re.match("(添加别称) ([0-9]*) (.*)$", str(message)).groups()
        songID = inf[1]
        alias = inf[2]
        if len(songID) > 5:
            # 不存在这样的歌曲ID，直接忽略请求
            return
        if len(alias) < 2:
            await addAlias.send("别称长度需要大于等于2。")
            return
        payload = {"songId": songID, "text": alias}
        r = await addSongAlias(payload)
        if r['code'] == 1:
            await addAlias.send("添加成功。")
        else:
            if r['message'] == "added":
                await addAlias.send("添加失败。\n原因：该歌曲已经拥有此别称。")
            else:
                # 可以自己多自定义几段话
                await addAlias.send("添加失败。")

    except Exception as e:
        print(e)
        await addAlias.send("指令实现过程出错，请联系管理员。")


getSongAlias = on_regex(r"有什么别称$")
@getSongAlias.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        songId = re.match("(.*)(有什么别称$)$", str(message)).groups()[0]
        payload = {"songId": songId}
        r:list = await getSongAliases(payload)
        if len(r)==0:
            await getSongAlias.send("它好像没有别称，输入：\n添加别称 "+songId+" 哈哈哈哈哈\n来为它增加一个别称吧！")
        else:
            myStr = "《" + total_list.by_id(songId).title + "》拥有以下别称：\n"
            for index, s in enumerate(r):
                # (该歌曲的别称下标).别称( (别称ID) )
                myStr += str(index + 1) + "." + s['text'] + "(" + str(s['id']) + ")" + "\n"
            await getSongAlias.send(myStr)

    except Exception as e:
        print(e)
        await getSongAlias.send("指令实现过程出错，请联系管理员。")


#接受别称ID
deleteSongAlias = on_regex("删除别称 [0-9]*")
@deleteSongAlias.handle()
async def _(event: Event, message: Message = EventMessage()):
    #建议建一个能够删除别称的QQ表
    qq = event.get_user_id()

    try:
        aliasId = re.match("(删除别称) ([0-9]*)$", str(message)).groups()[1]
        payload={'id':aliasId}
        state = await deleteAliasByID(payload)
        if state:
            await deleteSongAlias.send("删除成功。")
        else:
            await deleteSongAlias.send("删除失败。")
    except Exception as e:
        print(e)
        await deleteSongAlias.send("指令实现过程出错，请联系管理员。")
