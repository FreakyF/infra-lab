import importlib
import pkgutil
from pathlib import Path

_REGISTRY: dict[str, dict[int, list[str]]] = {}


def _discover() -> None:
    pkg_path = str(Path(__file__).parent)
    for info in pkgutil.iter_modules([pkg_path]):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"{__package__}.{info.name}")
        words = getattr(mod, "WORDS", None)
        if isinstance(words, dict):
            _REGISTRY[info.name] = words


_discover()


def get(name: str) -> dict[int, list[str]]:
    return _REGISTRY[name]


def available() -> list[str]:
    return sorted(_REGISTRY)
