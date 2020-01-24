from adapter.remote_adapter import RemoteAdapter

class Rclone(RemoteAdapter):    
    def __init__(self,node_info):
        super().__init__('rclone',node_info)

    def find(self):
        pass 

    def sync(self):
        pass