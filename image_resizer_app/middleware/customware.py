'''
File will be used through out the program for creating and using custom 
middlewares.
'''
import logging

from datetime import datetime

logger = logging.getLogger(__name__)

class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.method == "POST":
            start_time = datetime.utcnow() 
            response = self.get_response(request)
            end_time = datetime.utcnow()
            logger.info(f"Total time take to process image resizing request - {(end_time-start_time).total_seconds()}s")
        else:
            response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response