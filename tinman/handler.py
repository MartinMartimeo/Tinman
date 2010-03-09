#!/usr/bin/env python
"""
Tinman Request Handler

"""

__author__  = "Gavin M. Roy"
__email__   = "gavinmroy@gmail.com"
__date__    = "2009-11-10"
__version__ = 0.3

import httplib
import logging
import tinman.data
import tinman.session
import tornado.locale
import tornado.web

class ErrorHandler(tornado.web.RequestHandler):
    """
    Default Error Handler for 404 Errors
    """

    def get(self):
        return self.render('templates/error.html',
                            host=self.request.host,
                            status_code=404,
                            message=httplib.responses[404] );

class RequestHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, transforms=None):

        # Init the parent class
        super( RequestHandler, self ).__init__(application, request, transforms)

        logging.debug('New Instance of %s' % self.__class__.__name__)

        # Create a new instance of the data layer
        self.data = tinman.data.DataLayer(application.settings['Data'])

        # Create a new instance of the session handler
        self.session = tinman.session.Session(self)

        print self.session.started

    def get_current_user(self):

        try:
            user_id = self.session.user_id
        except AttributeError:
            return None

#        return self.data.get_user_by_id(user_id)

    def get_error_html(self, status_code):
        """
        Custom Error HTML Template
        """
        return self.render('templates/error.html',
                           host=self.request.host,
                           status_code=status_code,
                           message=httplib.responses[status_code] );

    def get_user_locale(self):

        # Try and get the locale from the session
        try:
            locale = self.session.locale
        except AttributeError:
            # It wasn't in the session, try and get it from the arguments
            locale = self.get_argument('locale', None)

        # We don't have a locale yet, get the browser's accept language
        if not locale:
            temp = self.request.headers['Accept-Language']
            parts = temp.split(';')
            if parts[0].find(','):
                parts = parts[0].split(',')
            locale = parts[0]

        # Get the supported locale list
        supported_locales = tornado.locale.get_supported_locales(locale)

        # If our locale is supported return it
        if locale in supported_locales:
            return tornado.locale.get(locale)

        # There is no supported locale
        return None
