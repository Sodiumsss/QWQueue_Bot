import re

from nonebot import on_regex
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import EventMessage

from src.libraries.maimaidx_music import *
from src.libraries.qwq_function import *

#根据游戏ID获取人数，可以前往网站的“机厅”中查看具体的游戏ID
getGP=on_regex(r"(吾悦麦麦)$")
@getGP.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        payload = {"gameId":1003}
        r= await getGamePlayer(payload)
        if r['code']==-1:
            await getGP.send("没人上报，似乎没有人！")
        elif r['code']==0:
            if r['message']=="waiting":
                await getGP.send("当前人数正在变动，请稍后查询！")
            else:
                print("你的gameId不正确。")
        else:
            await getGP.send("当前人数："+str(r['data']['player'])+"人\n上报时间："+str(r['data']['time']).replace("T"," "))

    except Exception as e:
        print(e)
        await getGP.send("指令实现过程出错，请联系管理员。")

incGPS=on_regex(r"^(吾悦麦麦加)([0-9][0-9]?)")
@incGPS.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        inf =re.match("^(吾悦麦麦加)([0-9][0-9]?)", str(message)).groups()
        player = int(inf[1])
        if player <0:
            await setGP.send("人数小于了0人，有鬼！")
            return
        payload = {"gameId":1003,"player":player}
        r= await incGamePlayers(payload)
        if r['code']==0:
            if r['message']=="waiting":
                await incGPS.send("当前人数正在变动，请稍后再发出指令！")
            elif r['message']=="size":
                await incGPS.send("人数不太对吧！")
            else:
                print("你的gameId不正确。")
        elif r['code']==1:
            await incGPS.send("成功更改，当前人数："+str(r['data']['player'])+"人")

    except Exception as e:
        print(e)
        await incGPS.send("指令实现过程出错，请联系管理员。")

incGP=on_regex(r"(吾悦麦麦\+\+)$")
@incGP.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        payload = {"gameId":1003}
        r= await incGamePlayer(payload)
        if r['code']==0:
            if r['message']=="waiting":
                await incGP.send("当前人数正在变动，请稍后再发出指令！")
            elif r['message']=="size":
                await incGP.send("人数超过了20人，真的有这么多吗！")
            else:
                print("你的gameId不正确。")
        else:
            await incGP.send("成功增加，当前人数："+str(r['data']['player'])+"人")
    except Exception as e:
        print(e)
        await incGP.send("指令实现过程出错，请联系管理员。")

decGP=on_regex(r"(吾悦麦麦\-\-)$")
@decGP.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        payload = {"gameId":1003}
        r= await decGamePlayer(payload)
        if r['code']==0:
            if r['message']=="waiting":
                await decGP.send("当前人数正在变动，请稍后再发出指令！")
            elif r['message']=="size":
                await decGP.send("当前没有人游玩，不能再减了！")
            else:
                print("你的gameId不正确。")
        elif r['code']==1:
            await decGP.send("成功增加，当前人数："+str(r['data']['player'])+"人")
    except Exception as e:
        print(e)
        await decGP.send("指令实现过程出错，请联系管理员。")


setGP=on_regex(r"^(吾悦麦麦)([0-9][0-9]?)(人)")
@setGP.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        inf =re.match("^(吾悦麦麦)([0-9][0-9]?)(人)", str(message)).groups()
        player = int(inf[1])
        if player >20:
            await setGP.send("人数超过了20人，真的有这么多吗！")
            return
        elif player <0:
            await setGP.send("人数小于了0人，有鬼！")
            return
        payload = {"gameId":1003,"player":player}
        r= await setGamePlayer(payload)
        if r['code']==0:
            if r['message']=="waiting":
                await setGP.send("当前人数正在变动，请稍后再发出指令！")
            elif r['message']=="size":
                await setGP.send("人数不太对吧！")
            else:
                print("你的gameId不正确。")
        elif r['code']==1:
            await setGP.send("成功更改，当前人数："+str(r['data']['player'])+"人")

    except Exception as e:
        print(e)
        await setGP.send("指令实现过程出错，请联系管理员。")


qwqQQ = on_regex(r"qwq验证.*")
@qwqQQ.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        payload = {"username": re.match("(qwq验证)(.*)", str(message)).groups()[1], 'qq': event.get_user_id()}
        response = await verifyQQ(payload)
        await qwqQQ.send(response['message'])
    except Exception as e:
        print(e)
        await qwqQQ.send("指令实现过程出错，请联系管理员。")


getSongIDName = on_regex(r"是什么歌$")
@getSongIDName.handle()
async def _(event: Event, message: Message = EventMessage()):
    try:
        aliasName = re.match("(.*)(是什么歌)$", str(message)).groups()[0]
        payload = {"text": aliasName}
        response = await getSongByAlias(payload)
        songList =response['data']
        listLen = len(songList)
        if listLen == 0:
            await getSongIDName.send("没有歌曲拥有此别称！")
            return
        if response['code']==1:
            if listLen == 1:
                # 调用自己的函数，生成并输出歌曲图片
                songId = str(songList[0]['songId'])
                songPhoto = "这是一张ID为" + songId + "叫做" + total_list.by_id(songId).title + "的歌曲的图片！"
                #
                await getSongIDName.send(songPhoto)
            else:
                myStr = "以下是拥有\"" + aliasName + "\"别称的歌曲：\n"
                for i in songList:
                    myStr += "ID：" + str(i['songId']) + ",歌曲名：《" + total_list.by_id(str(i['songId'])).title + "》\n"
                await getSongIDName.send(myStr)
        elif response['code']==2:
            # 模糊搜索到了结果
            myStr = f"没有直接找到拥有\"{aliasName}\"别称的歌曲，以下是别称中含有\"" + aliasName + "\"文字的歌曲：\n"
            myAlias = dict()
            myID = dict()
            for i in songList:
                if myAlias.get(str(i['songId'])) is None:
                    myAlias[str(i['songId'])] = f"《{str(i['text'])}》"
                else:
                    myAlias[str(i['songId'])] += f",《{str(i['text'])}》"

            for i in songList:
                if myID.get(str(i['songId'])) is None:
                    myStr += "ID：" + str(i['songId']) + "\n歌曲名：《" + total_list.by_id(str(i['songId'])).title \
                             + f"》\n别称：{myAlias[str(i['songId'])]}\n\n"
                    myID[str(i['songId'])]=True

            await getSongIDName.send(myStr)
        else:
            await getSongIDName.send("指令实现过程出错，请联系管理员。")
    except Exception as e:
        print(f"异常{e}")
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
