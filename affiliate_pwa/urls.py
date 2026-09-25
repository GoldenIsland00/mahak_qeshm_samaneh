from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views
from products import views as product_views
from referrals import views as referral_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.home, name='home'),
    path('register/', account_views.register_view, name='register'),
    path('register/success/', account_views.register_success, name='register_success'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', account_views.dashboard, name='dashboard'),
    path('dashboard/referral/', account_views.referral_page, name='referral'),
    path('dashboard/wallet/', account_views.wallet_page, name='wallet'),
    path('dashboard/withdraw/', account_views.request_withdrawal, name='withdraw'),
    path('dashboard/support/', account_views.support_request, name='support'),
    path('dashboard/profile/', account_views.profile_edit, name='profile'),
    path('packages/', product_views.package_list, name='packages'),
    path('packages/<slug:slug>/', product_views.package_detail, name='package_detail'),
    path('packages/<slug:slug>/buy/', product_views.buy_package, name='buy_package'),
    path('ref/<str:code>/', referral_views.track_referral, name='track_referral'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
