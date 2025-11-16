import json
from pathlib import Path
from typing import Dict, Any, Type

# --- (↓) 这里的 import 变成了相对路径 (↓) ---
from .models import BaseGsConfig


# --- (↑) 这里的 import 变成了相对路径 (↑) ---

class StringConfig:
    def __init__(
            self,
            name: str,
            config_path: Path,
            default_config: Dict[str, BaseGsConfig],
    ):
        self.config_path = config_path
        self.default_config = default_config
        self.config_data: Dict[str, BaseGsConfig] = self._load_config()

    def _load_config(self) -> Dict[str, BaseGsConfig]:
        config_from_file = {}
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_from_file = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        final_config: Dict[str, BaseGsConfig] = {}

        for key, default_obj in self.default_config.items():
            if key in config_from_file:
                saved_value = config_from_file[key]
                if isinstance(saved_value, dict):
                    try:
                        ConfigType: Type[BaseGsConfig] = default_obj.__class__
                        final_config[key] = ConfigType(**saved_value)
                        continue
                    except Exception:
                        pass

            final_config[key] = default_obj

        self._save_config(final_config)
        return final_config

    def _save_config(self, config_data: Dict[str, BaseGsConfig]):
        try:
            json_data = {
                key: obj.model_dump() for key, obj in config_data.items()
            }
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"[WutheringWavesUID] 保存配置文件失败: {e}")
        except Exception as e:
            print(f"[WutheringWavesUID] 序列化配置失败: {e}")

    def get_config(self, key: str) -> BaseGsConfig | None:
        return self.config_data.get(key)