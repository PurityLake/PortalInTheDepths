from random import choice
import hashlib
from string import ascii_letters, digits


class Seed:
    _SEED_CHARS: str = ascii_letters + digits

    def __init__(self, seed: str | None = None) -> None:
        self.seed: str = seed or self._create_seed()
        self.hash: int = (
            int(hashlib.sha256(self.seed.encode("utf-8")).hexdigest(), 16) % 10**8
        )

    def _create_seed(self) -> str:
        return "".join([choice(self._SEED_CHARS) for _ in range(16)])

    def get(self) -> int:
        return self.hash
