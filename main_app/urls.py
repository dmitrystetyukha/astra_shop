from django.urls import path

from main_app.views import main_page, Catalog, Category, ProductSingle, about

urlpatterns = [
    path("", main_page, name="main_page"),
    path("catalog/", Catalog.as_view(), name="catalog"),
    path("category/<int:category_id>", Category.as_view(), name="category"),
    path("product/<int:product_id>", ProductSingle.as_view(), name="product"),
    path("about", about, name="about"),
]
