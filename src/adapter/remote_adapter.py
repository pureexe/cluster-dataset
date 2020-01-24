from abc import ABC,abstractmethod
from shutil import which


class RemoteAdapter(ABC):
    def __init__(self,executeable_name, node_info, local_dir):
        self.__executeable_name = executeable_name
        self.__node = node_info
        self.__local_dir = local_dir
        super().__init__()

    @abstractmethod
    def download(self,path):
        """ download from remote"""
        pass
    
    @abstractmethod
    def upload(self,path):
        """ upload to remote"""
        pass
        
    def avaliable(self):
        """ check if remote sync program (rclone/rsync/etc) avaliable on this pc"""
        return which(self.__executeable_name) is not None

    def address(self):
        return self.__node['address']

    def hostname(self):
        return self.__node['hostname']

    def directory(self):
        return self.__node['directory']

    def local_directory(self):
        return self.__local_dir

