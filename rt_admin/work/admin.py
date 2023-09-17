from django.contrib import admin

# Register your models here.
from .models import Publisher  # 导入你的模型

@admin.register(Publisher)
class Publisher(admin.ModelAdmin):
    list_display = ('name','area','status',)  # 可以根据需要添加其他字段