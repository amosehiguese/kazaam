import yaml
import logging

from typing import Dict, Any
from pydantic import BaseModel, ValidationError

class DataSourceConfig(BaseModel):
    seismic: Dict[str, Any]
    well_logs: Dict[str, Any]
    historical: Dict[str, Any]
    external_apis: Dict[str, Any]

class ModelConfig(BaseModel):
    path: str
    version: str
    confidence_threshold: float = 0.7
    device: str = "cuda"

class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    api_keys: Dict[str, str]

class SystemConfig(BaseModel):
    data_sources: DataSourceConfig
    seismic_agent: ModelConfig
    drilling_agent: ModelConfig
    api: APIConfig

    enable_feedback_loop: bool = True

class Config:
    """Main configuration handler with validation."""
    def __init__(self, config_path: str):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_and_validate(config_path)

    def _load_and_validate(self, path: str):
        """Load and validate configuration file."""
        try:
            with open(path, 'r') as f:
                raw_config = yaml.safe_load(f)

            return SystemConfig(**raw_config)

        except FileNotFoundError:
            self.logger.error(f"Configuration file not found as {path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in config file: {str(e)}")
            raise
        except ValidationError as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error loading config: {str(e)}")
            raise
        
    def get_config(self) -> SystemConfig:
        """Get the validate configuration."""
        return self.config