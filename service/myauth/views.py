from django.shortcuts import render
from .Forms import UserEditorForm, ProfileEditForm
# Create your views here.

def edit(request):
    if request.method == "POST":
        user_form = UserEditorForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user, data=request.POST, files =request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            user_form = UserEditorForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'diploma-frontend/frontend:profile.html', {'user_form': user_form, 'profile_form': profile_form})
