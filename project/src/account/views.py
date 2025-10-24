from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile, WeightEntry, WeightGoal, ChatMessage
from .forms import UserRegistrationForm, UserProfileForm, WeightEntryForm, WeightGoalForm, UserUpdateForm
from chatbox.gpt import ChatGPTService
import json


def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please set up your profile.')
            return redirect('accounts:profile_setup')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle user login - Home page"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Show full name if available, otherwise show username
            display_name = user.get_full_name() if user.get_full_name() else (user.first_name if user.first_name else username)
            messages.success(request, f'Welcome back, {display_name}!')
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_setup_view(request):
    """Setup or update user profile"""
    try:
        profile = request.user.profile
        is_new = False
    except UserProfile.DoesNotExist:
        profile = None
        is_new = True
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            
            # If new profile, redirect to add first weight entry
            if is_new:
                messages.info(request, 'Now add your current weight to get started.')
                return redirect('accounts:add_weight')
            return redirect('accounts:dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'is_new': is_new
    }
    return render(request, 'accounts/profile_setup.html', context)


@login_required
def edit_profile_view(request):
    """Edit user's name and email"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def dashboard_view(request):
    """Main dashboard showing user's health data and progress"""
    # Check if user has a profile
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'Please complete your profile first.')
        return redirect('accounts:profile_setup')
    
    # Get latest weight entry
    latest_weight = request.user.weight_entries.first()
    
    # Get weight goal
    try:
        weight_goal = request.user.weight_goal
    except WeightGoal.DoesNotExist:
        weight_goal = None
    
    # Get recent weight entries for chart (last 30 entries)
    weight_history = request.user.weight_entries.all()[:30]
    
    # Prepare chart data
    chart_data = {
        'dates': [entry.recorded_date.strftime('%Y-%m-%d') for entry in reversed(weight_history)],
        'weights': [float(entry.weight_kg) for entry in reversed(weight_history)],
    }
    
    # Calculate timeline if goal exists
    timeline_data = None
    if weight_goal and latest_weight:
        current_weight = latest_weight.weight_kg
        weeks_to_goal = weight_goal.calculate_timeline(current_weight)
        target_date = weight_goal.get_target_date(current_weight)
        progress = weight_goal.get_progress_percentage(current_weight)
        
        timeline_data = {
            'current_weight': current_weight,
            'target_weight': weight_goal.target_weight_kg,
            'weight_difference': abs(weight_goal.target_weight_kg - current_weight),
            'weeks_to_goal': weeks_to_goal,
            'target_date': target_date,
            'progress': progress,
            'bmi': latest_weight.bmi,
            'bmi_category': latest_weight.bmi_category,
            'weekly_rate': weight_goal.get_weekly_rate(),
        }
    
    context = {
        'profile': request.user.profile,
        'latest_weight': latest_weight,
        'weight_goal': weight_goal,
        'weight_history': weight_history,
        'chart_data': chart_data,
        'timeline_data': timeline_data,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def add_weight_view(request):
    """Add a new weight entry"""
    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.save()
            messages.success(request, 'Weight entry added successfully!')
            return redirect('accounts:dashboard')
    else:
        form = WeightEntryForm()
    
    return render(request, 'accounts/add_weight.html', {'form': form})


@login_required
def set_goal_view(request):
    """Set or update weight goal"""
    try:
        goal = request.user.weight_goal
        is_new = False
    except WeightGoal.DoesNotExist:
        goal = None
        is_new = True
    
    if request.method == 'POST':
        form = WeightGoalForm(request.POST, instance=goal)
        if form.is_valid():
            weight_goal = form.save(commit=False)
            weight_goal.user = request.user
            weight_goal.save()
            
            msg = 'Weight goal set successfully!' if is_new else 'Weight goal updated successfully!'
            messages.success(request, msg)
            return redirect('accounts:dashboard')
    else:
        form = WeightGoalForm(instance=goal)
    
    # Get latest weight for reference
    latest_weight = request.user.weight_entries.first()
    
    context = {
        'form': form,
        'is_new': is_new,
        'latest_weight': latest_weight
    }
    return render(request, 'accounts/set_goal.html', context)


@login_required
def chatbot_view(request):
    """AI chatbot for health advice"""
    # GET request - show chat interface
    recent_messages = request.user.chat_messages.all()[:20]
    
    context = {
        'recent_messages': recent_messages
    }
    return render(request, 'accounts/chatbot.html', context)


@login_required
@require_POST
def chatbot_api_view(request):
    """API endpoint for chatbot messages"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Get response from ChatGPT
        gpt_service = ChatGPTService()
        response = gpt_service.get_response(user_message, request.user)
        
        # Save chat message
        chat_message = ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=response
        )
        
        return JsonResponse({
            'success': True,
            'response': response,
            'timestamp': chat_message.created_at.isoformat()
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
