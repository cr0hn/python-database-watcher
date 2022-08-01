from __future__ import annotations

import abc

from typing import Iterator


class BusInterface(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def open(cls, connection_string: str) -> BusInterface:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_json_messages(self) -> Iterator[dict]:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_messages(self) -> Iterator[str|bytes|int|float]:
        raise NotImplementedError()

    @abc.abstractmethod
    def send_json_message(self, data: dict):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_message(self, data: dict or str or bytes or int or float):
        raise NotImplementedError()

class BusInterfaceAsync(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    async def open(cls, connection_string: str) -> BusInterface:
        raise NotImplementedError()

    @abc.abstractmethod
    async def read_json_messages(self) -> Iterator[dict]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def read_messages(self) -> Iterator[str|bytes|int|float]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def send_json_message(self, data: dict):
        raise NotImplementedError()

    @abc.abstractmethod
    async def send_message(self, data: dict or str or bytes or int or float):
        raise NotImplementedError()


__all__ = ("BusInterfaceAsync", "BusInterface")
