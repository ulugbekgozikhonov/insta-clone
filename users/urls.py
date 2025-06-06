from django.urls import path

from .views import LoginView, RegisterView, logout_view,ProfileView,FollowView

urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('register/', RegisterView.as_view(), name='register'),
	path('logout/', logout_view, name='logout'),
 	path('profile/<str:username>/', ProfileView.as_view(), name="profile"),
 	path('follow/<str:username>/', FollowView.as_view(), name="follow"),
]
