from django.db import models

class DiseaseType(models.Model):
    name = models.CharField(max_length=100, verbose_name='传染病类型')

    def __str__(self):
        return self.name

class Policy(models.Model):
    category = models.CharField(max_length=100, verbose_name='政策类别')
    file_name = models.CharField(max_length=100, verbose_name='政策文件名')
    file_path = models.FileField(upload_to='policy_files/', verbose_name='政策文件路径')
    number = models.CharField(max_length=100, verbose_name='文号')
    country = models.CharField(max_length=100, verbose_name='所属国家')
    department = models.CharField(max_length=100, verbose_name='发布部门')
    year = models.IntegerField(verbose_name='发布年份')
    publish_date = models.DateField(verbose_name='发布日期')
    implementation_date = models.DateField(verbose_name='实施日期')
    disease_types = models.ManyToManyField(DiseaseType, verbose_name='传染病类型列表')
    keywords = models.CharField(max_length=100, verbose_name='关键词')
    timeliness = models.CharField(max_length=100, verbose_name='时效性')
    effectiveness_level = models.CharField(max_length=100, verbose_name='效力级别')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    status = models.CharField(max_length=100, verbose_name='状态')

    def __str__(self):
        return self.file_name