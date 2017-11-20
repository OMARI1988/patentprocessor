import sqlite3
from sqlite3 import Error
import sys
sys.path.append('lib')

from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from matplotlib import pyplot as plt
from scipy.stats import mode
import pandas as pd
from unidecode import unidecode
from lib.alchemy.schema import GrantBase, ApplicationBase
from lib.alchemy import session_generator
from lib.alchemy import schema
from pprint import pprint

sessiongen = session_generator(dbtype='grant')
session = sessiongen()

def plotPatentBreakDown():
    counts =[]
    tablekeys = []
    tables = GrantBase.metadata.tables
    rawtables = tables.keys()#
    for table in rawtables:
        res = session.execute('select count(*) from {0}'.format(table)).fetchone()[0]
        if res:
            counts.append(res)
            tablekeys.append(table)
    d = pd.DataFrame.from_dict({'tables': tablekeys, 'counts': map(lambda x: int(x), counts)})
    d.index = d['tables']
    h = d.plot(kind='bar',figsize=(16,10))
    h.set_xlabel('Table')
    h.set_ylabel('Record Count')
    plt.show()

def getAllTableNames():
    ''' Function to get all the SQL table names
        input()
        output: 
            tableNames : array of table names as strings 
    '''
    tables = GrantBase.metadata.tables
    rawTables = tables.keys()
    return rawTables

def getTotalNumberOfPatents():
    ''' Function to get total number of patents
        input: None
        output: 
            numberOfPatents : Number
    '''
    return session.execute('select count(*) from patent;').fetchone()[0]

def getAllPatents():
    ''' Function to get all patents
        input: None
        output: 
            allPatents : patentObject
    '''

    return session.query(schema.Patent).all()

def getAllClaims():
    ''' Function to get all patents
        input: None
        output: 
            allPatents : patentObject
    '''
    return session.query(schema.Claim).all()


def getAllDescription():
    ''' Function to get all patents
        input: None
        output: 
            allPatents : patentObject
    '''
    return session.query(schema.Description).all()


def getAllCitations():
    ''' Function to get all patents
        input: None
        output: 
            allPatents : patentObject
    '''
    return session.query(schema.USPatentCitation).all()

