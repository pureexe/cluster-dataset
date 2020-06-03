from .adapter import rclone, rsync, scp
import socket, os, tempfile, sqlite3, getpass, warnings
from datetime import datetime

class Dataset():
    def __init__(self, dataset_name, configuration):
        super().__init__()
        self.__dataset_name = dataset_name
        self.__nodes = configuration['nodes']
        self.__avaliable_adapter = {}
        self.__conn_db = None
        self.find_local_directory()
        if not os.path.exists(self.__local_dir):
            os.mkdir(self.__local_dir)
        self.check_avalible_adapter()
        self.connect_database()

    def __del__(self):
        self.close_database()

    def connect_database(self):
        if self.__conn_db is not None:
            return self.__conn_db
        # use 1 database per user to prevent conflict
        database_path = os.path.join(
            tempfile.gettempdir(),
            'cluster_dataset_{}.db'.format(getpass.getuser())
        )
        self.__conn_db = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        c = self.__conn_db.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS cache_record (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                address TEXT,
                path TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.__conn_db.commit()
        return self.__conn_db

    def close_database(self):
        if self.__conn_db is not None:
            self.__conn_db.close()
    
    def get_db_cursor(self):
        if self.__conn_db is None:
            self.connect_database()
        return self.__conn_db.cursor()

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
        self.__avaliable_adapter[name] = adpater

    def get_adapter(self,node='rsync'):
        if 'adapter' in node:
            if not node['adapter'] in self.__avaliable_adapter:
                raise RuntimeError('This PC doesn\'t support {} adapter'.format(node['adapter']))
            return self.__avaliable_adapter[node['adapter']]
        else:
            # currently we use rsync as default adapter
            if not 'rsync' in self.__avaliable_adapter:
                raise RuntimeError('This PC doesn\'t support rsync adapter')
            return self.__avaliable_adapter['rsync']

    def is_node_cached(self, adapter, local_dir):
        timeout = adapter.cache_timeout()
        if timeout == -1:
            return True
        c = self.get_db_cursor()
        c.execute('''
            SELECT updated_at FROM cache_record WHERE address=? AND path=? ORDER BY id DESC LIMIT 1
        ''', (adapter.address(), local_dir))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        diff_time = datetime.now() - rows[0][0]
        return diff_time.total_seconds() < timeout 

    def set_node_cache(self,adapter, local_dir):
        c = self.get_db_cursor()
        c.execute('''
            INSERT INTO cache_record (address, path, updated_at) VALUES (?,?,?)
        ''',(adapter.address(), local_dir, datetime.now()))
        self.__conn_db.commit()

    def download(self, selected_node = None):
        is_downloaded = False
        plural = 'any' if selected_node is None else 'selected'
        nodes = self.__nodes if selected_node is None else [selected_node]
        local_dir = os.path.join(self.__local_dir,self.__dataset_name)
        for node in self.__nodes:
            adapter = self.get_adapter(node)
            adapter_obj = adapter(node, self.__local_dir)
            cache_hit = self.is_node_cached(adapter_obj, local_dir)
            if not os.path.exists(local_dir) or not cache_hit:
                is_downloaded = adapter_obj.download(self.__dataset_name)
                try:
                    self.set_node_cache(adapter_obj, local_dir)
                except:
                    warnings.warn("Cannot wriet database file, please look into permission setting")
            if is_downloaded or cache_hit:
                break
        self.close_database() #close database imediately after
        if not is_downloaded and not os.path.exists(local_dir):
            raise RuntimeError('target dataset doesn\'t exist on {} node'.format(plural))

    def get_path(self):
        # dataset already in local don't need to download
        self.download()
        return os.path.join(self.__local_dir,self.__dataset_name)

    def upload_all(self):
        """ upload this pc into all host (in case of dataset need to update) """
        adapter = self.get_adapter()
        hostname = socket.gethostname()
        for node in self.__nodes:
            if node['hostname'] != hostname:
                adapter(node,self.__local_dir).upload(self.__dataset_name)

def get_config(directory = '/data/cluster-dataset/', local_directory = None):
    """ Example config file for vll.ist """
    output = {'nodes':[]}

    hostnames = [
        'v01.vll.ist',
        'v02.vll.ist',
        'v03.vll.ist',
        'v04.vll.ist',
        'vision01-desktop',
        'vision02-desktop',
        'vision03-desktop',
        'vision04-desktop',
        'ist01-MS-7C60',
        'ist02-MS-7C60'
    ] 
    address_public = [
        '10.204.100.111',
        '10.204.100.112',
        '10.204.100.113',
        '10.204.100.114',
        '10.204.100.117',
        '10.204.100.118',
        '10.204.100.119',
        '10.204.100.120',
        '10.204.100.123',
        '10.204.100.124'
    ]
    address_private  = [
        '10.0.0.1',
        '10.0.0.2',
        '10.0.0.3',
        '10.0.0.4', #temporary unusable
        '10.0.0.7',
        '10.0.0.8',
        '10.0.0.9',
        '10.0.0.10',
        '10.0.0.23',
        '10.0.0.24'
    ]
    pc_hostname = socket.gethostname()
    in_vll = pc_hostname in hostnames
    addresses = address_public
    if in_vll and pc_hostname != 'v04.vll.ist': #temporary disable on v4
        addresses = address_private

    for i in range(len(addresses)):
        output['nodes'].append({
            'hostname': hostnames[i],
            'address': addresses[i],
            'directory': directory,
        })
    # if this pc isn't member of VLL, add this pc with local path
    
    if not in_vll:
        path_dir = local_directory if local_directory is not None else directory
        output['nodes'].append({
            'hostname': pc_hostname,
            'address': socket.gethostbyname(pc_hostname),
            'directory': path_dir,
        })
    return output
