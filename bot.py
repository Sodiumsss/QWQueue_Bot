import nonebot
from nonebot.adapters.onebot.v11 import Adapter
nonebot.init()
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
driver.config.help_text = {}
nonebot.load_plugins("src/plugins")
if __name__ == "__main__":
    nonebot.run()
