# 🚀 Health Tracker - Quick Start Guide

Get up and running with Health Tracker in **5 minutes**!

---

## ⚡ Quick Setup (Linux/Mac)

```bash
# 1. Clone and navigate
git clone https://github.com/AndrewTr0612/DjangoTestingHealthApp.git
cd DjangoTestingHealthApp/project

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r src/requirements.txt

# 4. Setup database
cd src
python manage.py migrate

# 5. Start server
python manage.py runserver

# 6. Open http://localhost:8000 in your browser
```

---

## ⚡ Quick Setup (Windows)

```cmd
# 1. Clone and navigate
git clone https://github.com/AndrewTr0612/DjangoTestingHealthApp.git
cd DjangoTestingHealthApp\project

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r src\requirements.txt

# 4. Setup database
cd src
python manage.py migrate

# 5. Start server
python manage.py runserver

# 6. Open http://localhost:8000 in your browser
```

---

## 📋 Step-by-Step Instructions

### Step 1: Clone Repository
```bash
git clone https://github.com/AndrewTr0612/DjangoTestingHealthApp.git
cd DjangoTestingHealthApp
```

### Step 2: Navigate to Project
```bash
cd project
```

### Step 3: Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Step 4: Install Requirements
```bash
pip install -r src/requirements.txt
```

**Dependencies installed:**
- Django 5.2.7
- python-decouple 3.8
- Other core libraries

### Step 5: Setup Environment (Optional)
```bash
cd src
```

Create `.env` file (optional - has defaults):
```env
SECRET_KEY=django-insecure-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Step 6: Run Database Migrations
```bash
python manage.py migrate
```

This creates:
- User tables
- UserProfile
- WeightEntry
- WeightGoal
- ChatMessage

### Step 7: Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### Step 8: Start Development Server
```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 9: Open in Browser
Navigate to: **http://localhost:8000**

---

## 🎯 First Steps in the App

### 1. Register Your Account
1. Click "Register" button
2. Choose username and password
3. Enter email (optional)
4. Click "Sign Up"

### 2. Setup Your Profile
1. Enter your height (cm)
2. Select gender
3. Enter date of birth (optional)
4. Click "Save Profile"

### 3. Add First Weight Entry
1. Click "Add Weight" in navbar
2. Enter current weight (kg)
3. Add notes if desired
4. Click "Add Weight Entry"

### 4. Set Your Goal
1. Click "Set Goal" in navbar
2. Choose goal type:
   - Lose Weight
   - Gain Weight
   - Maintain Weight
3. Enter target weight
4. Select pace (slow/moderate/fast)
5. View timeline calculation
6. Click "Set Goal"

### 5. View Dashboard
- See current weight & BMI
- View progress to goal
- Check weight trend chart
- Monitor timeline

### 6. Try the Chatbox
1. Click blue chat button (bottom-right)
2. Ask questions:
   - "What should I eat?"
   - "Give me workout tips"
   - "Show meal prep ideas"
   - "I need motivation"

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8080

# Or kill process on port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
# Make sure virtual environment is activated
# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Reinstall requirements
pip install -r src/requirements.txt
```

### Database Errors
```bash
# Delete database and recreate
rm db.sqlite3
rm -rf account/migrations/0*.py
rm -rf chatbox/migrations/0*.py

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

---

## 🔑 Admin Panel Access

1. Create superuser (if not done):
   ```bash
   python manage.py createsuperuser
   ```

2. Access admin panel:
   ```
   http://localhost:8000/admin
   ```

3. Login with superuser credentials

4. Manage:
   - Users
   - Profiles
   - Weight Entries
   - Goals
   - Chat Messages

---

## 📦 What's Included

### Features
✅ User authentication & registration  
✅ Profile management (name, email, height, DOB)  
✅ Weight tracking with history  
✅ Automatic BMI calculation  
✅ Goal setting with timeline calculator  
✅ Progress tracking dashboard  
✅ Interactive weight trend charts  
✅ Health advice chatbox (no API needed!)  
✅ Responsive design (mobile-friendly)  
✅ Floating chat widget  

### Pages
- **Login** - `/accounts/login/`
- **Register** - `/accounts/register/`
- **Dashboard** - `/accounts/dashboard/`
- **Edit Profile** - `/accounts/profile/edit/`
- **Add Weight** - `/accounts/weight/add/`
- **Set Goal** - `/accounts/goal/set/`
- **Admin Panel** - `/admin/`

---

## 🎨 Customization

### Change Theme Colors
Edit `templates/base.html`:
```css
:root {
    --primary-color: #667eea;  /* Change this */
    --secondary-color: #764ba2; /* And this */
}
```

### Modify Health Tips
Edit `chatbox/gpt.py`:
```python
self.diet_tips = [
    "Your custom diet tip here",
    # Add more...
]
```

### Add New Features
1. Create view in `account/views.py`
2. Add URL in `account/urls.py`
3. Create template in `templates/accounts/`
4. Update navbar in `templates/base.html`

---

## 📚 Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Bootstrap Docs**: https://getbootstrap.com/docs/
- **Chart.js Docs**: https://www.chartjs.org/docs/

---

## 🐛 Common Issues

### Issue: "No module named 'decouple'"
**Solution:**
```bash
pip install python-decouple
```

### Issue: "CSRF verification failed"
**Solution:** Make sure you're using `{% csrf_token %}` in all forms

### Issue: Charts not showing
**Solution:** Check browser console for JavaScript errors. Make sure Chart.js CDN is accessible.

### Issue: Login redirects to profile setup repeatedly
**Solution:** Complete all required profile fields (height, gender)

---

## ✅ You're All Set!

Your Health Tracker is now running at **http://localhost:8000**

**Next Steps:**
1. ✅ Register your account
2. ✅ Setup your profile  
3. ✅ Add your first weight entry
4. ✅ Set a goal
5. ✅ Start tracking your progress!

---

## 💡 Pro Tips

- **Track daily** for best results
- **Set realistic goals** (0.5-1kg/week)
- **Use the chatbox** for motivation
- **Check dashboard** weekly
- **Try meal prep** ideas from chatbox
- **Follow YouTube** channels recommended

---

## 🎉 Happy Tracking!

You're ready to start your health journey! 💪

For detailed documentation, see [README.md](README.md)

**Questions?** Open an issue on GitHub!
