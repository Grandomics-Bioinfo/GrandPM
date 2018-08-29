from adminfilters.multiselect import UnionFieldListFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Sale, Project, Custom, Sample, Sequence,Analysis_Type
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from .forms import ProjectForm

class Analysis_Type_Admin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name')


class SaleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'dept', 'tel')

class CustomAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'custom_name', 'custom_dept')

class ProjectAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'proj_id','analysis_type', 'proj_name', 'start', 'deadline', 'state', 'custom')
    list_display_links = ('id', 'proj_id')

    list_filter = (
        ('sale', RelatedDropdownFilter),
        ('state', UnionFieldListFilter),
        ('priority', UnionFieldListFilter),
        'deadline'
    )
    advanced_filter_fields = ( 'proj_id', 'proj_name', 'start', 'deadline', 'state' )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')
#    autocomplete_fields = ['custom']

    fieldsets = (               # Edition form
        (None,  {'fields': ('proj_id', ('proj_name', 'custom'), ('state', 'priority'), ('start', 'description'), 'analysis_type')}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )
#    inlines = [ItemInline]

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('custom','sale','proj_id', 'proj_name', 'platform', 'analysis_type',
                       'start', 'deadline', 'state', 
                       'priority', 'description')}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class SampleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    pass

class SequenceAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    pass



admin.site.register(Custom, CustomAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Analysis_Type, Analysis_Type_Admin)
