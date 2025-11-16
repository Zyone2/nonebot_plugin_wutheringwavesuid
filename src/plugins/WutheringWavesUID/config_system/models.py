import json
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List, Dict, Any

# 1. 替换 GSC (Generic String Config)
GSC = TypeVar("GSC")


# 2. 创建一个基础配置模型
class BaseGsConfig(BaseModel):
    name: str
    help: str = Field(default="")
    data: Any

    class Config:
        extra = 'allow'


# 3. 替换 GsStrConfig, GsBoolConfig, GsIntConfig
class GsStrConfig(BaseGsConfig):
    def __init__(self, *args, **kwargs):
        # 兼容 (name, help, data)
        # 兼容 (name, help, OLD_ARG, data)
        # 兼容 (name, help, OLD_ARG, OLD_ARG2, data)
        if args:
            name = args[0]
            help = args[1]
            data = args[-1] # data 永远是最后一个
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            # 兼容 pydantic 标准初始化
            super().__init__(**kwargs)

class GsBoolConfig(BaseGsConfig):
    def __init__(self, *args, **kwargs):
        if args:
            name = args[0]
            help = args[1]
            data = args[-1]
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            super().__init__(**kwargs)

class GsIntConfig(BaseGsConfig):
    def __init__(self, *args, **kwargs):
        if args:
            name = args[0]
            help = args[1]
            data = args[-1]
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            super().__init__(**kwargs)

class GsImageConfig(BaseGsConfig):
    def __init__(self, *args, **kwargs):
        if args:
            name = args[0]
            help = args[1]
            data = args[-1]
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            super().__init__(**kwargs)

# 4. 替换 GsListConfig, GsListStrConfig, GsDictConfig
class GsListConfig(BaseGsConfig, Generic[GSC]):
    def __init__(self, *args, **kwargs):
        if args:
            name = args[0]
            help = args[1]
            data = args[-1]
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            super().__init__(**kwargs)

class GsListStrConfig(BaseGsConfig):
    def __init__(self, *args, **kwargs):
        if args:
            name = args[0]
            help = args[1]
            data = args[-1]
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            super().__init__(**kwargs)

class GsDictConfig(BaseGsConfig, Generic[GSC]):
    def __init__(self, *args, **kwargs):
        if args:
            name = args[0]
            help = args[1]
            data = args[-1]
            super().__init__(name=name, help=help, data=data, **kwargs)
        else:
            super().__init__(**kwargs)