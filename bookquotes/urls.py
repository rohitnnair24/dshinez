from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    submit_quote,
    get_all_quotes,
    delete_quote,
    delete_all_quotes,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    logout,
    get_todos,
    is_logged_in,
)

urlpatterns = [
    path('api/submit-quote/', submit_quote, name='submit_quote'),
    path('api/get-quotes/', get_all_quotes, name='get_all_quotes'),
    path('api/delete-quote/<int:quote_id>/', delete_quote, name='delete_quote'),
    path('api/delete-all-quotes/', delete_all_quotes, name='delete_all_quotes'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', logout, name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('todos/', get_todos, name='get_todos'),
    path('authenticated/', is_logged_in, name='is_logged_in'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
