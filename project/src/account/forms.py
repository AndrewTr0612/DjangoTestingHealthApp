from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from .models import UserProfile, WeightEntry, WeightGoal


class UserUpdateForm(forms.ModelForm):
    """Form for updating user's name and email"""
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        # Add placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['height_cm', 'date_of_birth', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'height_cm': forms.NumberInput(attrs={
                'placeholder': 'e.g., 170',
                'class': 'form-control',
                'step': '0.1'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False


class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight_kg', 'recorded_date', 'notes']
        widgets = {
            'recorded_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().isoformat()  # Prevent selecting future dates
            }),
            'weight_kg': forms.NumberInput(attrs={
                'placeholder': 'e.g., 70.5',
                'step': '0.1',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Optional notes...',
                'class': 'form-control'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        # Update max date dynamically
        self.fields['recorded_date'].widget.attrs['max'] = date.today().isoformat()
    
    def clean_recorded_date(self):
        """Validate that recorded_date is not in the future"""
        recorded_date = self.cleaned_data.get('recorded_date')
        if recorded_date and recorded_date > date.today():
            raise ValidationError('Weight entry date cannot be in the future. Please select today or an earlier date.')
        return recorded_date


class WeightGoalForm(forms.ModelForm):
    class Meta:
        model = WeightGoal
        fields = ['goal_type', 'target_weight_kg', 'pace', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'target_weight_kg': forms.NumberInput(attrs={
                'placeholder': 'e.g., 65',
                'step': '0.1',
                'class': 'form-control'
            }),
            'goal_type': forms.Select(attrs={'class': 'form-control'}),
            'pace': forms.Select(attrs={'class': 'form-control'}),
        }