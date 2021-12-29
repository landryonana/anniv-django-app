from django.core import serializers
from django.db.models.query_utils import Q
from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.text import slugify
from django.contrib import messages


from utilis.utility import save_form, save_form_user
from accounts.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from evangelisation.models import Profile


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('notification:notification_app_index')
            else:
                return redirect('tu_dois_etre_sauver')              
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url="user_login")
def tu_dois_etre_sauver(request):
    return render(request, 'accounts/tu_dois_etre_sauver.html')


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required(login_url="user_login")
def user_recherche(request):
    data = dict()
    users = None
    counter = None
    if request.GET.get('name') == 'query':
        value = request.GET.get('value')
        users = User.objects.filter(
            Q(username__contains=str(value)) | Q(first_name__contains=str(value))
        )
    else:
        users = User.objects.all()

    if len(users) > 1:
            counter_str = f"{len(users)} resultats"
    else:
        counter_str = f"{len(users)} resultat"
        counter = len(users)
        data['counter'] = counter
        data['empty_result'] = f"Pas de résultat"

    data['counter_str'] = counter_str
    data['users'] = render_to_string(
            'partials/table.html', 
            {'users':users}, 
            request=request
        )
    return  JsonResponse(data, safe=False)


@login_required(login_url="user_login")
def user_comptes(request):
    context = dict()
    if request.method == 'POST':
        action = request.POST.get('objects')
        if action == 'supprimer':
            users_del = []
            selected = request.POST.getlist('selected_action')
            if selected:
                for id in selected:
                    try:
                        user = User.objects.get(id=id)
                        users_del.append(user)
                    except User.DoesNotExist:
                        raise Http404("Pages non disponible")
                return render(request, 'partials/suppressions.html', {'users':users_del})
            else:
                messages.error(request, f"Merci de selectionner l'option\
                                    <b>supprimer tous les comptes ET selectioner au moins un element</b>\
                                    et valider"
                            )
        else:
            messages.error(request, f"Merci de selectionner l'option\
                                    <b>supprimer tous les comptes ET selectioner au moins un element</b>\
                                    et valider"
                            )
    users = User.objects.all()
    context['users'] = users
    context['select_link'] = 'comptes'
    return render(request ,'accounts/comptes.html', context)



@login_required(login_url="user_login")
def user_register(request):
    form = None
    context = dict()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            #no save form directely
            new_user = form.save(commit=False)
            #set password
            new_user.set_password(form.cleaned_data['password'])
            #save user or create new user
            new_user.save()
            
            #create new Profile of new user
            Profile.objects.create(user=new_user)
            messages.success(request, f"Vous avez ajouté <b>{new_user}</b> avec success")
            return redirect('user_comptes')
            
    else:
        form = UserRegistrationForm()
    context['form'] = form
    context['compte'] = True
    return render(request ,'partials/form_model.html', context)



@login_required(login_url="user_login")
def user_edit(request):
    user_form = None
    profile_form = None
    context = dict()
    if request.method == 'POST':
        user_form = UserEditForm(
                instance=request.user,
                data=request.POST, files=request.FILES)
        profile_form = ProfileEditForm(
                instance=request.user.profile,
                data=request.POST,
                files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            ext = str(profile.image.name).split('.')[-1]
            image_name = f'photo-de-{slugify(profile.user)}.{ext}'
            profile.image.name = image_name

            user_form.save()
            profile.save()
            return redirect('user_detail')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['select_link'] = 'profile'
    return render(request, 'accounts/user-edit-profile.html', context)




@login_required(login_url="user_login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # update passeword in session
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change_form.html', {
        'form': form,
        'select_link': 'profile'
    })


@login_required(login_url="user_login")
def password_change_done(request):
    return render(request, 'accounts/password_change_done.html')


@login_required(login_url="user_login")
def user_delete_users(request):
    list_users_id = request.POST.getlist('user_selected')
    for id in list_users_id:
        try:
            user = User.objects.get(id=int(id))
            user.delete()
        except User.DoesNotExist:
            raise Http404("Pages non disponible")
    if len(list_users_id)>1:
        messages.success(request, f'<b>suppression réussit de {len(list_users_id)} utilisateurs')
    else:
        messages.success(request, f'<b>suppression réussit de {len(list_users_id)} utilisateur')
    
    return redirect('user_comptes')

@login_required(login_url="user_login")
def user_delete(request, pk):
    context = dict()
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        raise Http404("Pages non disponible")

    if request.method=='POST':
        user.delete()
        return redirect('users')

    context['user'] = user
    return render(request, 'account/user_delete.html', context)




@login_required(login_url="user_login")
def user_detail(request, pk=None):
    user = None
    context = dict()
    if pk:
        try:
            user = User.objects.get(id=int(pk))
        except User.DoesNotExist:
            raise Http404("Pages non disponible")
    else:
        user = get_object_or_404(User, pk=request.user.id)
        context['mon_profile'] = True
    context = {'user': user}
    context['select_link'] = 'profile'
    
    return render(request, 'accounts/user-profile.html', context)