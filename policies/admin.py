from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from .models import Policy, DiseaseType

class PolicyAdmin(ImportExportModelAdmin):
    list_display = ('file_name', 'category', 'year', 'department', 'publish_date', 'timeliness', 'effectiveness_level',)
    list_filter = ('category', 'year', 'disease_types', )
    search_fields = ('file_name', 'disease_types__name', 'category')

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


admin.site.register(Policy, PolicyAdmin)
admin.site.register(DiseaseType)