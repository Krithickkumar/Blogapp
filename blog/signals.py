from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import login

# Custom signal for code verification
code_verification_signal = Signal()

@receiver(post_save, sender=login)
def generate_code_on_signup(sender, instance, created, **kwargs):
    if created and not instance.code:
        instance.generate_code()

@receiver(code_verification_signal)
def verify_code(sender, instance, re_enter_code, **kwargs):
    # Check if the re-entered code matches the generated code
    instance.verified = instance.code == re_enter_code
    instance.save()









# from django.db.models.signals import post_save
# from django.dispatch import receiver, Signal
# from .models import login

# code_verification_signal = Signal()

# @receiver(post_save, sender=login)
# def generate_code_on_signup(sender, instance, created, **kwargs):
#     if created and not instance.code:
#         instance.generate_code()

# @receiver(code_verification_signal)
# def verify_code(sender, instance, re_enter_code, **kwargs):
#     if instance.code == re_enter_code:
#         instance.verified = True
#     else:
#         instance.verified = False
#     instance.save()







































# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.contrib.auth import login as auth_login
# from django.contrib.auth.models import User
# from .models import login
# from django.shortcuts import render, redirect
# @receiver(user_logged_in)
# def check_code_after_login(sender, request, user, **kwargs):
#     """
#     This signal is triggered after a user has logged in.
#     """
#     username = request.session.get('username')
#     re_enter_code = request.POST.get('re_enter_code')  # This assumes code is sent via POST

#     if username and re_enter_code:
#         try:
#             # Retrieve the user from the Login model
#             user_data = login.objects.get(username=username)

#             # Compare the entered code with the stored code
#             if re_enter_code == user_data.code:
#                 return redirect("blog:index")
#         except login.DoesNotExist:
#             print(f"User {username} does not exist.")

# signals.py
# signals.py
# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.contrib import messages

# @receiver(user_logged_in)
# def check_code_after_login(sender, request, user, **kwargs):

#     username = request.session.get('username')
#     re_enter_code = request.POST.get('re_enter_code')

#     if username and re_enter_code:
#         try:
#             # Retrieve the user from the Login model
#             user_data = login.objects.get(username=username)

#             if re_enter_code == request.session.get('code'):
#                 request.session['is_verified'] = True
#                 messages.success(request, "Verification successful!")
#             else:
#                 messages.error(request, "Incorrect verification code.")
#         except login.DoesNotExist:
#             print(f"User {username} does not exist.")
#             messages.error(request, "User not found.")
