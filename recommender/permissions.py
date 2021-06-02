from django.contrib.auth.mixins import UserPassesTestMixin


class IsStaffMixin(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff
