#!/usr/bin/env python
"""
Project Request Handler Extension for adding localization and user authentication
 
"""

__author__  = "Gavin M. Roy"
__email__   = "gavinmroy@gmail.com"
__date__    = "2009-11-10"
__version__ = 0.1

import httplib
import project.data
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

#    def get_current_user(self):
#        user_id = self.get_secure_cookie("user")
#        if not user_id: return None
#        return self.backend.get_user_by_id(user_id)

    def get_error_html(self, status_code):
        """ 
        Custom Error HTML Template
        """        
        return self.render('templates/error.html', 
                           host=self.request.host,
                           status_code=status_code, 
                           message=httplib.responses[status_code] );
    
    def get_user_locale(self):
        locale = self.get_argument('locale', None)   
        supported_locales = tornado.locale.get_supported_locales(locale)
        if locale in supported_locales:
            return tornado.locale.get(locale)
#        if "locale" not in self.current_user.prefs:
#            # Use the Accept-Language header
#            return None
            
        return None
#        return self.current_user.prefs["locale"]
