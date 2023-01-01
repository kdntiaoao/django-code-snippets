from django.urls import path

from snippets import views

app_name = "snippets"
urlpatterns = [
    path("new/", views.snippet_new, name="new"),
    path("<int:snippet_id>/", views.snippet_detail, name="detail"),
    path("<int:snippet_id>/edit/", views.snippet_edit, name="edit"),
    path("<int:snippet_id>/delete/", views.snippet_delete, name="delete"),
]
