from django.urls import path, include
from rest_framework import routers
from user_control.models import UserActivities
# from rest_framework.routers import DefaultRouter
from app_control.views import (
    InventoryItemView, ShopView, SummaryView, PurchaseView, SaleByShopView, InventoryGroupView,
    # InventoryItemViewTest,
    SalePerformanceView, UploadView, InvoiceView, InventoryCSVLoaderView,
)

app_name = "app_control"

router = routers.DefaultRouter(trailing_slash=False)

router.register("inventory-item", InventoryItemView, "inventory-item")
#router.register("inventory-item-test", InventoryItemView, "inventory-item")

router.register("inventory-csv", InventoryCSVLoaderView, "login")
router.register("shop", ShopView, "shop")
router.register("summary", SummaryView, "summary")
router.register("purchase-summary", PurchaseView, "purchase-summary")
router.register("sale-by-shop", SaleByShopView, "sale-by-shop")
router.register("group", InventoryGroupView, "group")
router.register("top-selling", SalePerformanceView, "top-selling")
router.register("invoice", InvoiceView, "invoice")
router.register("uploads", UploadView, "invoice")

urlpatterns = [
    path('/', include(router.urls)),
]
