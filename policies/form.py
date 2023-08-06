from .models import DiseaseType
from django import forms
from django.forms import ModelForm, Form
from django.forms import IntegerField, CharField, ChoiceField, TextInput, ModelChoiceField, ModelMultipleChoiceField
from django.utils import timezone

current_year = timezone.now().year

# https://stackoverflow.com/questions/5601425/django-and-modelform-how-to-change-integerfield-to-dropdown-box?answertab=scoredesc#tab-top
YEAR_CHOICES = [(x,str(x)) for x in range(1949, current_year + 1 )]
END_YEAR_CHOICES = [(x,str(x)) for x in range(current_year, 1948, -1 )]

class PolicyFormSearch(Form):

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        initial["begin"] = "1950"
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

    file_name = CharField(required=False, label="政策文件标题")
    department = CharField(required=False, label="发文部门")
    #  widget=forms.CheckboxSelectMultiple,

    disease_types = ModelChoiceField(queryset=DiseaseType.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label='涉及传染病')

    # 年份下拉选择:
    begin = IntegerField(required=False, #choices=YEAR_CHOICES, 
                        widget=forms.NumberInput(
        attrs={
            'min':1949,'max': 3000,'type': 'number',
            'filter_field': 'year', 
            'filter_method': '__gte',
        } 
        ),
    label ="发布年份从")
    end = IntegerField(required=False, #choices=END_YEAR_CHOICES,
        widget=forms.NumberInput(
        attrs={
            'min':1949,'max': 3000,'type': 'number',
            'filter_field': 'year', 
            'filter_method': '__lt',
        } 
        ),
        label='至', initial=current_year)