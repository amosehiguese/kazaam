import os
import tempfile
import unittest

from  src.utils.config import Config, SystemConfig
from pydantic import ValidationError

class TestConfig(unittest.TestCase):
    """Test configuration loading and validation."""

    def setUp(self):
        self.valid_config = """
        data_sources:
            seismic:
                path: /data/seismic
                format: segy
            well_logs:
                path: /data/well_logs
                format: las
            historical:
                path: /data/historical
            external_apis:
                weather: https://api.weather.com
                regulations: https://api.regulations.com
        
        seismic_agent:
            path: /models/seismic
            version: 1.0.0
            confidence_threshold: 0.75
            device: cuda

        drilling_agent:
            path: models/drilling
            version: 1.0.0

        api:
            host: 0.0.0.0
            port: 8080
            workers: 2
            api_keys:
                client1: abc123
                client2: def456
        """

    def test_valid_config(self):
        """Test loading a valid configuration."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(self.valid_config)
            f.close()

            try:
                config = Config(f.name)
                self.assertIsInstance(config.get_config(), SystemConfig)
                self.assertEqual(config.get_config().api.port, 8080)
                self.assertEqual(config.get_config().seismic_agent.confidence_threshold, 0.75)

            finally:
                os.unlink(f.name)

    def test_missing_required_field(self):
        """Test missing required field in config"""
        invalid_config = self.valid_config.replace("path: /models/seismic", "")
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(invalid_config)
            f.close()

            with self.assertRaises(ValidationError):
                Config(f.name)
            os.unlink(f.name)

    def test_invalid_file_path(self):
        """Test with non_existent config file."""
        with self.assertRaises(FileNotFoundError):
            Config("/nonexistent/config.yaml")

if __name__ == "__main__":
    unittest.main()


