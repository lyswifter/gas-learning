from django.contrib import admin
from .models import BlockInfo, BlockCateInfo, MpoolInfo, MpoolCateInfo

# Register your models here.

@admin.register(BlockInfo)
class BlockInfoAdmin(admin.ModelAdmin):
    list_display = ("block_count", "basefee", "epoch", "created")
    search_fields = list_display
    list_filter = list_display

@admin.register(BlockCateInfo)
class BlockCateInfoAdmin(admin.ModelAdmin):
    list_display = ("cate_code", "count", "epoch")
    search_fields = list_display
    list_filter = list_display

@admin.register(MpoolInfo)
class MpoolInfoAdmin(admin.ModelAdmin):
    list_display = ("created", "epoch")
    search_fields = list_display
    list_filter = list_display

@admin.register(MpoolCateInfo)
class MpoolCateInfoAdmin(admin.ModelAdmin):
    list_display = ("cate_code", "count")
    search_fields = list_display
    list_filter = list_display

