from django.contrib import admin

from userauths.models import User, Profile
from user_dashboard.models import Notification, Patient, Results, Status
# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'age', 'gender']
    search_fields = ['firstname', 'lastname']
    #prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set the user on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['user'].queryset = User.objects.filter(id=request.user.id)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hostel":
            if not request.user.is_superuser:
                kwargs["queryset"] = Patient.objects.filter(user=request.user)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    




admin.site.register(Notification)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Results)
admin.site.register(Status)

