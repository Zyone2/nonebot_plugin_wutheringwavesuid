import nonebot
from nonebot.config import Config


class LocalCoreConfig:
    def __init__(self):
        self._driver_config: Config | None = None

    @property
    def driver_config(self) -> Config:
        """
        延迟加载 Driver Config，确保 NoneBot 已初始化
        """
        if self._driver_config is None:
            try:
                self._driver_config = nonebot.get_driver().config
            except Exception:
                # 如果在 NoneBot 启动前被导入，get_driver() 可能会失败
                # 此时返回一个空的 Config 对象，防止后续代码崩溃
                self._driver_config = Config()
        return self._driver_config

    def get_config(self, key: str):
        """
        模仿 gsuid_core.get_config 的接口
        """
        if key == "HOST":
            return str(self.driver_config.host)
        if key == "PORT":
            return self.driver_config.port

        return getattr(self.driver_config, key.lower(), None)

    # --- (↓) 添加这个新方法 (↓) ---
    def get_plugin_available_prefix(self, plugin_name: str) -> str:
        """
        获取插件可用的命令前缀。

        将按以下顺序查找:
        1. 插件特定配置 (在 .env 中设置 `WAVES_PREFIX`)
        2. NoneBot 全局配置 (在 .env 中设置 `COMMAND_START`)
        3. 默认回退值 ("#")
        """
        try:
            # 1. 尝试获取插件特定配置
            #    NoneBot 的 Config 会自动处理大小写 (WAVES_PREFIX)
            plugin_prefix = getattr(self.driver_config, "waves_prefix", None)
            if plugin_prefix and isinstance(plugin_prefix, str):
                return plugin_prefix
        except Exception:
            # 在极少数情况下（例如配置读取异常）
            pass

        # 3. 默认回退值
        return "#"


# 创建一个单例，以便在其他地方导入
core_config = LocalCoreConfig()