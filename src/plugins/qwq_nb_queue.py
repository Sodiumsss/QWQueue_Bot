import re

from nonebot import on_regex
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, PrivateMessageEvent
from nonebot.adapters.console import Event as ConsoleEvent
from nonebot.typing import T_State

from src.libraries.qwq_function import *

__plugin_meta__ = PluginMetadata(
    name="QWQueue",
    description="机厅排队插件",
    usage="输入 '机厅几' 查询所有机厅"
    )

alias_set = {
    '王者', '农', 'n','星河', '盒','h','万象汇', '汇','酷咔库','库','k','酷玩猩球', '猩球', '提','t','爱琴海', '海','迪卡丘'
}
game_set={10006,10043,10044,10045,10046}
place_map = {
    '王者之风':10006,
    '迪卡丘':10043,
    '酷咔库':10044,
    '酷玩猩球':10045,
    '游戏大魔方（爱琴海）':10046,
}
alias_map={}
alias_map.update(dict.fromkeys(['王者', '农', 'n'], 10006))
alias_map.update(dict.fromkeys(['迪卡丘','星河', '盒','h'], 10043))
alias_map.update(dict.fromkeys(['万象汇', '汇','酷咔库','库','k'], 10044))
alias_map.update(dict.fromkeys(['酷玩猩球', '猩球', '提','t'], 10045))
alias_map.update(dict.fromkeys(['爱琴海', '海'], 10046))


def find_alias(text):
    for i in range(len(text), 0, -1):
        prefix = text[:i]
        if prefix in alias_set:
            return prefix
    return None

def alias_mapper(alias):
    a_lower=alias.lower()
    if a_lower in alias_map:
        return alias_map[a_lower]
    
async def game_add(id,count):
    #TODO
    return

async def game_minus(id,count):
    #TODO
    return

async def game_query(id):
    payload={"gameId":id}
    r=await getGamePlayer(payload)
    if r['code']==-1:
        return f"暂无数据/无人上报"
    elif r['code']==0:
        if r['message']=="waiting":
            return f"正在更新，请稍后查询"
        else:
            return f"gameID不正确，请联系管理员"
    else:
        return "当前人数："+str(r['data']['player'])+"人\n上报时间："+str(r['data']['time']).replace("T"," ")

async def game_modify(id,count):
    if count>20:
        return "人数不能超过20人"
    elif count<0:
        return "人数不能小于0"
    payload={"gameId":id,"player":count}
    r=await setGamePlayer(payload)
    if r['code']==0:
        if r['message']=="waiting":
            return f"正在更新，请稍后查询"
        elif r['message']=="size":
            return f"这人数对吗"
        else:
            return f"gameID不正确，请联系管理员"
    elif r['code']==1:
        return f"更新成功，当前人数为{count}人"
    return

async def query_all_games():
    """查询所有机厅的人数和更新时间"""
    results = []
    for game_id in sorted(game_set):  # 按游戏ID排序
        try:
            payload = {"gameId": game_id}
            r = await getGamePlayer(payload)
            
            # 获取对应的地点名称
            place = next(place for place, id in place_map.items() if id == game_id)
            
            if r['code'] == 1:  # 成功获取数据
                # 处理时间格式 (原格式类似 "2024-03-19T12:34:56")
                time_str = r['data']['time'].split('T')[1][:8]  # 提取 HH:MM:SS
                results.append(f"{place}: {r['data']['player']}人 ({time_str})")
            elif r['code'] == -1:  # 无数据
                results.append(f"{place}: 暂无数据")
            elif r['code'] == 0 and r['message'] == "waiting":
                results.append(f"{place}: 更新中")
            else:
                results.append(f"{place}: 查询失败")
                
        except Exception as e:
            print(f"查询 游戏ID {game_id} 时出错: {e}")
            results.append(f"游戏ID {game_id}: 查询失败")
    
    return "\n".join(results) if results else "暂无数据"

async def parse_command(text):
    """解析指令并返回操作结果"""
    # 先找到地点别名
    if re.match(r'^(机厅|jt)(几|j|几人)$', text):
        print("识别为查询所有机厅")
        return await query_all_games()
    place = find_alias(text)
    
    if not place:
        return None
    
    # 剩余部分作为操作指令
    remainder = text[len(place):].strip()
    
    # 处理查询指令
    if remainder in ['几', 'j', '几人']:
        game_id = alias_map[place]
        return await game_query(game_id)
    
    # 处理数字指令
    match = re.match(r'([+-]?)(\d+)$', remainder)
    
    if match:
        sign, number = match.groups()
        people = int(number)
        
        game_id = alias_map[place]
        
        if sign == '+':
            return await game_add(game_id, people)
        elif sign == '-':
            return await game_minus(game_id, people)
        else:
            return await game_modify(game_id, people)
    return None

queue_cmd = on_regex(
    r'^(?:(?P<place>h|海|王者|农|n|迪卡丘|星河|盒|万象汇|汇|酷咔库|库|k|酷玩猩球|猩球|提|t|爱琴海)\s*'
    r'(?:(?P<query_people>几|j)|(?P<sign>[+-]?)?\s*(?P<people>\d+))?'
    r'|(?:机厅|jt)(?:几|j|几人))$'
)

@queue_cmd.handle()
async def handle_queue(event: GroupMessageEvent|PrivateMessageEvent|ConsoleEvent, state: T_State):
    text = event.get_plaintext()
    #text = event.get_message().extract_plain_text()  # 获取控制台输入的文本
    # 查询所有机厅
    if text.startswith(('机厅', 'jt')):
        result = await query_all_games()
        await queue_cmd.finish(result)
        return
    
    # 查找地点别名
    place = find_alias(text)
    if not place:
        await queue_cmd.finish()
        return
    
    # 获取剩余部分作为操作指令
    remainder = text[len(place):].strip()
    
    # 处理查询指令
    if remainder in ['几', 'j', '几人']:
        game_id = alias_map[place]
        result = await game_query(game_id)
        await queue_cmd.finish(result)
        return
    
    # 处理数字指令
    match = re.match(r'([+-]?)(\d+)$', remainder)
    if match:
        sign, number = match.groups()
        people = int(number)
        game_id = alias_map[place]
        
        if sign == '+':
            result = await game_add(game_id, people)
        elif sign == '-':
            result = await game_minus(game_id, people)
        else:
            result = await game_modify(game_id, people)
            
        await queue_cmd.finish(result)
        return
    
    await queue_cmd.finish()
