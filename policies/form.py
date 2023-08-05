from .models import DiseaseType
from django import forms
from django.forms import ModelForm, Form
from django.forms import IntegerField, CharField, ChoiceField, TextInput, ModelChoiceField, ModelMultipleChoiceField


class PolicyFormSearch(Form):
    file_name = CharField(required=False, label="政策文件标题")
    department = CharField(required=False, label="发文部门")
    #  widget=forms.CheckboxSelectMultiple,
    disease_types = ModelChoiceField(queryset=DiseaseType.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label='涉及传染病')
    begin = IntegerField(required=False, widget=TextInput(
        attrs={
            'filter_field': 'year', 
            'filter_method': '__gte',
        } 
    ), label ="发布年份从：")
    end = IntegerField(required=False, widget=TextInput(
        attrs={
            'filter_field': 'year', 
            'filter_method': '__lte',
        }
    ), label='至：')