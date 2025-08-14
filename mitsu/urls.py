# mitsu/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Put all site routes under the /mitsu-backend/ prefix
    path("mitsu-backend/", include([
        path("admin/", admin.site.urls),         # -> /mitsu-backend/admin/
        path("api/", include("mitsuback.urls")), # -> /mitsu-backend/api/...
    ])),
]
