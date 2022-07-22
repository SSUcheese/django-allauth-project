from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "reviews/<int:review_id>/",
        views.ReviewDetailListView.as_view(),
        name="review-detail",
        )
]