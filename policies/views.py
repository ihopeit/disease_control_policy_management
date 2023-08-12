from django.db.models import Sum, Count
from django.shortcuts import render
import datetime

# from slick_reporting.views import ReportView
# from slick_reporting.fields import SlickReportField
from .models import Policy, DiseaseType

# Create your views here.
# class SimpleListReport(ReportView):
    
#     report_model = Policy
#     # the model containing the data we want to analyze

#     date_field = 'created_date'
#     # a date/datetime field on the report model

#     group_by = 'year'
#     columns = ['year',
#                SlickReportField.create(Count, 'year', name='year__count', verbose_name='Year Count'),
#                ]

#     # fields on the report model ... surprise !
#     # columns = ['created_date', 'year', 'category', 'file_name',]


#     chart_settings = [{
#         'type': 'line', # line, bar, pie, # maybe doughnut, polarArea, radar, bubble ?
#         'engine_name': 'chartsjs',  # setting the engine per chart
#         'data_source': ['year__count'],  # the name of the field containing the data values
#         'title_source': ['year'],  # name of the field containing the data labels
#         'title': 'Chart (Year Distributions) Highcharts',  # to be displayed on the chart
#     }]

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

def policy_visualization(request):
    # 获取传染病分类列表
    disease_types = DiseaseType.objects.all()

    # 获取当前年份
    current_year = datetime.datetime.now().year

    # 处理查询参数
    category = request.GET.getlist('category')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    exclude_ids = request.GET.get('exclude_ids')

    # 构造查询条件
    query = Policy.objects.all()

    if category:
        query = query.filter(disease_types__name__in=category)

    if start_year:
        query = query.filter(year__gte=start_year)

    if end_year:
        query = query.filter(year__lte=end_year)

    if exclude_ids:
        exclude_ids = exclude_ids.split(',')
        query = query.exclude(id__in=exclude_ids)

    # 查询政策数量按年份分组
    policy_count_by_year = query.values('year').annotate(count=Count('id')).order_by('year')

    context = {
        'disease_types': disease_types,
        'policy_count_by_year': list(policy_count_by_year),
        'start_year': start_year,
        'end_year': end_year,
        'exclude_ids': exclude_ids,
    }

    return render(request, 'policy_visualization.html', context)

def policy_visualization2(request):
    # 处理查询参数
    categories = request.GET.getlist('category')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    exclude_ids_input = request.GET.get('exclude_ids')

    # 构建查询条件
    query = Policy.objects.all()
    if categories:
        query = query.filter(category__in=categories)
    if start_year:
        query = query.filter(year__gte=start_year)
    if end_year:
        query = query.filter(year__lte=end_year)
    if exclude_ids_input and exclude_ids_input != '.':
        exclude_ids = [int(id) for id in exclude_ids_input.split(',')]
        query = query.exclude(id__in=exclude_ids)

    # 查询数据并进行可视化处理
    policy_count_by_year = query.values('year').annotate(count=Count('id'))

    data = list(policy_count_by_year)


    # 构建数据用于传递给模板
    context = {
        'policy_count_by_year': data,
    }

    return render(request, 'policy_visualization.html', context)