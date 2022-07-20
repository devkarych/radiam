import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Audio:
    file_path: str
    file_name: str


class AbstractLoader(ABC):

    def __init__(self, url: str):
        self._url = url

    @abstractmethod
    def load(self, user_id: int) -> Audio:
        """
        Implement loading-logic here
        :return: path to saved file
        """

    def clear_cache(self, user_id: int) -> None:
        os.remove(self.get_dst_path(user_id))

    @abstractmethod
    def get_dst_path(self, user_id: int) -> str:
        """Destination path to loaded file"""
        pass
