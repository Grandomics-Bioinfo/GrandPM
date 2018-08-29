import csv
from django.http import HttpResponse

from adminfilters.multiselect import UnionFieldListFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Sale, Project, Custom, Sample, Sequence,Analysis_Type
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.contrib import messages
from .forms import ProjectForm

class Analysis_Type_Admin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name')


class SaleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'dept', 'tel')

class CustomAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'custom_name', 'custom_dept')

class ProjectAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'proj_id', 'proj_name', 'platform','analysis_type', 'start', 'deadline', 'state', 'custom')
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
    list_display = ('project', 'get_project_name','sample_id', 'sample_name', 'platform','analysis_type', 'start', 'deadline', 'state')
    list_display_links = ('project','sample_id', 'sample_name')
    def get_project_name(self, obj):
        return obj.project.proj_name
    # list_filter = (
    #     ('sample_id', RelatedDropdownFilter),
    #     ('start', UnionFieldListFilter),
    #     'deadline'
    # )
    list_filter=('sample_id', 'sample_name')
    advanced_filter_fields = ( 'sample_id', 'sample_name', 'start', 'deadline', 'state' )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')
    # autocomplete_fields = ['project']

    fieldsets = (               # Edition form
        (None,  {'fields': ('project', ('sample_id', 'sample_name'), ('platform', 'analysis_type'), ('start', 'priority'), 'description')}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )
   # inlines = [ItemInline]

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('project','sample_id','sample_name', 'platform', 'analysis_type',
                       'start', 'deadline', 'state',
                       'priority', 'description')}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


    actions = ["xiadan_cexu", 'export_csv']
    def xiadan_cexu(self, request, queryset):

        for obj in queryset:
            s=obj.sequence.create(library_id='abc')
            # s.save()
        messages.add_message(request, messages.INFO, '下单成功，已安排测序')
        # print()
    xiadan_cexu.short_description = "下单测序"

    def export_csv(self, request, queryset): 
	    meta = self.model._meta
	    field_names = [field.name for field in meta.fields]

	    response = HttpResponse(content_type='text/csv; charset=gbk')
	    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
	    writer = csv.writer(response)

	    writer.writerow(field_names)
	    for obj in queryset:
	        row = writer.writerow([getattr(obj, field) for field in field_names])
	    
	    messages.add_message(request, messages.INFO, '导出成功')

	    return response
            # s.save()
        # messages.add_message(request, messages.INFO, '下单成功，已安排测序')

    export_csv.short_description = "导出csv"





class SequenceAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('sample', 'library_id','jianku_date', 'sample_type', 'machine_id', 'cell_id', 'sequence_start', 'yield_data')
    list_display_links = ('sample', 'library_id')

    # list_filter = (
    #     ('sample_id', RelatedDropdownFilter),
    #     ('start', UnionFieldListFilter),
    #     'deadline'
    # )
    list_filter=('sample', 'library_id', 'sequence_start')
    # advanced_filter_fields = ( 'sample_id', 'sample_name', 'start', 'deadline', 'state' )
    ordering = ('-created_at',)
    readonly_fields = ('sample', 'created_at', 'last_modified', 'created_by')
    # autocomplete_fields = ['project']

    fieldsets = (               # Edition form
        (None,  {'fields': ( ('sample', 'library_id'), ('jianku_date', 'sample_type'), ('machine_id', 'cell_id'), 'sequence_start', 'yield_data')}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )
   # inlines = [ItemInline]

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('sample','library_id','jianku_date', 
                	'sample_type', 'machine_id','cell_id', 'sequence_start', 'yield_data',
                       'user', 'description')}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)



admin.site.register(Custom, CustomAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Analysis_Type, Analysis_Type_Admin)
