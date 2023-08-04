from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class DiseaseType(models.Model):
    name = models.CharField(max_length=100, verbose_name='传染病类型')

    def __str__(self):
        return self.name

class Policy(models.Model):
        # 其他字段...
    TIMELINESS_CHOICES = [
        ('现行有效', '现行有效'),
        ('失效', '失效'),
        ('已被修改', '已被修改'),
        ('尚未失效', '尚未失效'),
        ('部分失效', '部分失效'),
    ]

    EFFECTIVENESS_CHOICES = [
        ('法律', '法律'),
        ('行政法规', '行政法规'),
        ('检查法规', '检查法规'),
        ('司法解释', '司法解释'),
        ('部门规章', '部门规章'),
        ('军事法规规章', '军事法规规章'),
        ('党内法规制度', '党内法规制度'),
        ('团体规定', '团体规定'),
        ('行业规定', '行业规定'),
        ('其他', '其他'),
    ]

    current_year = timezone.now().year
    year_validator = [
        MinValueValidator(1949, message='年份不能早于1949年'),
        MaxValueValidator(current_year, message=f'年份不能晚于{current_year}年'),
    ]

    category = models.CharField(max_length=100, verbose_name='政策类别')
    file_name = models.CharField(max_length=100, verbose_name='政策文件名')
    file_path = models.FileField(upload_to='policy_files/', null=True, blank=True, verbose_name='政策文件路径')
    number = models.CharField(max_length=100, verbose_name='文号')
    country = models.CharField(max_length=100, verbose_name='所属国家')
    department = models.CharField(max_length=100, verbose_name='发布部门')
    year = models.IntegerField(validators=year_validator, help_text='请输入发布年份 yyyy（有效年份为1949~当前年份）', verbose_name='发布年份')
    publish_date = models.DateField(verbose_name='发布日期')
    implementation_date = models.DateField(null=True, blank=True, verbose_name='实施日期')
    disease_types = models.ManyToManyField(DiseaseType, verbose_name='传染病类型列表')
    keywords = models.CharField(max_length=100, null=True, blank=True, verbose_name='关键词')

    timeliness = models.CharField(max_length=100, null=True, blank=True, choices=TIMELINESS_CHOICES, verbose_name='时效性')

    effectiveness_level = models.CharField(max_length=100, null=True, blank=True, choices=EFFECTIVENESS_CHOICES, verbose_name='效力级别')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    status = models.CharField(max_length=100, null=True, blank=True, verbose_name='状态')

    def __str__(self):
        return self.file_name