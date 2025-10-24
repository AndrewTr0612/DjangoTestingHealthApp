from django.contrib import admin
from .models import UserProfile, WeightEntry, WeightGoal, ChatMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'height_cm', 'gender', 'age', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Physical Information', {
            'fields': ('height_cm', 'gender', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight_kg', 'bmi', 'bmi_category', 'recorded_date', 'created_at']
    list_filter = ['recorded_date', 'created_at']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'recorded_date'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Weight Data', {
            'fields': ('weight_kg', 'recorded_date', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeightGoal)
class WeightGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_type', 'target_weight_kg', 'pace', 'is_active', 'start_date']
    list_filter = ['goal_type', 'pace', 'is_active', 'start_date']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Goal Settings', {
            'fields': ('goal_type', 'target_weight_kg', 'pace', 'start_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'short_message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'message', 'response']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
