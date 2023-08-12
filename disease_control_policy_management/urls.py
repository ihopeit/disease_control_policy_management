"""disease_control_policy_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from policies.views import line_chart, line_chart_json, policy_visualization


from policies import views

urlpatterns = [
    # redirect home page to policy list page 
    path('', RedirectView.as_view(url = '/admin/policies/policy/')),

    path('admin/', admin.site.urls),

    # path('report/', views.SimpleListReport.as_view(), name="policy_report"),
    # path('report/undefined', views.SimpleListReport.as_view()),

    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('policy-visualization', policy_visualization, name='policy_visualization'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
