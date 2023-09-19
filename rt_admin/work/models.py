from django.db import models

# Create your models here.

class Publisher(models.Model): #资料库首字母一定要大写
    name = models.CharField(max_length=255,verbose_name='出版社名稱')
    AREA_CHOICES = [
        ('中国', '中国'),
        ('台湾', '台湾'),
        ('日本', '日本'),
        ('美国', '美国'),
    ]

    area = models.CharField(
        max_length=10,
        choices=AREA_CHOICES,
        verbose_name='合作地區'
    )
    STATUS_CHOICES = [
        ('进行中', '进行中'),
        ('到期', '到期'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='狀態'
    )
    shelf_name = models.CharField(max_length=55,null=True, blank=True,verbose_name='上架出版社名稱')
    advance_payment = models.IntegerField(default=0,verbose_name='保底金')
    fees_percentage = models.DecimalField(max_digits=5, decimal_places=3,null=True, blank=True,verbose_name='手續費百分比 (%)')
    ratio_percentage = models.DecimalField(max_digits=5, decimal_places=3,null=True, blank=True,verbose_name='拆分比 (%)')
    cycle_months = models.IntegerField(default=0,verbose_name='付款週期(月)')

    EXCHANGE_RATE_METHOD_CHOICES = [
        ('无', '无'),    
        ('中间价', '中间价'),
        ('汇款买入价', '汇款买入价'),
        ('汇款卖出价', '汇款卖出价'),
    ]

    exchange_rate_method = models.CharField(
        max_length=10,
        choices=EXCHANGE_RATE_METHOD_CHOICES,
        verbose_name='匯率方式'
    )
    renewal_time = models.DateField(null=True, blank=True,verbose_name='續簽時間')
    start_time = models.DateField(null=True, blank=True,verbose_name='合作開始時間')
    end_time = models.DateField(null=True, blank=True,verbose_name='合作結束時間')
    mark = models.CharField(max_length=255,null=True, blank=True,verbose_name='註記')
