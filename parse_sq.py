#!/usr/bin/env python

import os
import re
import sys
import pickle
sys.path.append('.')
sys.path.append('./lib/')

import alchemy
from argconfig_parse import ArgHandler
from ConfigParser import ConfigParser
from datetime import datetime
from grant_handler import PatentGrant


def xml_gen(obj):
    """
    XML generator for iteration of the large XML file
    (otherwise high memory required) in replacement of RE
    """
    data = []
    for rec in obj:
        data.append(rec)
        if rec.find("<?xml version=") >= 0 and len(data) > 1:
            yield "".join(data[:-1])
            data = [data[-1]]
    yield "".join(data)


def main(patentroot, xmlregex="ipg\d{6}.xml", commit=200, func=alchemy.add):
    """
    Returns listing of all files within patentroot
    whose filenames match xmlregex
    """
    files = [patentroot+'/'+fi for fi in os.listdir(patentroot)
             if re.search(xmlregex, fi, re.I) is not None]

    config = ConfigParser()
    config.read('{0}/lib/alchemy/config.ini'.format(os.path.dirname(os.path.realpath(__file__))))
    is_loaded = eval(config.get('global', 'is_loaded'))
    pickle_file = "{0}/loaded.pickle".format(config.get('global', 'loaded'))

    loaded = []
    if is_loaded:
        if os.path.exists(pickle_file):
            loaded = pickle.load(open(pickle_file, "rb"))

    for filename in files:
        if filename in loaded:
            continue
        t = datetime.now()
        for i, xml_string in enumerate(xml_gen(open(filename, "rb"))):
            patobj = PatentGrant(xml_string)
            try:
                pass
            except Exception as inst:
                print " *", inst
            if patobj:
                func(patobj, override=False)
            if i % commit == 0:
                print " *", datetime.now() - t, "- rec:", i, filename
                alchemy.commit()

        alchemy.commit()
        print filename, datetime.now() - t
        loaded.append(filename)
        if is_loaded:
            pickle.dump(loaded, open(pickle_file, "wb"))


if __name__ == '__main__':
    print "Loaded"
    args = ArgHandler(sys.argv[1:])

    XMLREGEX = args.get_xmlregex()
    PATENTROOT = args.get_patentroot()

    logfile = "./" + 'xml-parsing.log'
    main(PATENTROOT, XMLREGEX)
