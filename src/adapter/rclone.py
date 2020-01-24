from adapter.remote_adapter import RemoteAdapter

class Rclone(RemoteAdapter):    
    def __init__(self,node_info,local_dir):
        super().__init__('rclone',node_info,local_dir) 

    def download(self,path):
        raise NotImplementedError
    
    def upload(self,path):
        raise NotImplementedError
