from abc import ABC,abstractmethod
from shutil import which


class RemoteAdapter(ABC):
    def __init__(self,executeable_name = '',node_info):
        self.__executeable_name = executeable_name
        self.__node = node_info
        super().__init__()
        
    @abstractmethod
    def sync(self):
        pass
    
    @abstractmethod
    def find(self):
        pass
    
    def avaliable(self):
        """ check if remote sync program (rclone/rsync/etc) avaliable on this pc"""
        return which(self.__executeable_name) is not None

    def address(self):
        return self.__node.address

    def hostname(self)
        return self.__node.hostname

    def directory(self)
        return self.__node.directory

