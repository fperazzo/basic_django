# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

# Extending User Model Using a One-To-One Link
# There is a good chance that this is what you want. Personally that is the method I use for the most part. We will be creating a new Django Model to store the extra information that relates to the User Model.

# Bear in mind that using this strategy results in additional queries or joins to retrieve the related data. Basically all the time you access an related data, Django will fire an additional query. But this can be avoided for the most cases. I will get back to that later on.

# I usually name the Django Model as Profile:


##Now this is where the magic happens: we will now define signals so our Profile model will be automatically created/updated when we create/update User instances.


####  MODEL.PY ######


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Basically we are hooking the create_user_profile and save_user_profile methods to the User model, whenever a save event occurs. This kind of signal is called post_save.

# Great stuff. Now, tell me how can I use it.

# Piece of cake. Check this example in a Django Template:




<h2>{{ user.get_full_name }}</h2>
<ul>
  <li>Username: {{ user.username }}</li>
  <li>Location: {{ user.profile.location }}</li>
  <li>Birth Date: {{ user.profile.birth_date }}</li>
</ul>


# How about inside a view method?

# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()


# Generally speaking, you will never have to call the Profile’s save method. Everything is done through the User model.

# What if I’m using Django Forms?

# Did you know that you can process more than one form at once? Check out this snippet:

####  forms.py  ######


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company')


####  VIEWS.PY ######

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


####  profile.html ######

<form method="post">
  {% csrf_token %}
  {{ user_form.as_p }}
  {{ profile_form.as_p }}
  <button type="submit">Save changes</button>
</form>


# And the extra database queries you were talking about?

# Oh, right. I’ve addressed this issue in another post named “Optimize Database Queries”. You can read it clicking here.

# But, long story short: Django relationships are lazy. Meaning Django will only query the database if you access one of the related properties. Sometimes it causes some undesired effects, like firing hundreds or thousands of queries. This problem can be mitigated using the select_related method.

# Knowing beforehand you will need to access a related data, you can prefetch it in a single database query:

users = User.objects.all().select_related('profile')