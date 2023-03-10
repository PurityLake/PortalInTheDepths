from abc import ABCMeta, abstractmethod
from typing import Any, Self
import pygame

__all__ = ['Scene']


class Scene(metaclass=ABCMeta):
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> Self:
        pass

    @abstractmethod
    def get_event(self, event: pygame.Event) -> None:
        pass

    @abstractmethod
    def set_data(self, name: str, val: Any) -> Any:
        pass
