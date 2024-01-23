from api.models.client.admin import *
from unfold.sites import UnfoldAdminSite
from api.models import User

from django.contrib.auth.forms import AuthenticationForm

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_superuser']


class UserAdminSite(UnfoldAdminSite):
    """
    App-specific admin site implementation
    """

    login_form = AuthenticationForm

    site_header = 'Todomon'

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.is_active


user_admin = UserAdminSite(name='user_admin')
user_admin.register(Client, ClientAdmin)