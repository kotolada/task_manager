from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Task

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs) 
        # Calling the __init__ method of base class. It allows
        # a child class to inherit and extend the functionality
        # of its parent class without having to rewrite code.
            
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
    '<li>Your password must contain at least 8 characters.</li>'
    '<li>Your password can’t be entirely numeric.</li>'
    '</ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Repeat Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted">Enter the same password as before, for verification.</span>'

class AddTaskForm(forms.ModelForm):
    task_name = forms.CharField(label='Task Name',
                                max_length=100,
                                required=True, 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control', 'placeholder':'Task Name'}
                                    )
                                )
    task_description = forms.CharField(label='Task Description',
                                       required=False,
                                       widget=forms.Textarea(
                                            attrs={'class':'form-control', 'placeholder':'Task Description', 'style':"height: 200px"}
                                            )
                                        )
    due_date = forms.DateTimeField(label='Due Date',
                                   required=False,
                                   widget=forms.DateTimeInput(
                                       attrs={'class':'form-control', 'type': 'datetime-local'}
                                       )
                                    )

    class Meta:
        model = Task
        exclude = ('task_status', 'user',)
