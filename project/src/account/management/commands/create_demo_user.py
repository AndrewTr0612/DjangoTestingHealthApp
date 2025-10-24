"""
Django management command to create a demo user with sample health data
Usage: python manage.py create_demo_user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account.models import UserProfile, WeightEntry, WeightGoal
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Creates a demo user with sample health tracking data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing demo user if exists and create a new one',
        )

    def handle(self, *args, **options):
        username = 'demo'
        email = 'demo@healthtracker.com'
        password = 'demo123456'
        
        # Check if demo user already exists
        if User.objects.filter(username=username).exists():
            if options['reset']:
                self.stdout.write(self.style.WARNING('Deleting existing demo user...'))
                User.objects.get(username=username).delete()
            else:
                self.stdout.write(self.style.ERROR(
                    f'User "{username}" already exists. Use --reset to recreate.'
                ))
                return

        self.stdout.write('Creating demo user...')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='John',
            last_name='Doe'
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created user: {username}'))

        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            height_cm=175.0,  # 175 cm (5'9")
            date_of_birth=date(1990, 6, 15),  # 35 years old
            gender='M'
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created profile: Height {profile.height_cm}cm, Age {profile.age}'))

        # Create weight entries (90 days of data showing weight loss journey)
        today = date.today()
        starting_weight = 95.0  # kg (started at 95kg)
        target_weight = 80.0    # kg (goal is 80kg)
        
        self.stdout.write('Creating weight entries...')
        weight_entries = []
        
        # Generate weight data for the past 90 days
        # Simulating a realistic weight loss journey with some fluctuations
        for days_ago in range(90, -1, -1):
            entry_date = today - timedelta(days=days_ago)
            
            # Calculate progressive weight loss with realistic daily variations
            progress_ratio = (90 - days_ago) / 90  # 0 to 1
            base_weight = starting_weight - (starting_weight - target_weight - 3) * progress_ratio
            
            # Add realistic daily fluctuations (+/- 0.3kg)
            import random
            random.seed(days_ago)  # Consistent random values
            daily_variation = random.uniform(-0.3, 0.3)
            weight = round(base_weight + daily_variation, 1)
            
            # Add notes for specific milestones
            notes = ''
            if days_ago == 90:
                notes = 'Starting my weight loss journey! Excited to get healthier.'
            elif days_ago == 60:
                notes = 'Lost 5kg! Feeling more energetic and motivated.'
            elif days_ago == 30:
                notes = 'Halfway to my goal! Clothes fitting better.'
            elif days_ago == 7:
                notes = 'One week progress check - staying consistent!'
            elif days_ago == 0:
                notes = 'Current weight - making great progress!'
            
            # Create entry every 3 days to avoid too much data
            if days_ago % 3 == 0 or days_ago <= 7:  # More frequent entries in last week
                weight_entry = WeightEntry.objects.create(
                    user=user,
                    weight_kg=weight,
                    recorded_date=entry_date,
                    notes=notes
                )
                weight_entries.append(weight_entry)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(weight_entries)} weight entries'))
        
        # Get current weight (latest entry)
        current_weight = weight_entries[-1].weight_kg
        
        # Display some statistics
        first_weight = weight_entries[0].weight_kg
        weight_lost = first_weight - current_weight
        self.stdout.write(self.style.SUCCESS(
            f'  Starting weight: {first_weight:.1f}kg → Current weight: {current_weight:.1f}kg'
        ))
        self.stdout.write(self.style.SUCCESS(f'  Total weight lost: {weight_lost:.1f}kg'))

        # Create weight goal
        goal_start_date = today - timedelta(days=90)
        goal = WeightGoal.objects.create(
            user=user,
            goal_type='lose',
            target_weight_kg=target_weight,
            pace='moderate',  # 0.5 kg/week
            start_date=goal_start_date,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(
            f'✓ Created weight goal: Lose weight to {target_weight:.1f}kg (Moderate pace)'
        ))
        
        # Calculate progress
        progress = goal.get_progress_percentage(current_weight)
        weeks_remaining = goal.calculate_timeline(current_weight)
        
        self.stdout.write(self.style.SUCCESS(f'  Goal progress: {progress}%'))
        self.stdout.write(self.style.SUCCESS(f'  Estimated weeks to goal: {weeks_remaining}'))

        # Display demo user credentials
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Demo user created successfully!'))
        self.stdout.write('='*60)
        self.stdout.write(self.style.WARNING('Login Credentials:'))
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Password: {password}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('\nDemo User Profile:'))
        self.stdout.write(f'  Name: {user.first_name} {user.last_name}')
        self.stdout.write(f'  Age: {profile.age} years old')
        self.stdout.write(f'  Height: {profile.height_cm} cm')
        self.stdout.write(f'  Gender: {profile.get_gender_display()}')
        self.stdout.write(f'  Current Weight: {current_weight:.1f} kg')
        self.stdout.write(f'  Current BMI: {weight_entries[-1].bmi} ({weight_entries[-1].bmi_category})')
        self.stdout.write(f'  Weight Goal: {target_weight:.1f} kg')
        self.stdout.write(f'  Progress: {progress}% complete')
        self.stdout.write('='*60)
