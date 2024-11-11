from django.urls import path
from . import views

app_name = 'blog'

urlpatterns =[
    path("signup",views.signup_page,name="signss"),
    path("index",views.index,name="index"),
    # path("login",views.login_page,name="loginss"),
    path("post/<int:post_id>",views.detail,name="detail"),
    path("new_url",views.new_url_view,name="new_url_1"),
    path("old_url",views.old_url_redirect,name="old_url_redirect"),
    path("contact",views.contact_form,name="contact"),
    # path("udemy/<str:month>",views.udemy,name="udemy_pg"),
    # path("udemy_link/,<str:month_id>",views.udemy_re,name="udemy_ree")
    path("index1",views.index1),
    path("<int:month>",views.monthly_challenge_by_number),
    path("<str:month>",views.monthly_challenge,name="month-challenge"),
    path("about",views.about,name="about"),
    path('verify_code/', views.verify_code_view, name='verifyy'),

]