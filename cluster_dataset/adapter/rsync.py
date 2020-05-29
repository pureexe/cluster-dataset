from .remote_adapter import RemoteAdapter
import subprocess, os

class Rsync(RemoteAdapter):    
    def __init__(self,node_info, local_dir):
        super().__init__('rsync', node_info, local_dir)
    def download(self,path):        
        code = subprocess.call([
            'rsync',
            '-auv',
            '{}:{}/{}'.format(self.address(), self.directory(), path),
            '{}'.format(self.local_directory())
        ],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        return code == 0

    def upload(self,path):
        code = subprocess.call([
            'rsync',
            '-auv',
            '{}'.format(self.local_directory()),
            '{}:{}/{}'.format(self.address(), self.directory(), path)
        ],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        return code == 0

    def cache_timeout(self):
        """
        rsync will update source every 1 hour
        """
        return 3600