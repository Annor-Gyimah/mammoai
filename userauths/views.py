from django.shortcuts import render, redirect
from userauths.models import User, Profile
from userauths.forms import UserRegisterForm, PasswordResetForm, SetPasswordForm, ProfileUpdateForm, UserUpdateForm, passwordchangingform
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from user_dashboard.models import Notification
from django.contrib.auth import update_session_auth_hash
from django.conf import settings


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        profile = Profile.objects.get(user=user)
        profile.verified = True
        profile.save()
        user.save()
        noti = Notification.objects.create(
            type="User Registered"
        )
        if request.user.is_authenticated:
            noti.user = request.user
        else:
            noti.user = None
        noti.save()
        

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('userauths:sign-in')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('home:index')



def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('userauths/template_activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    from_email = settings.EMAIL_HOST_USER   
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to your email {to_email} inbox and click on the received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you already logged in")
        return redirect('home:index')
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            full_name = form.cleaned_data.get("full_name")
            phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")
            
            # Send activation email
            activateEmail(request, user, email)
            
            # Get profile by user
            profile = Profile.objects.get(user=user)
            profile.full_name = full_name
            profile.phone = phone
            profile.save()
            return redirect("home:index")

        else:
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if email and User.objects.filter(email=email).exists():
                messages.error(request, f"This email {email} is already registered.")
            
            if password1 != password2:
                messages.error(request, "Passwords do not match")

    else:
        form = UserRegisterForm()
       
        
    context = {
        "form": form
    }
    return render(request, 'userauths/sign-up.html', context)



# def RegisterView(request):
#     if request.user.is_authenticated:
#         messages.warning(request, f"Hey you already logged in")
#         return redirect('user_dashboard:dashboard')
    
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST or None)

#         if form.is_valid():
#             form.save()
#             full_name = form.cleaned_data.get("full_name")
#             phone = form.cleaned_data.get("phone")
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password1")

#             user = authenticate(email=email, password=password)
#             login(request, user)
            
#             messages.success(request, f"Hey {user}, your account has been created.")

#             noti = Notification.objects.create(
#                 type="User Registered"
#             )
#             if request.user.is_authenticated:
#                 noti.user = request.user
#             else:
#                 noti.user = None
#             noti.save()


#             profile = Profile.objects.get(user=request.user)
#             profile.full_name = full_name
#             profile.phone = phone
#             profile.save()

#             return redirect("user_dashboard:dashboard")

            

            
                
        
#     else:
#         form = UserRegisterForm()
       
        
#     context = {
#         "form": form
#     }
#     return render(request, 'userauths/sign-up.html', context)



def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("userauths/template_reset_password.html",{
                    'user':associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,"We have emailed you the instructions for your password reset. Please Kindly check your email or spam.")
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home:index')

        
    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="userauths/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset succesfully. You may go ahead and log in now.")
                return redirect('userauths:sign-in')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'userauths/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link has expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home:index")




def loginViewTemp(request):
    if request.user.is_authenticated:
        messages.warning(request, "Already logged in")
        return redirect('user_dashboard:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)
            if user_query is not None:
                login(request, user_auth)
                messages.success(request, "Successfully logged in")
                next_url = request.GET.get("next", "user_dashboard:dashboard")
                return redirect(next_url)
            else:
                messages.error(request, "Username or password doesnt exist")
                return redirect("userauths:sign-in")

        except:
            messages.error(request, "Username or password doesnt exist")
            return redirect("userauths:sign-in")
            
    return render(request, 'userauths/sign-in.html')


def LogoutView(request):
    logout(request)
    #messages.success(request, "Successfully logged out")
    return redirect('home:index')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() or p_form.is_valid():
            u_form.save()
            p_form.save()
            

            messages.success(request, "Profile updated successfully")
            return redirect("user_dashboard:dashboard")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        


    context = {
        "profile":profile,
        "u_form": u_form,
        "p_form": p_form,
        #"form":form,

    }


    return render(request, 'userauths/edit_profile.html',context)


@login_required
def password_change(request):
    profile = Profile.objects.get(user=request.user)
    profile_image_url = Profile.objects.filter(user=request.user).get()
    p_image = profile_image_url.image

    if request.method == "POST":
        form = passwordchangingform(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent logging the user out after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully")
            return redirect("user_dashboard:dashboard")
    else:
        form = passwordchangingform(user=request.user)

    context = {
        "profile": profile,
        "form": form,
        "p_image": p_image
    }
    return render(request, "userauths/password_change.html", context)