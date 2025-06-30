from django.contrib import admin
from django.urls import path
from client_app import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login_view,name='login'),
    path('add/',views.add_product,name='add'),
    path('signup/',views.register_user,name='signup'),
    path('home/', views.home, name='home'),       # <-- Add this
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.dashboard, name='orders'),      # Temporary, points to dashboard
    path('products/', views.dashboard, name='products'),
    path('customers/', views.dashboard, name='customers'),
    path('settings/', views.dashboard, name='settings'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('order/<int:product_id>/', views.order_page, name='order_page'),
    path('product_filter',views.product_filter, name='product_filter'),
    path('orders_detail/', views.orders_detail, name='orders_detail'),
    path('approve_order/<int:order_id>/', views.approve_order, name='approve_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    #rest api urls
    path('get_user_details/', views.get_user_details, name='get_user_details'),
    path('post_user_details/', views.post_user_details, name='post_user_details'),
    path('update_user_details/<int:user_id>/', views.update_user_details, name='update_user_details'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

