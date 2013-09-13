# encoding: utf-8
import logging
import numbers
from .core import BaseService, CheckMethodPermissions, build_permission_name, \
    nocheckpermission
from django.core.exceptions import PermissionDenied

LOG = logging.getLogger(__name__)
LOG_PERM = logging.getLogger('%s.perm' % __name__)


class CreateServiceMixin(object):

    ''' Add default create operation to service '''
    __metaclass__ = CheckMethodPermissions

    def create(self, obj):
        LOG.info(u'Creating %s - %s', type(obj).__name__, obj)
        self.validate(obj)
        obj.save()


class UpdateServiceMixin(object):

    ''' Add default update operation to service '''
    __metaclass__ = CheckMethodPermissions

    def update(self, obj):
        LOG.info(u'Updating %s - %s', type(obj).__name__, obj)
        obj.save()


class DeleteServiceMixin(object):

    ''' Add default delete operation to service '''
    __metaclass__ = CheckMethodPermissions

    def delete(self, obj):
        LOG.info(u'Deleting %s - %s', type(obj).__name__, obj)
        obj.delete()


class ListServiceMixin(object):

    """
    Performe pre-filter in object list to avoid unauthorized access
    """

    @nocheckpermission()
    def list(self, **filters):
        """ Returns a queryset filtering object by user permission. If you want,
        you can specify filter arguments.

        See https://docs.djangoproject.com/en/dev/ref/models/querysets/#filter for more details
        """
        LOG.debug(u'Querying %s by filters=%s', self.model_class.__name__, filters)
        query = self.__queryset__()
        perm = build_permission_name(self.model_class, 'view')
        query_with_permission = filter(lambda o: self.user.has_perm(perm, obj=o), query)
        ids = map(lambda o: o.pk, query_with_permission)

        # FIXME: Return to query again without use database
        queryset = self.__queryset__().filter(pk__in=ids)
        related = getattr(self, 'select_related', None)
        if related:
            queryset = queryset.select_related(*related)

        return queryset

    def __queryset__(self):
        """ Returns basic queryset """
        return self.model_class.objects.get_query_set()

    @nocheckpermission()
    def get(self, pk=None, **filters):
        """ Retrieve an object instance. If a single argument is supplied, object is queried by
        primary key, else filter queries will be applyed.
        If more than one object was found raise MultipleObjectsReturned.
        If no object found, raise DoesNotExist.
        Raise PermissionDenied if user has no permission 'view' on object.

        See https://docs.djangoproject.com/en/dev/ref/models/querysets/#get for more details
        """
        LOG.debug(u'Querying (GET) %s by pk=%s and filters=%s', self.model_class.__name__, repr(pk), filters)
        query = self.model_class.objects.filter(**filters)
        if pk is None:
            obj = query.get()
        else:
            if (isinstance(pk, basestring) and pk.isdigit()) or isinstance(pk, numbers.Number):
                obj = query.get(pk=pk)
            elif 'slug' in self.model_class._meta.get_all_field_names():
                obj = query.get(slug=pk)
            else:
                # pk is not a number and model has no slug. So, object don't exists.
                raise self.model_class.DoesNotExist()

        perm = build_permission_name(self.model_class, 'view')
        if not self.user.has_perm(perm, obj=obj):
            raise PermissionDenied(u'User %s has no permission %s for object %s' % (self.user, perm, obj))
        return obj


class CRUDService(CreateServiceMixin, UpdateServiceMixin, DeleteServiceMixin, ListServiceMixin, BaseService):
    pass
