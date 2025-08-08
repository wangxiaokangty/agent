from abc import ABC, abstractmethod
from typing import Any, Dict, Type
import os
import importlib
from pathlib import Path


class Chunker(ABC):
    """Abstract base class for chunker implementations with Registry functionality."""
    
    _registry: Dict[str, Type['Chunker']] = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses in the registry."""
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls

    @abstractmethod
    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        pass

    def chunk(self, contents: str | list[str], **kwargs) -> list[str] | list[list[str]]:
        batched = True
        if not isinstance(contents, list):
            batched = False
            contents = [contents]
        chunks = self._chunk(contents=contents, **kwargs)
        if not batched:
            return chunks[0]
        return chunks
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'Chunker':
        """Create a chunker instance from configuration dictionary."""
        if 'type' not in config:
            raise ValueError("Configuration must include 'type' field specifying chunker class name")
        
        chunker_type = config['type']
        if chunker_type not in cls._registry:
            raise ValueError(f"Unknown chunker type: {chunker_type}. Available types: {list(cls._registry.keys())}")
        
        chunker_class = cls._registry[chunker_type]
        
        # Extract parameters (exclude 'type' field)
        params = {k: v for k, v in config.items() if k != 'type'}
        
        return chunker_class(**params)
    
    def to_config(self) -> Dict[str, Any]:
        """Convert chunker instance to configuration dictionary."""
        config: Dict[str, Any] = {'type': self.__class__.__name__}
        
        # Get init parameters by inspecting the instance
        if hasattr(self, '__dict__'):
            for key, value in self.__dict__.items():
                # Skip internal attributes and complex objects
                if not key.startswith('_') and key != 'chunker':
                    # Only include simple serializable types
                    if isinstance(value, (str, int, float, bool, list, dict)):
                        config[key] = value
        
        return config
    
    @classmethod
    def get_registry(cls) -> Dict[str, Type['Chunker']]:
        """Get the current registry of chunker classes."""
        return cls._registry.copy()


def _auto_import_chunkers():
    """Automatically import all chunker modules to trigger subclass registration."""
    current_dir = Path(__file__).parent
    
    # Import all Python files in the chunker directory
    for py_file in current_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        # Convert file path to module path
        relative_path = py_file.relative_to(current_dir.parent.parent)
        module_path = str(relative_path.with_suffix("")).replace(os.sep, ".")
        
        try:
            importlib.import_module(module_path)
        except ImportError:
            # Skip modules that can't be imported (e.g., missing dependencies)
            pass

# Auto-import all chunker classes when this module is imported
_auto_import_chunkers()
