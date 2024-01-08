from ..rand import Seed

__all__ = ["Map"]


class Map:
    def __init__(self, max_w: int, max_h: int, seed: str | None = None):
        self.seed: Seed = Seed(seed)
        self.max_w: int = max_w
        self.max_h: int = max_h

    def generate(self) -> None:
        pass
