import hoshino
from hoshino import Service, priv
from hoshino import aiorequests
import aiocqhttp
import asyncio
import os

sv = Service(
    name='ewu',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=False,  # 是否默认启用
)

latest_path = os.path.join(os.path.dirname(__file__), 'latest.txt')

@sv.scheduled_job('cron',second='*/30')
async def ewubattle():
    # 获取消息
    url = "https://interface.sina.cn/wap_api/common_timeline.d.json?url=mcwiwss2660206"
    res = await aiorequests.get(url)
    result = await res.json()
    result = result['result']
    # print(result['data']['data'][0])
    one = result['data']['data'][0]
    time = one['title']
    report = one['item']['info']['title']

    # 读最新
    with open(latest_path, 'r', encoding='utf-8') as latest:
        latest = latest.read()
    if report == latest:
        return

    # 发送
    url = one['item']['base']['base']['url']
    img_url = []
    # print(time, report, url)
    bot = hoshino.get_bot()
    glist_info = await sv.get_enable_groups()
    for each_g in glist_info:
        await asyncio.sleep(1.5)
        gid = each_g
        try:
            for one_im in one['item']['info']['covers']:
                img_url.append(one_im['url'])
            img = f"[CQ:image,file={img_url[0]}]"
        except:
            img = {}

        try:
            await bot.send_group_msg(group_id=gid, message=f"关注俄乌战争：\n{time}\n{report}\n{img}\n{url}")
        except:  # 可能风控
            try:
                await bot.send_group_msg(group_id=gid, message=f"关注俄乌战争：{time}\n{report}\n{url}")
            except:  # 可能风控
                await bot.send_group_msg(group_id=gid, message=f"关注俄乌战争：{time}\n{report}")
    
    # 写最新
    with open(latest_path, 'w', encoding='utf-8') as latest:
        latest.write(report)
