# encoding: utf-8
from mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django_services import service as svc


class TestModel(MagicMock):

    class _meta:
        object_name = "TestModel"
        app_label = "test"


class CRUDServiceForTest(svc.CRUDService):
    model_class = TestModel

    def my_operation(self, obj):
        pass


class ServiceForTest(svc.BaseService):
    model_class = TestModel


class BaseServiceTest(TestCase):

    def test_after_instantiate_put_user_as_instance_attribute(self):
        user = User()
        service = ServiceForTest(user=user)
        self.assertIs(user, service.user)
        self.assertIsNone(service.request)

    def test_after_instantiate_put_request_as_instance_attribute(self):
        request = HttpRequest()
        request.user = User()
        service = ServiceForTest(request)
        self.assertIs(request, service.request)
        self.assertIs(request.user, service.user)


class CRUDServiceTest(TestCase):

    def create_service(self):
        request = HttpRequest()
        request.user = User()
        return CRUDServiceForTest(request)

    def create_model(self):
        obj = TestModel()
        return obj

    @patch.object(User, 'has_perm')
    def test_create_will_call_obj_save_method(self, has_perm):
        service = self.create_service()
        obj = self.create_model()
        has_perm.return_value = True
        service.create(obj)
        self.assertTrue(obj.save.called)

    def test_validate_will_call_obj_full_clean_method(self):
        service = self.create_service()
        obj = self.create_model()
        service.validate(obj)
        self.assertTrue(obj.full_clean.called)

    @patch.object(User, 'has_perm')
    @patch.object(CRUDServiceForTest, 'validate')
    def test_before_save_call_validate_model(self, validate, has_perm):
        service = self.create_service()
        obj = self.create_model()
        validate.return_value = None
        has_perm.return_value = True
        service.create(obj)
        self.assertTrue(validate.called)

    def test_validate_with_different_object_type_raise_exception(self):
        service = self.create_service()
        obj = object()
        with self.assertRaises(ValidationError):
            service.validate(obj)

    @patch.object(User, 'has_perm')
    def test_create_method_will_check_add_permission(self, has_perm):
        service = self.create_service()
        obj = self.create_model()
        has_perm.return_value = True
        service.create(obj)
        has_perm.assert_called_with('test.add_testmodel', obj=obj)

    @patch.object(User, 'has_perm')
    def test_update_method_will_check_change_permission(self, has_perm):
        service = self.create_service()
        obj = self.create_model()
        has_perm.return_value = True
        service.update(obj)
        has_perm.assert_called_with('test.change_testmodel', obj=obj)

    @patch.object(User, 'has_perm')
    def test_create_method_will_validate_delete_permission(self, has_perm):
        service = self.create_service()
        obj = self.create_model()
        has_perm.return_value = True
        service.delete(obj)
        has_perm.assert_called_with('test.delete_testmodel', obj=obj)

    @patch.object(User, 'has_perm')
    def test_my_custom_method_will_check_permission_with_method_name(self, has_perm):
        service = self.create_service()
        obj = self.create_model()
        has_perm.return_value = True
        service.my_operation(obj)
        has_perm.assert_called_with('test.my_operation_testmodel', obj=obj)
