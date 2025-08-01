from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('form/', views.customerForm, name='cutomerForm')
]
