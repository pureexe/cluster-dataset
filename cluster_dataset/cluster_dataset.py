from .adapter import rclone, rsync, scp
import socket, os

class Dataset():
    def __init__(self, dataset_name, configuration):
        super().__init__()
        self.__dataset_name = dataset_name
        self.__nodes = configuration['nodes']
        self.__avaliable_adapter = {}
        self.find_local_directory()
        if not os.path.exists(self.__local_dir):
            os.mkdir(self.__local_dir)
        self.check_avalible_adapter()

    def find_local_directory(self):
        self.__local_dir = None
        hostname = socket.gethostname()
        is_hostname = lambda x: x['hostname'] == hostname
        local_nodes = list(filter(is_hostname,self.__nodes))
        if len(local_nodes) == 0:
            raise RuntimeError('please provide hostname of this pc in configuration')
        self.__local_dir = local_nodes[0]['directory']

    def check_avalible_adapter(self):
        if rsync.Rsync(None,None).avaliable():
            self.__avaliable_adapter['rsync'] = rsync.Rsync
        if rclone.Rclone(None,None).avaliable():
            self.__avaliable_adapter['rclone'] = rclone.Rclone
        if scp.Scp(None,None).avaliable():
            self.__avaliable_adapter['scp'] = scp.Scp
    
    def add_adapter(self, name, adpater):
        self__avaliable_adapter[name] = adpater


    def get_adapter(self,node):
        if 'adapter' in node:
            if not node['adapter'] in self.__avaliable_adapter:
                raise RuntimeError('This PC doesn\'t support {} adapter'.format(node['adapter']))
            return self.__avaliable_adapter[node['adapter']]
        else:
            # currently we use rsync as default adapter
            if not 'rsync' in self.__avaliable_adapter:
                raise RuntimeError('This PC doesn\'t support rsync adapter')

    def download(self, selected_node = None):
        is_downloaded = False
        if selected_node is None:
            for node in self.__nodes:
                adapter = self.get_adapter(node)
                is_downloaded = adapter(node,self.__local_dir).download(self.__dataset_name)
                if is_downloaded:
                    break
            if not is_downloaded:
                raise RuntimeError('target dataset doesn\'t exist on any node')
        else:
            adapter = self.get_adapter(selected_node)
            is_downloaded = adapter(selected_node,self.__local_dir).download(self.__dataset_name)
            if not is_downloaded:
                raise RuntimeError('target dataset doesn\'t exist on selected node')

    def get_path(self):
        # dataset already in local don't need to download
        dataset_local_dir = os.path.join(self.__local_dir,self.__dataset_name)
        if not os.path.exists(dataset_local_dir):
            self.download()
        return os.path.join(self.__local_dir,self.__dataset_name)

    def upload_all(self):
        """ upload this pc into all host (in case of dataset need to update) """
        adapter = self.get_adapter()
        hostname = socket.gethostname()
        for node in self.__nodes:
            if node['hostname'] != hostname:
                adapter(node,self.__local_dir).upload(self.__dataset_name)

def get_config(directory = '/data/cluster-dataset/'):
    """ Example config file for vll.ist """
    output = {'nodes':[]}
    hostname = 'v{:02d}.vll.ist'
    address = '10.204.100.{:d}'
    for i in range(1,5):
        output['nodes'].append({
            'hostname': hostname.format(i),
            'address': address.format(110+i),
            'directory': directory,
        })
    return output