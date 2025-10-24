from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class UserProfile(models.Model):
    """Extended user profile with health information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    height_cm = models.FloatField(
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        help_text="Height in centimeters"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='O')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = datetime.today().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class WeightEntry(models.Model):
    """Track user's weight over time"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    weight_kg = models.FloatField(
        validators=[MinValueValidator(20), MaxValueValidator(500)],
        help_text="Weight in kilograms"
    )
    recorded_date = models.DateField(default=datetime.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_date', '-created_at']
        verbose_name = "Weight Entry"
        verbose_name_plural = "Weight Entries"

    def __str__(self):
        return f"{self.user.username} - {self.weight_kg}kg on {self.recorded_date}"

    @property
    def bmi(self):
        """Calculate BMI if user has a profile with height"""
        if hasattr(self.user, 'profile') and self.user.profile.height_cm:
            height_m = self.user.profile.height_cm / 100
            bmi_value = self.weight_kg / (height_m ** 2)
            return round(bmi_value, 2)
        return None

    @property
    def bmi_category(self):
        """Get BMI category"""
        bmi = self.bmi
        if bmi is None:
            return "Unknown"
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class WeightGoal(models.Model):
    """User's weight goal and preferences"""
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('gain', 'Gain Weight'),
        ('maintain', 'Maintain Weight'),
    ]
    
    PACE_CHOICES = [
        ('slow', 'Slow (0.25 kg/week)'),
        ('moderate', 'Moderate (0.5 kg/week)'),
        ('fast', 'Fast (1 kg/week)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='weight_goal')
    goal_type = models.CharField(max_length=10, choices=GOAL_CHOICES)
    target_weight_kg = models.FloatField(
        validators=[MinValueValidator(20), MaxValueValidator(500)],
        help_text="Target weight in kilograms"
    )
    pace = models.CharField(max_length=10, choices=PACE_CHOICES, default='moderate')
    start_date = models.DateField(default=datetime.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Weight Goal"
        verbose_name_plural = "Weight Goals"

    def __str__(self):
        return f"{self.user.username}'s Goal: {self.get_goal_type_display()} to {self.target_weight_kg}kg"

    def get_weekly_rate(self):
        """Get weekly weight change rate in kg"""
        rates = {
            'slow': 0.25,
            'moderate': 0.5,
            'fast': 1.0,
        }
        return rates.get(self.pace, 0.5)

    def calculate_timeline(self, current_weight):
        """Calculate estimated weeks to reach goal"""
        if not current_weight:
            return None
        
        weight_diff = abs(self.target_weight_kg - current_weight)
        weekly_rate = self.get_weekly_rate()
        
        if weekly_rate == 0:
            return None
        
        weeks = weight_diff / weekly_rate
        return round(weeks, 1)

    def get_target_date(self, current_weight):
        """Calculate estimated date to reach goal"""
        weeks = self.calculate_timeline(current_weight)
        if weeks:
            target_date = self.start_date + timedelta(weeks=weeks)
            return target_date
        return None

    def get_progress_percentage(self, current_weight):
        """Calculate progress towards goal"""
        # Get the first weight entry after goal was set
        start_entries = self.user.weight_entries.filter(
            recorded_date__gte=self.start_date
        ).order_by('recorded_date')
        
        if not start_entries.exists():
            return 0
        
        start_weight = start_entries.first().weight_kg
        weight_diff_total = abs(self.target_weight_kg - start_weight)
        
        if weight_diff_total == 0:
            return 100
        
        weight_diff_current = abs(current_weight - start_weight)
        progress = (weight_diff_current / weight_diff_total) * 100
        return min(round(progress, 1), 100)


class ChatMessage(models.Model):
    """Store chat messages between user and AI"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"