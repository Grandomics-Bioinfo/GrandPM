import csv
from django.http import HttpResponse

from adminfilters.multiselect import UnionFieldListFilter
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import *
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.contrib import messages
from .forms import ProjectForm

class MachineAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'platform')


class Analysis_Type_Admin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name')


class SaleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'dept', 'tel')

class CustomAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'custom_name', 'custom_dept')

class ProjectAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'proj_id', 'proj_name', 'platform','analysis_type', 'start', 'deadline', 'status', 'custom')
    list_display_links = ('id', 'proj_id')

    advanced_filter_fields = ( 'proj_id', 'proj_name', 'start', 'deadline', 'status' )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')

    fieldsets_temp = (               # Edition form
        (None,  {'fields': ('proj_id', 'proj_name', 'sample_amount', 'proj_owner', 
                           'platform', 'analysis_type', 'start', 'deadline', 'end','status', 'priority')}),
        (_('合同'),{'fields':(('custom', 'sale'), ('contract_type', 'is_invoice', 'invoice_id'), ('price', 'is_pay', 'pay_money'), 'description'), 'classes': ('collapse',)}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )
#    inlines = [ItemInline]
    fieldsets = fieldsets_temp
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = ProjectAdmin.fieldsets_temp
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class SampleAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('project', 'get_project_name','sample_id', 'sample_name', 'platform','analysis_type', 'start', 'deadline', 'status')
    list_display_links = ('project','sample_id', 'sample_name')
    def get_project_name(self, obj):
        return obj.project.proj_name
    # list_filter = (
    #     ('sample_id', RelatedDropdownFilter),
    #     ('start', UnionFieldListFilter),
    #     'deadline'
    # )
    list_filter=('sample_id', 'sample_name')
    advanced_filter_fields = ( 'sample_id', 'sample_name', 'start', 'deadline', 'status' )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')
    # autocomplete_fields = ['project']

    fieldsets_tmp = (               # Edition form
        (None,  {'fields': ('project', 'sample_id', 'sample_name', 'platform', 'analysis_type', 'start', 'deadline',
                'data_size', 'receive_start','extract_finish', 'library_finish', 'sequence_finish','bioinfo_finish',
               'status', 'priority', 'description')}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )
    fieldsets = fieldsets_tmp
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = SampleAdmin.fieldsets_tmp
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


    actions = ["order_sequence", 'export_csv']
    def order_sequence(self, request, queryset):

        for obj in queryset:
            s=obj.sequence.create(library_id='abc')
            # s.save()
        messages.add_message(request, messages.INFO, '下单成功，已安排测序')
        # print()
    order_sequence.short_description = "下单测序"

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


class ExtractionAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('order_date', 'sample', 'sample_type','method')
    list_display_links = ('sample', )

    # list_filter = (
    #     ('sample_id', RelatedDropdownFilter),
    #     ('start', UnionFieldListFilter),
    #     'deadline'
    # )
    list_filter=('sample',)
    # advanced_filter_fields = ( 'sample_id', 'sample_name', 'start', 'deadline', 'status' )
    ordering = ('-created_at',)
    readonly_fields = ('sample', 'created_at', 'last_modified', 'created_by')
    # autocomplete_fields = ['project']

   # inlines = [ItemInline]
    fieldsets_tmp = ( 
                (None, {'fields': ('sample', 'order_id', 'order_date', 'proj_type','bct_id', 'bct_amount',
                        'sample_type','method', 'finish_date',
                         'user', 'description')}),
               (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)})
            )

    fieldsets = fieldsets_tmp
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = ExtractionAdmin.fieldsets_tmp      # Creation form
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class SequenceAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('order_date', 'sample', 'library_id','library_start', 'sequence_start', 'yield_data')
    list_display_links = ('sample', 'library_id')

    # list_filter = (
    #     ('sample_id', RelatedDropdownFilter),
    #     ('start', UnionFieldListFilter),
    #     'deadline'
    # )
    list_filter=('sample', 'library_id', 'sequence_start')
    # advanced_filter_fields = ( 'sample_id', 'sample_name', 'start', 'deadline', 'status' )
    ordering = ('-created_at',)
    readonly_fields = ('sample', 'created_at', 'last_modified', 'created_by')
    # autocomplete_fields = ['project']

   # inlines = [ItemInline]
    fieldsets_tmp = ( 
                (None, {'fields': ('sample', 'order_id', 'order_date', 'library_require','library_start', 'sample_type',
                        'library_id','machine_id', 'cell_pos', 'sequence_start', 'sequence_end', 'yield_data',
                       ('ap_total','ap_muxscan'), ('ap_g1', 'ap_g2', 'ap_g3', 'ap_g4'),
                       'user', 'description')}),
               (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)})
            )

    fieldsets = fieldsets_tmp
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = SequenceAdmin.fieldsets_tmp      # Creation form
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class BioinfoAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('sample', 'total_bases','pass_bases', 'pass_reads_n50')
    list_display_links = ('sample',)

    # list_filter = (
    #     ('sample_id', RelatedDropdownFilter),
    #     ('start', UnionFieldListFilter),
    #     'deadline'
    # )
    list_filter=('sample', 'total_bases','pass_bases', 'pass_reads_n50')
    # advanced_filter_fields = ( 'sample_id', 'sample_name', 'start', 'deadline', 'status' )
    ordering = ('-created_at',)
    readonly_fields = ('sample', 'created_at', 'last_modified', 'created_by')
    # autocomplete_fields = ['project']

   # inlines = [ItemInline]
    fieldsets_tmp = ( 
                (None, {'fields': ('sample', 'total_bases','pass_bases', 'pass_reads_n50'
                       'user', 'description')}),
               (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)})
            )

    fieldsets = fieldsets_tmp
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = BioinfoAdmin.fieldsets_tmp      # Creation form
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)



admin.site.register(Custom, CustomAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Extraction, ExtractionAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Analysis_Type, Analysis_Type_Admin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Bioinfo, BioinfoAdmin)
