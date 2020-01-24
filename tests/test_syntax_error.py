from cluster_dataset import *
def test_dataset_syntax():
    config = get_config('/tmp') 
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    # append this pc information to configure
    config['nodes'].append({
        'hostname': hostname ,
        'address': ip,
        'directory': 'dataset' #path to store dataset in this pc
    })
    #load dataset name totoro
    totoro_dataset = Dataset('totoro',config)