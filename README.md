# cluster-dataset
[![Build Status](https://travis-ci.org/pureexe/cluster-dataset.svg?branch=master)](https://travis-ci.org/pureexe/experiment-collector) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 

annoy to copy data from your computer to a lot of computing engines when you are doing data science? try cluster-dataset

## Installation
you can install this python module by using pip by typing following command

```
pip install git+https://github.com/pureexe/cluster-dataset
```

## Usage

#### 1. write config.

you store your conflg in other file and load when you need the dataset

config which provide to Dataset class should be have format in dictionary which are

```python
{
  'nodes':[ # store in list of object
    {
      'hostname': 'v01.vll.ist' # hostname usually be pc name such as pakkapon@OMEN. the OMEN is hostname
      'address': 'vistec.ist' # can be ip address and domain name 
      'directory': '/home/me/dataset' # place to store dataset
      'adapter': 'scp' # optional, if not provide it will be rsync
    },
    {
      ...
    },
    ..., # you can have as many nodes as you want
  ]
}
```
#### 2.  load dataset and enjoy

it's time to get your dataset. you won't be headache about find and download dataset anymore.

```python
from cluster_dataset import Dataset
dataset = Dataset('tororo',CONFIG) # change totoro to your dataset naem
path = dataset.get_path() # the cluster set will search every node then download to your pc and return path the dataset
```

## Pre-requirement for rsync and scp
Please setup ssh key authentication in both local PC and nodes to make this python module working correctly.

## Windows User

Windows user doens't support `rsync` right now.

However, We still can use scp by enable OpenSSH client and OpenSSH Server by go to Settings (just press button Windows+I) > Apps > Optional features > Add a feature and click download on OpenSSH client and OpenSSH Server.

Then, Go to services (by press Windows+R and type services.msc) and enable OpenSSH Authenication Agent and OpenSSH SSH Server.

I recommend to set start up type to automatic for Windows server or automatic (delay started) for your persernol computer. If you don't do this you need to do manual start by going into services every times you reboot.  


## My Cluster don't support rsync and scp
If your dataset is in the place that doesn't support rsync and scp. You have to use other protocol such as, [WebDAV](https://en.wikipedia.org/wiki/WebDAV), [SMB](https://en.wikipedia.org/wiki/Server_Message_Block), [XDCC](https://en.wikipedia.org/wiki/XDCC) or your dataset is in commerial cloud service such as [Google Cloud Storage](https://cloud.google.com/storage/), [Amazon AWS S3](https://aws.amazon.com/s3/), [Alibaba OSS](https://www.alibabacloud.com/product/oss) You have to implement own adapater.

### Implement own adapter
To write own adapter, You need to use `RemoteAdapter` as base class. and You have to provide 3 method with is `__init__`, `upload` and `download`. 

For  `__init__`, you need to provide `executeable_name` which need to called when you do upload and download. The base class will raise error if you try to use adapter on the pc that you don't have executable file. For example, Google Cloud need to call  `gcloud` to manage the file. so you set `executeable_name = 'gcloud'`

For `upload` and `download`, You have to write how it will upload and download such as do authentication before download

You can look into how write adapter at [rsync adapter](https://github.com/pureexe/cluster-dataset/blob/master/cluster_dataset/adapter/rsync.py)

```python
from cluster_dataset.adapter.remote_adapter import RemoteAdapter
class GCPadapter(RemoteAdapter):
    def __init__(self, node_info, local_dir):
        executeable_name = 'gcloud' # executeable which require to have on the pc
        super().__init__(executeable_name, node_info, local_dir)
    
    def upload(self, path):
        # DO authen and upload file 
        return True
        
    def download(self, path):
        # Do authen and download file
        return True
```

After you finish implement your own adapter. Please don't forgot to pull request to this repo. the pull request are welcome 🥰🥰🥰

###  Using Own adapter

Now you can specified your new adapter name into `CONFIG['nodes'][0]['adapter]` and add new adapter following this code.

```python
dataset = Dataset('dataset_name',CONFIG)
dataset.add_adapter('googlecloud',GCPadapter)
path = dataset.get_path()
```


## Plan & Feature to implement
- [x] rsync support
- [x] scp support
- [ ] rclone support
- [x] automatic look up in each node
- [ ] automatic sync between local and node
- [ ] raise error when data in local and node are difference and it will replace
- [ ] unit testing support (currently only check for syntax error)

