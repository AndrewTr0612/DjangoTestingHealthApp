import random
import logging

logger = logging.getLogger(__name__)


class ChatGPTService:
    """Health advice chatbot without AI - provides curated health tips and resources"""
    
    def __init__(self):
        self.diet_tips = [
            "🥗 Try meal prepping on Sundays! Prepare grilled chicken, brown rice, and roasted vegetables for the week.",
            "🍎 Start your day with a protein-rich breakfast - eggs, Greek yogurt, or a protein smoothie.",
            "💧 Drink at least 8 glasses of water daily. Add lemon or cucumber for flavor!",
            "🥑 Include healthy fats: avocados, nuts, olive oil, and fatty fish like salmon.",
            "🍽️ Use smaller plates to control portion sizes naturally.",
            "🥦 Fill half your plate with vegetables at every meal.",
            "🚫 Avoid sugary drinks - they add empty calories without making you feel full.",
            "🍗 Lean proteins: chicken breast, turkey, fish, tofu, and legumes.",
            "🌾 Choose whole grains: brown rice, quinoa, oats, and whole wheat bread.",
            "⏰ Don't skip meals - eat every 3-4 hours to maintain metabolism.",
        ]
        
        self.workout_tips = [
            "🏃 Beginner workout: 30 min walk daily + 10 push-ups + 20 squats + 30 sec plank",
            "💪 Strength training 3x/week helps build muscle and boost metabolism.",
            "🏋️ Full body workout: Squats, Push-ups, Lunges, Rows, Planks - 3 sets of 10 reps each.",
            "🚴 Cardio options: Running, cycling, swimming, or dancing - 150 min/week.",
            "🧘 Don't forget rest days! Your muscles need time to recover and grow.",
            "⚡ HIIT workout: 30 sec sprint + 30 sec rest, repeat 10 times = quick fat burn!",
            "🏃‍♀️ Mix it up: Combine cardio, strength training, and flexibility exercises.",
            "📱 Follow fitness YouTubers: FitnessBlender, POPSUGAR Fitness, Chloe Ting.",
            "🎯 Progressive overload: Gradually increase weight, reps, or intensity each week.",
            "🤸 Bodyweight exercises: Perfect for home workouts - no equipment needed!",
        ]
        
        self.meal_prep_ideas = [
            "🍱 Meal Prep Idea: Chicken teriyaki bowls - chicken, broccoli, carrots, and brown rice.",
            "🥘 Batch cook chili or soup - freeze in portions for quick healthy meals.",
            "🍳 Prep breakfast: Overnight oats with berries, chia seeds, and almond butter.",
            "🥙 Make wraps: Whole wheat tortilla + hummus + grilled veggies + protein.",
            "🍝 Healthy pasta: Whole grain pasta + marinara + lean ground turkey + vegetables.",
            "🥗 Mason jar salads: Layer dressing, hard veggies, protein, greens (lasts 5 days!).",
            "🍗 Baked protein: Season 5 chicken breasts, bake at 375°F for 25 min, divide for week.",
            "🥕 Pre-cut veggies: Wash and chop carrots, celery, peppers for easy snacking.",
            "🍚 Rice cooker hack: Make a big batch of brown rice/quinoa on Sunday.",
            "🫙 Portion control: Use meal prep containers to pre-portion your meals.",
        ]
        
        self.youtube_channels = [
            "📺 Chloe Ting - Free workout programs and abs challenges",
            "📺 FitnessBlender - 500+ free workout videos for all levels",
            "📺 POPSUGAR Fitness - Dance cardio and fun workouts",
            "📺 Yoga with Adriene - Yoga for beginners to advanced",
            "📺 Athlean-X - Science-based fitness and nutrition",
            "📺 Blogilates - Pilates and fitness challenges",
            "📺 MadFit - No jumping apartment-friendly workouts",
            "📺 The Body Coach TV - HIIT workouts with Joe Wicks",
            "📺 HASfit - Free complete workout programs",
            "📺 Pamela Reif - No talking, music-only workouts",
        ]
        
        self.motivational_quotes = [
            "💪 'The only bad workout is the one that didn't happen.'",
            "🎯 'Progress, not perfection. Small steps lead to big changes!'",
            "⭐ 'Your body can do it. It's your mind you need to convince.'",
            "🔥 'Don't wish for it. Work for it!'",
            "🌟 'You're one workout away from a better mood.'",
            "💯 'Consistency is key. Show up every day, even when it's hard.'",
            "🏆 'Believe in yourself and you will be unstoppable!'",
            "🚀 'Your health is an investment, not an expense.'",
            "💎 'Take care of your body. It's the only place you have to live.'",
            "✨ 'Every meal is a chance to fuel your body right!'",
        ]
    
    def get_health_context(self, user):
        """Build context about user's health data"""
        context = []
        
        if hasattr(user, 'profile'):
            profile = user.profile
            context.append(f"📊 Your Profile: Height {profile.height_cm}cm, {profile.get_gender_display()}")
            if profile.age:
                context.append(f"Age: {profile.age} years")
        
        latest_weight = user.weight_entries.first()
        if latest_weight:
            context.append(f"⚖️ Current: {latest_weight.weight_kg}kg, BMI: {latest_weight.bmi} ({latest_weight.bmi_category})")
        
        if hasattr(user, 'weight_goal'):
            goal = user.weight_goal
            context.append(f"�� Goal: {goal.get_goal_type_display()} to {goal.target_weight_kg}kg")
            
            if latest_weight:
                weeks_to_goal = goal.calculate_timeline(latest_weight.weight_kg)
                if weeks_to_goal:
                    context.append(f"⏱️ Timeline: {weeks_to_goal} weeks to goal")
        
        return "\n".join(context) if context else ""
    
    def get_response(self, user_message, user):
        """Get health advice based on user's question"""
        
        message_lower = user_message.lower()
        
        # Build personalized context
        context = self.get_health_context(user)
        response_parts = []
        
        if context:
            response_parts.append(context)
            response_parts.append("")
        
        # Diet and nutrition queries
        if any(word in message_lower for word in ['diet', 'eat', 'food', 'nutrition', 'meal', 'calorie', 'hungry']):
            response_parts.append("🍽️ NUTRITION ADVICE:")
            response_parts.extend(random.sample(self.diet_tips, 3))
            response_parts.append("")
            response_parts.append("📌 MEAL PREP IDEAS:")
            response_parts.extend(random.sample(self.meal_prep_ideas, 2))
        
        # Workout and exercise queries
        elif any(word in message_lower for word in ['workout', 'exercise', 'gym', 'train', 'cardio', 'strength', 'fitness', 'muscle']):
            response_parts.append("💪 WORKOUT TIPS:")
            response_parts.extend(random.sample(self.workout_tips, 3))
            response_parts.append("")
            response_parts.append("📺 RECOMMENDED CHANNELS:")
            response_parts.extend(random.sample(self.youtube_channels, 3))
        
        # Weight loss queries
        elif any(word in message_lower for word in ['lose weight', 'weight loss', 'fat', 'slim', 'reduce']):
            response_parts.append("🎯 WEIGHT LOSS TIPS:")
            response_parts.append("• Create a calorie deficit: burn more than you consume")
            response_parts.append("• Aim for 0.5-1kg loss per week (safe and sustainable)")
            response_parts.append("• Combine cardio + strength training for best results")
            response_parts.append("")
            response_parts.extend(random.sample(self.diet_tips, 2))
            response_parts.append("")
            response_parts.extend(random.sample(self.workout_tips, 2))
        
        # Weight gain queries
        elif any(word in message_lower for word in ['gain weight', 'weight gain', 'bulk', 'muscle gain']):
            response_parts.append("💪 WEIGHT GAIN TIPS:")
            response_parts.append("• Eat in a calorie surplus: consume more than you burn")
            response_parts.append("• Focus on protein: 1.6-2.2g per kg body weight")
            response_parts.append("• Lift heavy weights 4-5x per week")
            response_parts.append("• Eat every 3-4 hours, include protein at each meal")
            response_parts.append("• Track your calories and progressively increase")
        
        # Meal prep queries
        elif any(word in message_lower for word in ['meal prep', 'prepare', 'cooking', 'recipe']):
            response_parts.append("🍱 MEAL PREP GUIDE:")
            response_parts.extend(self.meal_prep_ideas[:5])
            response_parts.append("")
            response_parts.append("💡 Pro tip: Invest in good containers and prep on Sundays!")
        
        # YouTube/video queries
        elif any(word in message_lower for word in ['youtube', 'video', 'channel', 'watch']):
            response_parts.append("📺 TOP FITNESS CHANNELS:")
            response_parts.extend(self.youtube_channels[:7])
            response_parts.append("")
            response_parts.append("💡 Search YouTube for: 'home workout no equipment' or 'beginner HIIT'")
        
        # Motivation queries
        elif any(word in message_lower for word in ['motivat', 'inspire', 'give up', 'tired', 'hard', 'difficult']):
            response_parts.append("⭐ YOU'VE GOT THIS!")
            response_parts.extend(random.sample(self.motivational_quotes, 4))
            response_parts.append("")
            response_parts.append("Remember: Every expert was once a beginner. Keep going! 💪")
        
        # BMI queries
        elif any(word in message_lower for word in ['bmi', 'body mass', 'healthy weight']):
            latest_weight = user.weight_entries.first()
            if latest_weight and latest_weight.bmi:
                response_parts.append(f"📊 Your BMI: {latest_weight.bmi} ({latest_weight.bmi_category})")
                response_parts.append("")
                if latest_weight.bmi_category == "Underweight":
                    response_parts.append("• Focus on gaining muscle mass through strength training")
                    response_parts.append("• Eat calorie-dense foods: nuts, avocados, whole milk")
                elif latest_weight.bmi_category == "Overweight" or latest_weight.bmi_category == "Obese":
                    response_parts.append("• Focus on sustainable weight loss: 0.5-1kg/week")
                    response_parts.append("• Combine cardio and strength training")
                    response_parts.append("• Track your food intake and create a calorie deficit")
                else:
                    response_parts.append("✅ Great! Maintain with balanced diet and regular exercise")
            else:
                response_parts.append("Add your weight first to calculate BMI!")
        
        # General greeting
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'help']):
            response_parts.append("👋 Hello! I'm your Health Tracker assistant!")
            response_parts.append("")
            response_parts.append("I can help you with:")
            response_parts.append("• 🍽️ Diet and nutrition advice")
            response_parts.append("• 💪 Workout plans and tips")
            response_parts.append("• 🍱 Meal prep ideas")
            response_parts.append("• 📺 YouTube fitness channels")
            response_parts.append("• ⭐ Motivation and tips")
            response_parts.append("")
            response_parts.append("Ask me anything about fitness, diet, workouts, or meal planning!")
        
        # Default response
        else:
            response_parts.append("🏥 GENERAL HEALTH TIPS:")
            response_parts.extend(random.sample(self.diet_tips, 2))
            response_parts.append("")
            response_parts.extend(random.sample(self.workout_tips, 2))
            response_parts.append("")
            response_parts.append("💡 Ask me about: diet, workouts, meal prep, or motivation!")
        
        return "\n".join(response_parts)
