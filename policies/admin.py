from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ImportMixin
from import_export import resources, fields
import tablib

from django_admin_search.admin import AdvancedSearchAdmin
from .form import PolicyFormSearch

from .models import Policy, DiseaseType

# see: https://cloud.tencent.com/developer/article/2219443
# https://zhuanlan.zhihu.com/p/456360553
# https://geek-docs.com/django/django-questions/776_django_parsing_fields_in_djangoimportexport_before_importing.html
class PolicyResource(resources.ModelResource):

    def __init__(self, input_contract=None):
        super(PolicyResource, self).__init__()
        field_list = Policy._meta.fields
        self.verbose_name_dict = {}
        for i in field_list:
            self.verbose_name_dict[i.name] = i.verbose_name

    # def get_export_fields(self):
    # 默认导入导出field的column_name为字段的名称，这里修改为字段的verbose_name
    def get_fields(self): # 导入和导出的表头都需要用 verbose_name
        fields = super(PolicyResource, self).get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果有设置 verbose_name，则将 column_name 替换为 verbose_name, 否则维持原有的字段名。
            if field_name in self.verbose_name_dict.keys():
                field.column_name = self.verbose_name_dict[field_name]
        return fields

    def export(self, queryset=None, *args, **kwargs):
        """
        Exports a resource.
        """

        self.before_export(queryset, *args, **kwargs)

        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)

        for obj in self.iter_queryset(queryset):
            # obj.gender = obj.get_gender_display()
            data.append(self.export_resource(obj))

        self.after_export(queryset, data, *args, **kwargs)

        return data

    class Meta:
        skip_unchanged = True  # 是否跳过的记录出现在导入结果对象
        report_skipped = False  # 所有记录将被导入
        # export_order = ('id', )
        model = Policy
        verbose_name = True

class MyPolicy(Policy):
    class Meta:
        proxy = True
        verbose_name = "政策导入导出"
        verbose_name_plural = "政策导入导出"

class PolicyExportAdmin(ImportExportModelAdmin):
    list_display = ('file_name', 'category', 'year', 'department', 'publish_date', 'timeliness', 'effectiveness_level',)
    list_filter = ('category', 'year', 'department', 'disease_types', )

    def has_add_permission(self, request):
         return False
    
    def has_change_permission(self, request):
         return False

    # get_queryset方法用于优化查询性能，通过select_related和prefetch_related方法提前加载关联的字段。
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.select_related('category')
        queryset = queryset.prefetch_related('disease_types')
        return queryset

    # get_ordering方法用于指定默认的排序方式，这里按照publication_year字段进行排序。
    def get_ordering(self, request):
        return ['year']

    resource_class = PolicyResource


class PolicyAdmin(AdvancedSearchAdmin):
    list_display = ('file_name', 'category', 'year', 'department', 'publish_date', 'timeliness', 'effectiveness_level',)
    list_filter = ('category', 'year', 'department', 'disease_types', )

    search_form = PolicyFormSearch

    # get_queryset方法用于优化查询性能，通过select_related和prefetch_related方法提前加载关联的字段。
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # queryset = queryset.select_related('category')
        queryset = queryset.prefetch_related('disease_types')
        return queryset

    # get_ordering方法用于指定默认的排序方式，这里按照publication_year字段进行排序。
    def get_ordering(self, request):
        return ['year']

    resource_class = PolicyResource

    # def changelist_view(self, request, extra_context=None):
    #     # 自定义统计逻辑
    #     # 根据发布年份、发布部门、政策类别、传染病类别和效力级别进行统计
    #     # 实现你的统计逻辑

    #     return super().changelist_view(request, extra_context=extra_context)

admin.site.site_header = '中国传染病防治政策数据库'
admin.site.site_title  = '中国传染病防治政策数据库'
admin.site.index_title   = '中国传染病防治政策数据库'

admin.site.register(Policy, PolicyAdmin)
admin.site.register(MyPolicy, PolicyExportAdmin)
admin.site.register(DiseaseType)