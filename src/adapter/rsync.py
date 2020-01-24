from adapter.remote_adapter import RemoteAdapter
import subprocess, os

class Rsync(RemoteAdapter):    
    def __init__(self,node_info, local_dir):
        super().__init__('rsync', node_info, local_dir)

    def download(self,path):
        remote_path = os.path.join(self.directory(),path)
        local_path = os.path.join()
        code = subprocess.call([
            'rsync',
            '-av',
            '{}:{}/{}'.format(self.address(), self.directory(), path),
            '{}/{}'.format(self.local_directory(),path)
        ],stdout=subprocess.DEVNULL)
        return code == 0