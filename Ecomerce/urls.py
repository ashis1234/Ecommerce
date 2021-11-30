from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('products/',include('product.urls')),
    path('orders/',include('order.urls')),
    path('users/',include('user.urls')),
    path('shipping/',include('shipping.urls')),
    

    # path('',include('core.urls')),
    path('api/gettoken/',TokenObtainPairView.as_view(),name="gettoken"),
    path('api/refresh_token/',TokenRefreshView.as_view(),name="refresh_token"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

