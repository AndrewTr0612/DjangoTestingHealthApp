"""
Quick script to view demo user information
Usage: python manage.py shell < view_demo_user.py
"""
from django.contrib.auth.models import User
from account.models import WeightEntry, WeightGoal, UserProfile

print("\n" + "="*70)
print("DEMO USER INFORMATION")
print("="*70)

try:
    user = User.objects.get(username='demo')
    
    print(f"\n📋 LOGIN CREDENTIALS")
    print(f"   Username: demo")
    print(f"   Password: demo123456")
    print(f"   Email: {user.email}")
    
    print(f"\n👤 USER PROFILE")
    print(f"   Name: {user.first_name} {user.last_name}")
    if hasattr(user, 'profile'):
        profile = user.profile
        print(f"   Age: {profile.age} years old")
        print(f"   Height: {profile.height_cm} cm")
        print(f"   Gender: {profile.get_gender_display()}")
    
    print(f"\n⚖️  WEIGHT TRACKING")
    weight_entries = user.weight_entries.all()
    if weight_entries.exists():
        first_entry = weight_entries.last()
        latest_entry = weight_entries.first()
        print(f"   Total entries: {weight_entries.count()}")
        print(f"   First entry: {first_entry.weight_kg:.1f} kg on {first_entry.recorded_date}")
        print(f"   Latest entry: {latest_entry.weight_kg:.1f} kg on {latest_entry.recorded_date}")
        print(f"   Weight change: {first_entry.weight_kg - latest_entry.weight_kg:.1f} kg")
        print(f"   Current BMI: {latest_entry.bmi} ({latest_entry.bmi_category})")
    
    print(f"\n🎯 WEIGHT GOAL")
    if hasattr(user, 'weight_goal'):
        goal = user.weight_goal
        print(f"   Goal type: {goal.get_goal_type_display()}")
        print(f"   Target weight: {goal.target_weight_kg:.1f} kg")
        print(f"   Pace: {goal.get_pace_display()}")
        print(f"   Start date: {goal.start_date}")
        
        if weight_entries.exists():
            current_weight = weight_entries.first().weight_kg
            progress = goal.get_progress_percentage(current_weight)
            weeks = goal.calculate_timeline(current_weight)
            print(f"   Current progress: {progress}%")
            print(f"   Weeks to goal: {weeks}")
            print(f"   Weight to lose: {current_weight - goal.target_weight_kg:.1f} kg")
    
    print(f"\n📊 RECENT WEIGHT ENTRIES (Last 5)")
    for entry in weight_entries[:5]:
        note_preview = f" - {entry.notes[:40]}..." if entry.notes else ""
        print(f"   {entry.recorded_date}: {entry.weight_kg:.1f} kg{note_preview}")
    
    print("\n" + "="*70)
    print("✅ Demo user is ready to use!")
    print("   Login at: http://localhost:8000/")
    print("="*70 + "\n")

except User.DoesNotExist:
    print("\n❌ Demo user not found!")
    print("   Create one by running: python manage.py create_demo_user")
    print("="*70 + "\n")
