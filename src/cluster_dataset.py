from adapter import rclone,rsync

class Dataset():
    def __init__(self,dataset_name, configuration):
        self.__nodes = configuration.nodes
        super().__init__()
    
    def hello(self):
        return 'hello'