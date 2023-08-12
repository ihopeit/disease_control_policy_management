from django.db.models import Sum, Count
from django.shortcuts import render
from django.contrib import admin

import datetime

# from slick_reporting.views import ReportView
# from slick_reporting.fields import SlickReportField
from .models import Policy, DiseaseType

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='line_chart.html')

line_chart_json = LineChartJSONView.as_view()

def PolicyVisualizationView(request):
    # 获取传染病分类列表
    disease_types = DiseaseType.objects.all()

    # 获取当前年份
    current_year = datetime.datetime.now().year

    # 处理查询参数
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    exclude_ids = request.GET.get('exclude_ids')

    # 构造查询条件
    query = Policy.objects.all()

    selected_disease_types = request.GET.getlist('disease_types', [])
    if selected_disease_types:
        query = query.filter(disease_types__id__in=selected_disease_types)

    # if category:
    #     query = query.filter(disease_types__name__in=category)

    if start_year:
        query = query.filter(year__gte=start_year)

    if end_year:
        query = query.filter(year__lte=end_year)

    if exclude_ids and len(exclude_ids) > 0:
        exclude_id_list = exclude_ids.split(',')
        # Filter out any non-numeric values.
        exclude_id_list = [id_ for id_ in exclude_id_list if id_.isdigit()]
        if exclude_id_list:  # Only apply the filter if there are valid IDs to exclude.
            query = query.exclude(id__in=exclude_id_list)

    # 是否按照传染病类别统计政策文件数量    
    group_by_category = request.GET.get('group_by_category')

    show_raw_data = request.GET.get('show_raw_data')

    # 查询政策数量按年份分组
    # 在进行年份统计时，同一条政策记录如果属于多个传染病类别，会被重复计算, Count 聚合函数在默认情况下不会考虑重复的记录。
    policy_count_by_year = query.values('year').annotate(count=Count('id', distinct=True)).order_by('year')


    # 计算数据总量
    total_count = query.distinct().count()

    context = admin.site.each_context(request)
    # 添加其他上下文变量
    #context['other_context'] = 'other value'

    other_context = {
        'disease_types': disease_types,
        'policy_list':  query.distinct(),
        'policy_count_by_year': list(policy_count_by_year),
        'selected_disease_types': [int(id) for id in request.GET.getlist('disease_types', [])],
        'current_year': current_year,
        'show_raw_data': show_raw_data,
        'start_year': start_year,
        'end_year': end_year,
        'group_by_category': group_by_category,
        'total_count': total_count,  # 添加数据总量
    }
    if exclude_ids:
        other_context['exclude_ids'] =  exclude_ids

    if group_by_category:
        policy_count_by_disease_type = query.values('disease_types__name').annotate(count=Count('id', distinct=True)).order_by('disease_types')
        other_context['policy_count_by_category'] = policy_count_by_disease_type

    context.update(other_context)

    return render(request, 'policy_visualization.html', context)

