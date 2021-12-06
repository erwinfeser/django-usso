from django.contrib import admin
from usso.models import Usso


@admin.register(Usso)
class UssoAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'external_id')
    readonly_fields = ('external_id',)

    def get_queryset(self, request):
        qs = super(UssoAdmin, self).get_queryset(request)
        return qs.select_related('user')
