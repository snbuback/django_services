# -*- coding:utf-8 -*-

class ApplicationException(Exception):
    """ Base class for all DjangoService Exceptions """
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.message = args[0]
        elif kwargs.get('message', None):
            self.message = kwargs['message']
        super(ApplicationException, self).__init__(*args, **kwargs)

    def get_message(self):
        message = getattr(self, '_message', None)
        if not message:
            message = unicode(self.__class__.__name__)
        return message

    def set_message(self, msg):
        self._message = msg

    message = property(get_message, set_message)

    def __unicode__(self):
        if self.message:
            return self.message
        return u"%s.%s(message=%s)" % (unicode(self.__module__), unicode(self.__class__.__name__), unicode(self.message))

    def __str__(self):
        return str(self.__unicode__())


class InternalException(ApplicationException):
    """ Base exception when an unrecoverable error happens """
    pass


class InvalidOperationException(ApplicationException):
    """ Base class used for invalid operations """
    pass
