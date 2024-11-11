from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Post,login
import logging
from django.http import Http404, HttpResponseNotFound
from django.core.paginator import Paginator
from .forms import Contact,Login_form,CodeForm,SignupForm,CodeVerificationForm
from django.contrib import messages
from .signals import code_verification_signal
from myapp import settings
from django.core.mail import send_mail

# monthly = [         {'id':'1','january':'post1','content':'january'},
        # {'id':'1','february':'post2','content':'february'},
        # {'id':'2','march':'post3','content':'march'},
        # {'id':'3','april':'post4','content':'april'},
        # {'id':'4','may':'post5','content':'may'}
        # ]
monthly_challenges={
    'january': 'Eat something healthy',
    'february': 'Spend 30 minutes on a hobby',
    'march':'March',
    'april':'April',
    'may':'MAY',
    'june':'JUNE',
    'july':'JULY',
    'august':'AUGUST',
    'september':'SEPTEMBER',
    'october':'OCTOBER',
    'november':'NOVEMBER',
    'december':'DECEMBER'
    
}


def signup_page(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "Signup successful! Please check your email for the verification code.")
            request.session['username'] = new_user.username  # Storing username in session

            # Send verification email
            subject = "Your Verification Code"
            message = f"Hello {new_user.username},\nYour verification code is: {new_user.code}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [new_user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('blog:verifyy')
    else:
        form = SignupForm()

    return render(request, 'blog/signup.html', {'form': form})

def verify_code_view(request):
    username = request.session.get('username')

    user_instance = login.objects.get(username=username)
    code = user_instance.code

    if request.method == "POST":
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            re_enter_code = form.cleaned_data['re_enter_code']

            # Trigger the verification signal
            code_verification_signal.send(sender=login, instance=user_instance, re_enter_code=re_enter_code)
            
            if user_instance.verified:
                messages.success(request, "Verification successful!")
                return redirect('blog:index')
            else:
                messages.error(request, "Incorrect verification code. Please try again.")
                return redirect('blog:verifyy')
    else:
        form = CodeVerificationForm()

    return render(request, 'blog/verify_code.html', {'form': form, 'code': code})


# def signup_page(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             messages.success(request, "Signup successful! Please enter the verification code.")
#             request.session['username'] = new_user.username  # Storing username in session
#             return redirect('blog:verifyy')
#     else:
#         form = SignupForm()

#     return render(request, 'blog/signup.html', {'form': form})

# def verify_code_view(request):
#     user_instance = login.objects.get(username=request.user.username)
#     code = user_instance.code
#     if request.method == "POST":
#         form = CodeVerificationForm(request.POST)
#         if form.is_valid():
#             re_enter_code = form.cleaned_data['re_enter_code']

#             # Welcome Email
#             subject = "Your verification code"
#             message = "Hello " + user_instance.username + "!! \n" + "Your Verification cod is"+ user_instance.code
#             from_email = settings.EMAIL_HOST_USER
#             to_list = [user_instance.email]
#             send_mail(subject, message, from_email, to_list, fail_silently=True)
        
#             # Trigger the verification signal
#             code_verification_signal.send(sender=login, instance=user_instance, re_enter_code=re_enter_code)
#             if user_instance.verified:
#                 messages.success(request, "Verification successful!")
#                 return redirect('blog:index')
#             else:
#                 messages.error(request, "Incorrect verification code. Please try again.")
#                 return redirect('blog:verifyy')
#     else:
#         form = CodeVerificationForm()

#     return render(request, 'blog/verify_code.html', {'form': form, 'code': code})






def index(request):
    title_name = "Krithick's BLOG"
    all_posts = Post.objects.all()
    paginator = Paginator(all_posts ,6)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request,'blog/index.html',{'title_name': title_name , 'page_obj': page_obj},)

def detail(request, post_id):
    try:
        post = Post.objects.get(id=int(post_id))
    except Post.DoesNotExist:
        raise Http404("ONNUM ILLA!")

    
    recently_viewed_pro = Post.objects.none()

    
    if 'recently_viewed' not in request.session:
        request.session['recently_viewed'] = []
  
    recently_viewed = request.session['recently_viewed']

    if str(post_id) in recently_viewed:
        recently_viewed.remove(str(post_id))


    recently_viewed.insert(0, str(post_id))

    if len(recently_viewed) > 5:
        recently_viewed.pop() 

    request.session['recently_viewed'] = recently_viewed
    request.session.modified = True

    recently_viewed_pro = Post.objects.filter(id__in=request.session['recently_viewed'])

    logger = logging.getLogger("testing")
    logger.debug(f'Session recently_viewed: {request.session.get("recently_viewed")}')
    logger.debug(f'Recently viewed posts: {recently_viewed_pro}')

    return render(request, 'blog/details.html', {
        'post': post,
        'recently_viewed_pro': recently_viewed_pro
    })



def old_url_redirect(request):
    return redirect(reverse('blog:new_url_1'))

def new_url_view(request):
    return HttpResponse("you are viewing new page")

def contact_form(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        logger=logging.getLogger('testing')
        if form.is_valid():
            # Access cleaned and validated form data
            logger.debug(f"{form.cleaned_data['name']}")
            logger.debug(f"{form.cleaned_data['email']}")
            logger.debug(f"{form.cleaned_data['message']}")
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug("validation error")
    return render(request,'blog/contact.html')

def about(request):
    return render(request,'blog/contact.html')


# def udemy(request,month):
    # try:
        # for check in monthly:
            # if month in check:
                # return HttpResponse(month)
    # except:
        # return HttpResponse("illa")

# def udemy_re(request,month_id):
    # return render(request,'blog/udemy1.html',{'monthly':monthly})

def index1(request):
    list_items =""
    months = list(monthly_challenges.keys())
    for month in months:
            capitalized_month=month.capitalize()
            month_path = reverse("blog:month-challenge", args=[month])
            list_items += f"<li><a href=\"{month_path}\">{capitalized_month}</a></li>"
            
    response_data=f"<ul>{list_items}</ul>"
    return HttpResponse(response_data)

def monthly_challenge_by_number(request, month):
    months = list(monthly_challenges.keys())
    if month > len(months):
        return HttpResponseNotFound("Invalid")
    redirect_month = months[month -1]
    redirect_path= reverse("blog:month-challenge",args=[redirect_month])
    return HttpResponseRedirect(redirect_path)


def monthly_challenge(request, month):
    try:
        challenge_text= monthly_challenges[month]
        return render(request , "blog/challenge.html")
        
    except:
        return HttpResponseNotFound('Invalid')