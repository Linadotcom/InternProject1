from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('FlashReport.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('authentication.urls')),

] 


# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('FlashReport.urls')),
# ]