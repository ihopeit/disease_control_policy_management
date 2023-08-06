from django.contrib import admin
from django.apps import apps

from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ImportMixin
from import_export.widgets import ManyToManyWidget

from import_export import resources, fields
import tablib

from django_admin_search.admin import AdvancedSearchAdmin
from .form import PolicyFormSearch

from .models import Policy, DiseaseType

# Set ordering of Apps and models in Django admin dashboard
# https://stackoverflow.com/questions/58256151/set-ordering-of-apps-and-models-in-django-admin-dashboard
ADMIN_ORDERING = (
    ('policies', ('Policy', 'MyPolicy', 'DiseaseType')),
    ('auth', ('User', 'Group')),
    ('admin_interface', ('Theme', ))
)


# see: https://cloud.tencent.com/developer/article/2219443
# https://zhuanlan.zhihu.com/p/456360553
# https://geek-docs.com/django/django-questions/776_django_parsing_fields_in_djangoimportexport_before_importing.html
class PolicyResource(resources.ModelResource):

    # 给Resource添加一个自定义字段，指向模型的关系对象，用widget做格式规范
    # 关联关系的导入导出, ForeignKeyWidget, ManyToManyWidget
    disease_types = fields.Field(
        column_name='传染病类型',
        attribute='disease_types',
        widget=ManyToManyWidget(DiseaseType, separator=',', field='name')
    )
    
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
        # export_order = ("id","传染病类型","政策类别","政策文件名","政策文件路径","文号","所属国家","发布部门","发布年份","发布日期","实施日期","关键词","时效性","效力级别","创建日期","更新日期","备注")
        export_order = ("id","disease_types", "category","file_name","file_path","number","country","department","year","publish_date","implementation_date","disease_types","keywords","timeliness","effectiveness_level","created_date","updated_date","comment")
        model = Policy
        verbose_name = True

class MyPolicy(Policy):
    class Meta:
        proxy = True
        verbose_name = "政策批量导入导出"
        verbose_name_plural = "政策批量导入导出"

class PolicyExportAdmin(ImportExportModelAdmin):
    list_display = ('file_name', 'id', 'category', 'year', 'department', 'publish_date', 'timeliness', 'effectiveness_level',)
    list_filter = ('category', 'year', 'department', 'disease_types', )

    def has_add_permission(self, request):
         return False
    
    def has_change_permission(self, request, obj=None):
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
    list_display = ('file_name', 'id', 'category', 'year', 'department', 'publish_date', 'timeliness', 'effectiveness_level',)
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

    # def changelist_view(self, request, extra_context=None):
    #     # 自定义统计逻辑
    #     # 根据发布年份、发布部门、政策类别、传染病类别和效力级别进行统计
    #     # 实现你的统计逻辑

    #     return super().changelist_view(request, extra_context=extra_context)

admin.site.site_header = '中国传染病防治政策数据库'
admin.site.site_title  = '中国传染病防治政策数据库'
admin.site.index_title   = '中国传染病防治政策数据库'


def get_app_list(self, request, app_label=None):
    """
        应用、model 排序
    """
    app_dict = self._build_app_dict(request, app_label)
    
    if not app_dict:
        return
        
    NEW_ADMIN_ORDERING = []
    if app_label:
        for ao in ADMIN_ORDERING:
            if ao[0] == app_label:
                NEW_ADMIN_ORDERING.append(ao)
                break
    
    if not app_label:
        for app_key in list(app_dict.keys()):
            if not any(app_key in ao_app for ao_app in ADMIN_ORDERING):
                app_dict.pop(app_key)
    
    app_list = sorted(
        app_dict.values(), 
        key=lambda x: [ao[0] for ao in ADMIN_ORDERING].index(x['app_label'])
    )
     
    for app, ao in zip(app_list, NEW_ADMIN_ORDERING or ADMIN_ORDERING):
        if app['app_label'] == ao[0]:
            for model in list(app['models']):
                if not model['object_name'] in ao[1]:
                    app['models'].remove(model)
        app['models'].sort(key=lambda x: ao[1].index(x['object_name']))
    return app_list

# 模块排序
admin.AdminSite.get_app_list = get_app_list

#  应用名设置成中文
# https://docs.djangoproject.com/en/4.1/ref/applications/#for-application-authors
apps.get_app_config('auth').verbose_name = "系统管理权限"
apps.get_app_config('admin_interface').verbose_name = "界面管理"

admin.site.register(Policy, PolicyAdmin)
admin.site.register(MyPolicy, PolicyExportAdmin)
admin.site.register(DiseaseType)
