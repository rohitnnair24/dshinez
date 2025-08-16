from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('api/submit-quote/', views.submit_quote, name='submit_quote'),
    path('api/get-quotes/', views.get_all_quotes, name='get_all_quotes'),
    path('api/delete-quote/<int:quote_id>/', views.delete_quote, name='delete_quote'),
    path('api/delete-all-quotes/', views.delete_all_quotes, name='delete_all_quotes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
