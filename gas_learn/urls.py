from django.urls import path
from gas_learn import views

urlpatterns = [
    path("block/", views.Blockview.as_view(), name="block_view"),
    path("block/cate/", views.BlockCateView.as_view(), name="block_cate_view"),
    path("block/del/int:<pk>", views.BlockDeleteView.as_view(), name="block_del_view"),
    
    path("mpool/", views.Mpoolview.as_view(), name="mpool_view"),
    path("mpool/cate/", views.MpoolCateView.as_view(), name="mpool_cate_view"),
]