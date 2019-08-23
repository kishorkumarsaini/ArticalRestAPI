from django.urls import path,include
from artical.views import ArticalView,LogInView,LogOutView,UserViewSet,Register,ArticalApi
from rest_framework import routers
from .import views

router=routers.DefaultRouter()
router.register('createuser',UserViewSet)

app_name="artical"
urlpatterns = [
    path('',include(router.urls)),
    path('articals/',views.ArticalView.as_view()),
    path('<int:pk>/',views.ArticalView.as_view()),
    path('auth/login',views.LogInView.as_view()),
    path('auth/logout',views.LogOutView.as_view()),
    path('register/',views.Register.as_view()),

]
