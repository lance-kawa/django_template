from guardian.admin import GuardedModelAdmin


class GuardAdmin(GuardedModelAdmin):
    user_can_access_owned_objects_only = True
    
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being added, not changed
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # If adding a new object
            self.exclude = ("user",)
        else:
            self.exclude = None
        return super().get_form(request, obj, **kwargs)
