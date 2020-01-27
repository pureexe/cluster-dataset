from cluster_dataset import Dataset, get_config
import socket

# load VLL cluster v1-v4 configure
config = get_config('/home/pakkapon') #change into path on the node
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

# append this pc information to configure
config['nodes'].append({
    'hostname': hostname ,
    'address': ip,
    'directory': 'dataset', # Path to store dataset in this pc
    'adapter': 'scp' # If doesn't provide adpater type, It will pick rsync by default
})

#load dataset name totoro
totoro_dataset = Dataset('totoro',config)

#get path of dataset on this pc, if not exist it will automatic look up from node
path = totoro_dataset.get_path()
