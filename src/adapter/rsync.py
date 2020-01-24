from adapter.remote_adapter import RemoteAdapter

class Rsync(RemoteAdapter):    
    def __init__(self,node_info):
        super().__init__('rsync',node_info)
    def find(self):
        pass 

    def sync(self):
        pass