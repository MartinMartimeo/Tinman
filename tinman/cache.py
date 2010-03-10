#!/usr/bin/env python
"""
Tinman Cache Module
"""

__author__  = "Gavin M. Roy"
__email__   = "gavinmroy@gmail.com"
__date__    = "2010-03-10"
__version__ = 0.1

import logging
import memcache

client = False
config = False

# Cache Decorator
def memoize(fn):

    def wrapper(*args):
        global config, client

        # Get the class name for the key
        temp = str(args[0].__class__).split('.')
        class_name = temp[len(temp)-1:][0]

        # Set the base key
        key = '%s:%s:%s' % ( config['prefix'], str(class_name), str(fn.__name__) )

        # Add the arguments to the key
        for value in args[1:]:
            key += ':%s' % str(value)

        logging.debug('Cache Decorator Get for %s' % key)
        value = client.get(key)
        if value:
            logging.debug('Cache Decorator hit for %s' % key)
            return value

        # Call and return the original function
        value = fn(*args)

        # Set the Value
        logging.debug('Cache Decorator Set for %s' % key)
        client.set(key, value, config['duration'])

        # Return the value
        return value

    return wrapper

class Cache:

    def __init__(self, settings):
        global config, client

        # Create our memcache servers
        if not client:
            logging.debug('Creating a new memcache Client instance')
            config = settings
            client = memcache.Client(config['servers'], debug=0)

    def delete_decorator_item(self, classname, function, parameters):
        global config
        pass
