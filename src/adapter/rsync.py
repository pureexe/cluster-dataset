from adapter.remote_adapter import RemoteAdapter

class Rsync(RemoteAdapter):    
    def __init__(self):
        super().__init__('rsync')
    def find(self):
        pass 

    def sync(self):
        pass