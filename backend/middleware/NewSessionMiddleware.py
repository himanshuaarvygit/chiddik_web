from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

class NewSessionMiddleware(SessionMiddleware):

    def process_response(self, request, response):
        response = super(NewSessionMiddleware, self).process_response(request, response)
        #You have access to request.user in this method
        if not request.user.is_authenticated():
            del response.cookies[settings.SESSION_COOKIE_NAME]
        return response