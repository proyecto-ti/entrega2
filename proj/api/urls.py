from django.conf.urls import url
from django.urls import path

from .views import *


# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('inventories', InventoriesView.as_view()),
    path('inventoriestotal', inventories_view),
    path('orders', OrdersView.as_view()),
    path('oc/<str:oc_id>/notification/', OCView.as_view()),
    path('bodegas', bodegas_view),
    path('', estadisticas_view)
]


#    path('bus/', views.bus, name='bus'),
