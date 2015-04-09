
import time

from ovirtsdk.xml import params
from ovirtsdk.api import API

url = 'http://localhost:8080'
username = 'admin@internal'
password = 'a'

print 'Connecting to', url, 'as', username
api = API(url=url, username=username, password=password)

print 'Connected'

print 'Updating data center'
dc = api.datacenters.get(name='Default')
dc.get_version().set_major(3)
dc.get_version().set_minor(5)
dc.update()
print 'Data center updated'

print 'Updating cluster'
cluster = api.clusters.get(name='Default')
cluster.get_version().set_major(3)
cluster.get_version().set_minor(5)
cluster.set_cpu(params.CPU(id='Intel Westmere Family'))
cluster.update()
print 'Cluster updated'

print 'Creating host'
host = api.hosts.get('Host1')
if host is None:
    host = api.hosts.add(params.Host(
        name='Host1',
        cluster=api.clusters.get(name='Default'),
        address='192.168.122.38',
        root_password='a'))
    print 'Host created'
else:
    print 'Host already exists'


while not (host.get_status().state == 'up'):
    print 'host status: %s' % host.get_status().state
    time.sleep(1)
    host = api.hosts.get(id=host.id)

print 'Creating storage domain'
storageDomain = api.storagedomains.add(
    params.StorageDomain(name='Domain1', host=host, type_='data', storage=params.Storage(
        type_='nfs', address='192.168.122.1', path="/home/jakub/exported-nfs"
    ))
)
print 'Storage domain created'

print 'Attaching storage domain to datacenter'
dc.storagedomains.add(storageDomain)
dc.update()
print 'Storage domain attached'