from django.contrib import admin
from django.urls import include, path

from snippets.views import top

urlpatterns = [
    path("", top, name="top"),
    path("accounts/", include("accounts.urls")),
    path("snippets/", include("snippets.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
