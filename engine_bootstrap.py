
import time

from ovirtsdk.xml import params
from ovirtsdk.api import API


def connect():
    url = 'http://localhost:8080/ovirt-engine/api'
    username = 'admin@internal'
    password = 'a'

    print 'Connecting to', url, 'as', username
    api = API(url=url, username=username, password=password)

    print 'Connected'
    return api


def main():

    api = connect()

    dc = updateDataCenter(api)

    updateCluster(api)

    host = createHost(api, 'Host1', '192.168.122.137')

    storageDomain = createStorageDomain(api, host, 'Domain1', '/home/jakub/nfs1/d1')

    attachDomainToDc(dc, storageDomain)


def attachDomainToDc(dc, storageDomain):
    print 'Attaching storage domain to datacenter'
    dc.storagedomains.add(storageDomain)
    dc.update()
    print 'Storage domain attached'


def createStorageDomain(api, host, name, path):
    print 'Creating storage domain'
    storageDomain = api.storagedomains.get(name)
    if storageDomain is None:
        storageDomain = api.storagedomains.add(
            params.StorageDomain(name=name, host=host, type_='data', storage=params.Storage(
                type_='nfs', address='192.168.122.1', path=path, nfs_version="V4"
            ))
        )
        print 'Storage domain created'
    else:
        print 'Storage domain already exists'
    return storageDomain


def createHost(api, name, ipAddress):
    print 'Creating host'
    host = api.hosts.get(name)
    if host is None:
        host = api.hosts.add(params.Host(
            name=name,
            cluster=api.clusters.get(name='Default'),
            address=ipAddress,
            root_password='a'))
        print 'Host created'
    else:
        print 'Host already exists'
    while not (host.get_status().state == 'up'):
        print 'host status: %s' % host.get_status().state
        time.sleep(1)
        host = api.hosts.get(id=host.id)
    print 'host status: %s' % host.get_status().state
    return host


def updateCluster(api):
    print 'Updating cluster'
    cluster = api.clusters.get(name='Default')
    cluster.get_version().set_major(3)
    cluster.get_version().set_minor(6)
    cluster.set_cpu(params.CPU(id='Intel Haswell-noTSX Family'))
    cluster.update()
    print 'Cluster updated'


def updateDataCenter(api):
    print 'Updating data center'
    dc = api.datacenters.get(name='Default')
    dc.get_version().set_major(3)
    dc.get_version().set_minor(6)
    dc.update()
    print 'Data center updated'
    return dc


main()
