from abc import ABC, abstractmethod
from logging import Logger

class Loggador(ABC):
    @abstractmethod
    def LogInfo(mensagem: str) -> None: NotImplemented
    @abstractmethod
    def LogError(mensagem: str) -> None: NotImplemented
    @abstractmethod
    def LogWarning(mensagem: str) -> None: NotImplemented

class MyLogger(Logger, Loggador):
    def __init__(self, *args):
        Logger.__init__(self, "MyLogger", *args)
        Loggador.__init__(self)

    def LogInfo(self, mensagem: str) -> None:
        self.info(mensagem)
    def LogError(self, mensagem: str) -> None:
        self.error(mensagem)
    def LogWarning(self, mensagem: str) -> None:
        self.warning(mensagem)
