from adapter.remote_adapter import RemoteAdapter

class Rclone(RemoteAdapter):    
    def __init__(self):
        super().__init__('rclone')

    def find(self):
        pass 

    def sync(self):
        pass