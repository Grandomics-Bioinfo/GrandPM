import csv
from django.http import HttpResponse
import pandas as pd
import numpy as np

from .models import Project, Custom, Sale, Sample


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


def convert_int(s):

    if not s:
        return 0
    else:
        return int(s)




def import_project(file_path):
    
    # df = pd.read_excel(file_path, converters={'年龄': convert_int})
    df = pd.read_excel(file_path).fillna('')
    print(df.dtypes)
    df['年龄'] = df['年龄'].apply(convert_int)
    for index, row in df.iterrows():
        sale, _ = Sale.objects.get_or_create(
            name=row['销售'],
            defaults={
            'region':row['区域'],
            # 'city': row['地区']
            }
        )
        custom, _ = Custom.objects.get_or_create(
           name=row['送检医生'],
           dept=row['送检医院'],
           keshi=row['送检科室']
        )

        project, _ = Project.objects.get_or_create(
            contract_id=row['合同编号'],
            defaults={
              'proj_id':row['项目编号(家系编号)'],
               "custom": custom,
               "sale": sale,
               'project_type': row['项目类型'],
               'description': row['项目备注']
            }
        )

        sample, _ = Sample.objects.get_or_create(
            sample_id=row['样本编号'],
            defaults={
                'sample_name': row['姓名'],
                'sample_name2': row['姓名修正'],
                'age': row['年龄'],
                'sex': row['性别'],
                'nation': row['民族'],
                'sample_type': row['样本类型'],
                'sample_use': row['样本用途'],
                'bct_id': row['采血管编号'],
                'clin_info': row['临床信息'],
                'description': row['样本备注'],
                'project': project,
            }
        )





def import_project2(file_path):
    """
liwenjing 
"""
    # df = pd.read_excel(file_path, converters={'年龄': convert_int})

    df = pd.read_excel(file_path).fillna('')
    df['项目周期'] = df['项目周期（工作日）'].apply(convert_int)
    for index, row in df.iterrows():
        sale, _ = Sale.objects.get_or_create(
            name=row['销售'],
        )
        custom, _ = Custom.objects.get_or_create(
           name=row['客户名称'],
           dept=row['客户单位'],
        )

        project, _ = Project.objects.get_or_create(
            contract_id=row['合同编号'],
            defaults={
              'proj_id':row['项目编号'],
              'proj_name':row['合同名称'],
               "custom": custom,
               "sale": sale,
               'project_type': row['项目类型'],
               'description': row['备注'],
            }
        )
       
        platform, _ = Platform.objects.get_or_create(
            name=row['测序平台']
       )
       
        analysis_type_list = []
        for xx in row['项目类型'].split('+'):
            analysis_type, _ = Analysis_Type.objects.get_or_create(
               name=row['项目类型']
           )
            analysis_type_list.append(analysis_type)

        sample, _ = Sample.objects.get_or_create(
            sample_id=row['样本编号'],
            defaults={
                'sample_name': row['姓名'],
                'sample_name2': row['姓名修正'],
                'sex': row['性别'],
                'nation': row['民族'],
                'sample_type': row['样本类型'],
                'deadline': row['合同规定截止日期'],
                'clin_info': row['临床信息'],
                'description': row['样本备注'],
                'project': project,
                'status': row['项目进度'],
                'platform': platform,
                'analysis_type':analysis_type_list,
                'data_size': row['合同要求数据量'],
                'period': row['项目周期'],
                'description': row['样本备注'],
                'end': row['结题日期'],
            }
        )


def export_as_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

