from abc import ABC,abstractmethod

class RemoteAdapter(ABC):
    @abstractmethod
    def sync(self):
        pass
    
    @abstractmethod
    def find(self):
        pass
    
    @abstractmethod
    def avaliable(self):
        """ check if adapter install on this pc """
        pass
