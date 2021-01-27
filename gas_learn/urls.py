from django.urls import path
from gas_learn import views

urlpatterns = [
    # block cate data info
    path("block/", views.Blockview.as_view(), name="block_view"),
    path("block/cate/", views.BlockCateView.as_view(), name="block_cate_view"),
    path("block/del/int:<pk>", views.BlockDeleteView.as_view(), name="block_del_view"),

    # mpool cate data info
    path("mpool/", views.Mpoolview.as_view(), name="mpool_view"),
    path("mpool/cate/", views.MpoolCateView.as_view(), name="mpool_cate_view"),

    # data collect
    path("train/data/block/", views.TrainningDataView.as_view(), name="train_data_view"),

    # train
    path("train/result/", views.TrainingResultView.as_view(), name="train_result_view"),
    path("train/result/<int:epoch>", views.TrainingResultDetailView.as_view(), name="train_result_detail_view"),
    path("train/tigger/", views.TrainingTiggerView.as_view(), name="train_tigger_view"),
    
    # forecast
    path("forecast/result/", views.ForecastResultView.as_view(), name="forecast_result_view"),
    path("forecast/result/<int:epoch>", views.ForecastResultDetailView.as_view(), name="forecast_result_detail_view"),
    path("forecast/tigger/", views.ForecastTiggerView.as_view(), name="forecast_tigger_view"),
]