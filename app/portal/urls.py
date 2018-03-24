from django.urls import path
from django.contrib.auth.views import (
    login,
    logout,
    logout_then_login
)
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),

    # Features
    path('FossTable/', views.viewFossTable, name='viewFossTable'),
    path('FossDetails/<foss>', views.viewFossDetails, name='viewFossDetails'),
    path('AddFossTutorial/<foss_id>',
         views.AddFossTutorial.as_view(), name='addFossTutorial'),
    path('CreateFoss/', views.CreateFOSS.as_view(), name='addNewFoss'),


    path('submissions/', views.UserSubmissions.as_view(), name='submissions'),
    path('publish/<foss_id>/<tut_id>',
         views.publish, name='publish'),
    # Payment
    path('payment/', views.UserPayment.as_view(), name='payment'),
    path('pay/<username>/<multiplier>/<month>', views.pay, name='pay'),

    # Accounts
    path('login/', login, {
        'redirect_authenticated_user': True,
        'template_name': 'portal/forms.html',
        'extra_context': {
            "form_page_name": 'Login',
            'submit_btn_name': "Login",
        },
    }, name='login'),
    path('logout/', logout, name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),

]
