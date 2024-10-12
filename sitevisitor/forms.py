from django import forms
from django.contrib.auth.forms import UserCreationForm
from userpanel.models import User_Table, GENDER_CHOICES
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Phone',
        })
    )
    profile_description = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Profile description',
            'style': 'height:100px',
            'rows': 3,
        })
    )
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    id_proof = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)  # Save the User model instance
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()  # Save the user to the database

            # Create the related User_Table instance
            user_table = User_Table.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                profile_description=self.cleaned_data.get('profile_description', ''),
                profile_image=self.cleaned_data.get('profile_image', None),
                id_proof=self.cleaned_data.get('id_proof', None),
                gender=self.cleaned_data['gender']
            )
            user_table.save()  # Save the User_Table instance

        return user
