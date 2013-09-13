# encoding: utf-8
import logging
from functools import wraps
from django.core.exceptions import ValidationError, PermissionDenied

LOG = logging.getLogger(__name__)
LOG_PERM = logging.getLogger('%s.perm' % __name__)

METHOD_PERMISSION_TRANSLATION = {
    'create': 'add',
    'update': 'change'
}


def build_permission_name(model_class, prefix):
    """ Build permission name for model_class (like 'app.add_model'). """
    model_name = model_class._meta.object_name.lower()
    app_label = model_class._meta.app_label
    action_name = prefix
    perm = '%s.%s_%s' % (app_label, action_name, model_name)
    return perm


class checkpermission(object):

    """
    Decorator only to BaseService methods, to protect it from unauthorized calls.
    If no arguments given, permission will be build from method name.
    For example, for method 'start' in VirtualMachineService
    the default permission required will be 'virtualmachine.start_virtualmachine'
    where the first virtualmachine is appname (in this situation same as class name)

    If you like, you can customize permission, only with prefix. For method called
    'start', you can specify:
    @checkpermission(prefix="iniciar")
    to use permission 'virtualmachine.iniciar_virtualmachine'

    Or if you want total control, you can specify entire permission as:
    @checkpermission(permission="virtualmachine.myops_vm")
    """

    def __init__(self, prefix=None, permission=None):
        self.prefix = prefix
        self.permission = permission

    def __call__(self, func):

        @wraps(func)
        def __check__(service, *args, **kwargs):
            perm_name = self.get_permission(service, func)
            obj = args[0] if len(args) else None
            call_name = "%s.%s" % (type(service).__name__, func.__name__)
            self.has_perm(service, perm_name, obj, call_name)
            return func(service, *args, **kwargs)
        __check__.checkpermission = self
        return __check__

    def get_permission(self, service, func):
        """
        Build permission required to access function "func"
        """
        if self.permission:
            perm = self.permission

        elif self.prefix is False:
            # No permission will be checked
            perm = False

        elif self.prefix:
            perm = build_permission_name(service.model_class, self.prefix)

        else:
            name = func.__name__
            # check if there is a translation between default permission and method name
            action_name = METHOD_PERMISSION_TRANSLATION.get(name, name)

            perm = build_permission_name(service.model_class, action_name)
        return perm

    def has_perm(self, service, perm_name, obj, call_name):
        """
        Raise PermissionDenied if user has no permission in object
        """
        user = service.user
        if not (perm_name is False):
            if not user.has_perm(perm_name, obj=obj):
                LOG_PERM.warn(
                    u'User %s has no permission %s. Access to %s with obj=%s',
                    user, perm_name, call_name, obj)
                raise PermissionDenied(u'User %s has no permission %s for object %s' % (service.user, perm_name, obj))

            LOG_PERM.debug(
                u'User %s was authorized to access %s with permission %s with obj=%s',
                user, call_name, perm_name, obj)


class nocheckpermission(checkpermission):

    """
    Disable checkpermission for a method
    """

    def __init__(self):
        super(nocheckpermission, self).__init__(False)


class CheckMethodPermissions(type):

    def __new__(cls, classname, bases, classdict):

        no_perm = ('model_class',)

        for attr, item in classdict.items():
            if not (attr in no_perm) and not attr.startswith('_') and callable(item):
                if not hasattr(item, 'checkpermission'):
                    # comment line bellow if you want disable checkpermission
                    classdict[attr] = checkpermission()(item)

        return type.__new__(cls, classname, bases, classdict)


class BaseService(object):
    __metaclass__ = CheckMethodPermissions
    # no_perm = ('model_class',)

    '''
    Base service class. All bussiness logic must be in services class.
    Methods, not starting with '_', will have check permission before call it.
    If you want to change permission required to execute that method, you can
    put an attribute "perm" in method. If perm is string, it is own permission name.
    If perm is method (or lambda), it will executed before and need to raise PermissionError
    if no permission
    '''

    def __init__(self, request=None, user=None):
        assert request or user, 'Both request and user are None'
        self.request = request
        self.user = user or request.user
        assert self.model_class is not None, 'model_class'

    @nocheckpermission()
    def validate(self, obj):
        """ Raises django.core.exceptions.ValidationError if any validation error exists """

        if not isinstance(obj, self.model_class):
            raise ValidationError('Invalid object(%s) for service %s' % (type(obj), type(self)))
        LOG.debug(u'Object %s state: %s', self.model_class, obj.__dict__)
        obj.full_clean()

    @nocheckpermission()
    def filter_objects(self, objects, perm=None):
        """ Return only objects with specified permission in objects list. If perm not specified, 'view' perm will be used. """
        if perm is None:
            perm = build_permission_name(self.model_class, 'view')
        return filter(lambda o: self.user.has_perm(perm, obj=o), objects)

    def __repr__(self):
        return '%s(user=%s)' % (type(self).__name__, self.user)

    def __str__(self):
        return repr(self)
