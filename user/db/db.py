# app.py the main portal for the service

#!/usr/bin/env python
import ConfigParser
import os
from tornado_mysql import pools
from tornado_mysql import err
from tornado import gen


dbConnPool = None

def connPool(): 
    global dbConnPool
    if dbConnPool == None: 
        configParser = ConfigParser.RawConfigParser()
        configDir = os.path.split(os.path.realpath(__file__))[0]
        configFile = configDir + "/db.conf"
        configParser.read(configFile)

        dbConfig = dict(configParser.items('config'))
        dbConnPool = pools.Pool(
            dict(host=dbConfig['host'],
                port=int(dbConfig['port']),
                db=dbConfig['name'],
                user=dbConfig['user'],
                passwd=dbConfig['passwd']),
            max_idle_connections=1,
            max_recycle_sec=8,
            max_open_connections=2)

    return dbConnPool

# add user
def addUser(name, string):
    pass

# update user
def updateUser(id, name, address):
    pass

# delete user
def deleteUser(id):
    pass

def deleteUser(name):
    pass