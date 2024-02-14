import re
from abc import ABC, abstractmethod
from typing import Any

import src


class Strategy(ABC):
    """Абстрактный класс, использующийся для определения функции для поиска. Реализация описана в классах ниже."""
    @abstractmethod
    def find(self, data):
        pass


class Name(Strategy):
    """Класс для поиска по имени."""

    PATTERN = re.compile(r'^[A-ZА-Я][a-zа-я]+$')

    def find(self, data: str) -> Any:
        if not self.PATTERN.match(data):
            error = '\nУказано неверное имя!\n'
            return {'status': False, 'error': error}

        profiles = src.get_profiles()
        if profiles:
            found = [profile for profile in profiles if profile.name == data]
            return src.get_profiles_with_pagination(profiles=found, from_found=True)

        return None


class Number(Strategy):
    """Класс для поиска по номеру."""

    PATTERN = re.compile(r'^\d{11}$')

    def find(self, data: str) -> dict | None:
        if not self.PATTERN.match(data):
            error = '\nУказан неверный личный номер!\n'
            return {'status': False, 'error': error}

        profiles = src.get_profiles()
        if profiles:
            found = [profile for profile in profiles if str(profile.number) == data]
            return src.get_profiles_with_pagination(profiles=found, from_found=True)

        return None


class Context:
    """Класс, определяющий в рамках какого контекста будет производиться поиск."""

    def __init__(self, strategy: Name | Number) -> None:
        self._strategy = strategy

    def find(self, data: str) -> dict | None:
        return self._strategy.find(data)
