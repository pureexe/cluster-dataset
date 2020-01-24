from abc import ABC,abstractmethod
from shutil import which


class RemoteAdapter(ABC):
    def __init__(self,executeable_name = ''):
        self.__executeable_name = executeable_name
        super().__init__()
    @abstractmethod
    def sync(self):
        pass
    
    @abstractmethod
    def find(self):
        pass
    
    def avaliable(self):
        return which(self.__executeable_name) is not None

