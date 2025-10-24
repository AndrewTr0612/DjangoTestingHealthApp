# 🏥 Health Tracker - Django Web Application

A comprehensive health and fitness tracking web application built with Django. Track your weight, set goals, monitor progress, and get personalized health advice!

![Django](https://img.shields.io/badge/Django-5.2.7-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 🔐 User Authentication
- **Secure Registration & Login** - Create your account and log in securely
- **Profile Management** - Edit your name, email, and personal information
- **Password Protection** - Django's built-in authentication system

### ⚖️ Weight Tracking
- **Record Weight Entries** - Track your weight over time with dates and notes
- **Weight History** - View all your past weight entries in a clean table
- **BMI Calculation** - Automatic BMI calculation and categorization
- **Progress Charts** - Beautiful Chart.js line graphs showing weight trends

### 🎯 Goal Setting
- **Set Weight Goals** - Define your target weight (lose, gain, or maintain)
- **Choose Your Pace** - Slow, moderate, or fast weight loss/gain plans
- **Timeline Calculator** - Automatic calculation of:
  - Weeks to goal
  - Target completion date
  - Current progress percentage
  - Weekly weight change rate

### 📊 Dashboard
- **Overview Statistics** - Current weight, BMI, target weight, height
- **Progress Tracking** - Visual progress bars and circular progress indicators
- **Weight Trend Chart** - Interactive line chart showing your weight over time
- **Goal Timeline** - See how close you are to achieving your goals

### 💬 Health Assistant Chatbox
- **Diet & Nutrition Advice** - Get curated tips on healthy eating
- **Meal Prep Ideas** - Practical meal planning and preparation guides
- **Workout Tips** - Exercise routines for all fitness levels
- **YouTube Recommendations** - Links to top fitness channels
- **Motivational Support** - Inspiring quotes and encouragement
- **Personalized Responses** - Advice based on your profile and goals

### 🎨 Modern UI/UX
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Bootstrap 5** - Clean, professional interface with gradients
- **Floating Chat Widget** - Facebook Messenger-style chat button
- **Smooth Animations** - Card hover effects and transitions
- **Color-Coded Stats** - Easy-to-read BMI categories with badges

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AndrewTr0612/DjangoTestingHealthApp.git
   cd DjangoTestingHealthApp
   ```

2. **Set Up Virtual Environment**
   ```bash
   cd project
   python -m venv .venv
   
   # On Linux/Mac:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cd src
   cp .env.example .env  # Or create .env file manually
   ```
   
   Edit `.env` file:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Open your browser and go to: `http://localhost:8000`
   - Register a new account or login
   - Start tracking your health!

---

## 📁 Project Structure

```
DjangoTestingHealthApp/
├── project/
│   ├── .venv/                  # Virtual environment
│   └── src/
│       ├── manage.py           # Django management script
│       ├── requirements.txt    # Python dependencies
│       ├── db.sqlite3         # SQLite database
│       ├── .env               # Environment variables
│       ├── account/           # Main app
│       │   ├── models.py      # Database models
│       │   ├── views.py       # View functions
│       │   ├── forms.py       # Django forms
│       │   ├── urls.py        # URL routing
│       │   └── admin.py       # Admin configuration
│       ├── chatbox/           # Chatbot functionality
│       │   ├── gpt.py         # Health advice service
│       │   └── views.py       # Chatbot views
│       ├── healthtracker/     # Project settings
│       │   ├── settings.py    # Django settings
│       │   ├── urls.py        # Main URL config
│       │   └── wsgi.py        # WSGI config
│       ├── templates/         # HTML templates
│       │   ├── base.html      # Base template
│       │   └── accounts/      # Account templates
│       └── static/            # Static files
│           ├── css/           # Stylesheets
│           └── js/            # JavaScript
├── README.md                  # This file
└── QUICKSTART.md             # Quick setup guide
```

---

## 💾 Database Models

### UserProfile
- User (OneToOne with Django User)
- Height (cm)
- Date of Birth
- Gender (Male/Female/Other)
- Auto-calculated Age

### WeightEntry
- User (ForeignKey)
- Weight (kg)
- Recorded Date
- Notes (optional)
- Auto-calculated BMI
- Auto-categorized BMI Category

### WeightGoal
- User (OneToOne)
- Goal Type (Lose/Gain/Maintain)
- Target Weight (kg)
- Pace (Slow/Moderate/Fast)
- Created Date
- Methods: calculate_timeline(), get_target_date(), get_progress_percentage()

### ChatMessage
- User (ForeignKey)
- Message
- Response
- Timestamp

---

## 🎯 How to Use

### 1. Register & Setup Profile
1. Click "Register" and create your account
2. Fill in your height, gender, and date of birth
3. Complete your profile setup

### 2. Add Your First Weight Entry
1. Navigate to "Add Weight"
2. Enter your current weight
3. Select the date (defaults to today)
4. Add optional notes

### 3. Set a Goal
1. Click "Set Goal"
2. Choose your goal type (lose/gain/maintain weight)
3. Enter your target weight
4. Select your preferred pace
5. View automatic timeline calculations

### 4. Track Progress
1. Visit your Dashboard to see:
   - Current weight and BMI
   - Progress towards goal
   - Weight trend chart
   - Timeline estimate
2. Add new weight entries regularly
3. Watch your progress graph update!

### 5. Get Health Advice
1. Click the blue chat button (bottom-right corner)
2. Ask questions like:
   - "What should I eat for weight loss?"
   - "Give me a workout plan"
   - "Show me meal prep ideas"
   - "I need motivation"
3. Get instant, curated health advice!

---

## 🛠️ Technologies Used

### Backend
- **Django 5.2.7** - Python web framework
- **SQLite** - Database (development)
- **Python 3.12** - Programming language

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Chart.js 4.4.0** - Interactive charts
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Client-side functionality

### Libraries
- **python-decouple** - Environment variable management
- **Django Auth** - User authentication
- **Django Forms** - Form handling

---

## 🎨 Screenshots

### Dashboard
View your health stats, progress, and weight trends in one place.

### Weight Tracking
Log your weight entries and see your progress over time with interactive charts.

### Goal Setting
Set realistic goals and get automatic timeline calculations.

### Health Assistant
Get instant advice on diet, workouts, and meal prep through the floating chatbox.

---

## 📝 Features in Detail

### BMI Calculation & Categories
- **Underweight**: BMI < 18.5
- **Normal**: BMI 18.5 - 24.9
- **Overweight**: BMI 25.0 - 29.9
- **Obese**: BMI ≥ 30.0

### Goal Timeline Calculator
- Calculates weeks to goal based on safe weight loss/gain rates
- **Slow pace**: 0.25 kg/week
- **Moderate pace**: 0.5 kg/week
- **Fast pace**: 1.0 kg/week
- Shows target completion date
- Tracks progress percentage

### Health Chatbot Topics
- **Diet**: Nutrition tips, calorie advice, healthy eating
- **Workouts**: Exercise routines, strength training, cardio
- **Meal Prep**: Weekly meal planning, batch cooking
- **YouTube**: Fitness channel recommendations
- **Motivation**: Inspirational quotes and support
- **BMI**: Personalized advice based on your BMI category

---

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing with Django's built-in system
- Login required decorators on sensitive views
- Session-based authentication
- XSS protection
- SQL injection prevention (Django ORM)

---

## 🌐 Deployment

### For Production:
1. Set `DEBUG=False` in `.env`
2. Generate a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL or MySQL instead of SQLite
5. Set up static file serving
6. Use a production WSGI server (Gunicorn, uWSGI)
7. Enable HTTPS
8. Configure proper logging

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Andrew**
- GitHub: [@AndrewTr0612](https://github.com/AndrewTr0612)

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Chart.js Contributors
- Stack Overflow Community
- All fitness YouTubers for inspiration

---

## 📞 Support

If you have any questions or run into issues:
1. Check the [QUICKSTART.md](QUICKSTART.md) guide
2. Review the code comments
3. Open an issue on GitHub
4. Contact the author

---

## 🎉 Happy Health Tracking!

Start your fitness journey today with Health Tracker! 💪🏥

**Remember**: Consistency is key. Small progress is still progress! 🌟
