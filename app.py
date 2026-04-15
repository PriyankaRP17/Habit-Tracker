import os
from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from collections import Counter
from datetime import datetime, timedelta, date

from models import db, User, Habit, HabitCompletion
from forms import LoginForm, RegisterForm, HabitForm
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

articles = [
    {
        "id": 1,
        "title": "5 Morning Habits to Boost Productivity",
        "summary": "Start your day with these actionable morning routines that improve focus and energy.",
        "content": """Starting your day with intentional habits sets the tone for success. Here are five morning habits to help you boost focus, energy, and productivity:

        Wake up early – Give yourself extra time before the day begins.
        Hydrate & eat a healthy breakfast – Fuel your body for optimal performance.
        Exercise or stretch – Get your blood flowing and mind alert.
        Plan your day – Write down the top 3 tasks you want to accomplish.
        Practice mindfulness – Meditation or journaling can reduce stress and increase focus.

        Implementing even a few of these habits consistently can transform your mornings and improve productivity. Over time, these small changes compound into significant improvements in your personal and professional life. Remember, consistency is more important than perfection—focus on building routines that are sustainable and enjoyable."""
    },
    {
        "id": 2,
        "title": "How to Build Consistent Habits",
        "summary": "Consistency is key! Learn practical strategies to stick to your routine habits and avoid burnout.",
        "content": """Building habits isn’t about motivation; it’s about consistency. Here’s how to stick to your routines and make them part of your lifestyle:

        Start small – Begin with tiny habits that are easy to maintain, such as drinking a glass of water every morning or writing a single sentence in a journal.
        Track your progress – Use HabitHive or a journal to log your streaks. Seeing your progress visually reinforces your commitment.
        Use reminders & triggers – Link habits to existing routines or set notifications. For example, do push-ups after brushing your teeth.
        Celebrate small wins – Reward yourself to reinforce positive behavior. Even small victories help maintain motivation.
        Don’t beat yourself up – Missing a day is normal; focus on getting back on track instead of feeling guilty.

        Consistency over time leads to automaticity—habits become part of your lifestyle, and positive behaviors stick. Patience and persistence are your best allies in building meaningful, lasting habits."""
    },
    {
        "id": 3,
        "title": "Mindfulness for Habit Success",
        "summary": "Discover how practicing mindfulness can help you maintain focus and improve habit retention.",
        "content": """Mindfulness is the practice of being fully present in the moment. Integrating mindfulness into your habit routine can improve focus, reduce stress, and prevent burnout. Here’s how to incorporate mindfulness:

        Be aware of triggers – Notice what prompts bad habits and replace them with better actions. Awareness is the first step to change.
        Slow down your actions – Pause before reacting. Mindful decision-making helps you choose behaviors aligned with your goals.
        Reflect daily – Take 5 minutes each evening to review your habit progress. Consider what went well and where you can improve.
        Visualize success – Picture yourself completing habits and reaching your goals. Visualization strengthens commitment and motivation.

        By practicing mindfulness, you strengthen your habit-building muscles and ensure every action is intentional. It’s not just about doing tasks, but doing them with focus, awareness, and purpose."""
    }
]

@app.route('/blog/<int:id>')
def blog_detail(id):
    article = next((a for a in articles if a["id"] == id), None)
    related_articles = [a for a in articles if a["id"] != id]
    if article:
        return render_template('blog_detail.html', article=article, related_articles=related_articles)
    else:
        return "Article not found", 404

@app.route("/")
def home():
    return render_template("dashboard.html", articles=articles)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard", articles=articles))
        else:
            flash("Invalid username or password")

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", articles=articles, user=current_user)

@app.route("/habit", methods=["GET", "POST"])
@login_required
def habit():
    form = HabitForm()
    recommended_habits = []

    weight = current_user.weight
    height = current_user.height
    age = current_user.age

    bmi_category = None
    age_category = None

    if weight and height:
        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Normal"
        elif bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

    if age:
        if age < 18:
            age_category = "Child/Teen"
        elif age <= 35:
            age_category = "Young Adult"
        elif age <= 55:
            age_category = "Adult"
        else:
            age_category = "Senior"

    if bmi_category in ["Overweight", "Obese"]:
        recommended_habits += ["Cardio", "Drink Water", "Meditation"]
    elif bmi_category == "Underweight":
        recommended_habits += ["Strength Training", "Balanced Meals"]

    if age_category in ["Child/Teen"]:
        recommended_habits += ["Story Reading", "Homework Routine"]
    elif age_category in ["Senior"]:
        recommended_habits += ["Gentle Walk", "Memory Games"]

    if form.validate_on_submit():
        habit_name = form.habit_name.data.strip() or form.habit_choice.data
        if not habit_name:
            flash("Please enter a habit or select one from the dropdown!", "danger")
            return redirect(url_for("habit"))

        if form.weight.data:
            current_user.weight = form.weight.data
        if form.height.data:
            current_user.height = form.height.data
        if form.age.data:
            current_user.age = form.age.data
        if form.gender.data:
            current_user.gender = form.gender.data
        db.session.commit()

        new_habit = Habit(
            user_id=current_user.id,
            habit_name=habit_name,
            frequency=form.frequency.data,
            duration=form.duration.data,
            preferred_time=form.preferred_time.data
        )
        db.session.add(new_habit)
        db.session.commit()
        flash("Habit added successfully!", "success")
        return redirect(url_for("habit"))

    habits = Habit.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "habit.html",
        form=form,
        habits=habits,
        recommended_habits=recommended_habits
    )

@app.route("/complete-habit/<int:habit_id>", methods=["POST"])
@login_required
def complete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()

    today = date.today()
    existing = HabitCompletion.query.filter_by(
        habit_id=habit.id, date=today
    ).first()

    if existing:
        return jsonify({"message": "Habit already marked completed today"}), 400

    new_completion = HabitCompletion(
        habit_id=habit.id, completed=True, date=today
    )
    db.session.add(new_completion)
    db.session.commit()

    return jsonify({"message": "Habit marked as completed!"}), 200

@app.route("/delete-habit/<int:habit_id>", methods=["DELETE"])
@login_required
def delete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first_or_404()

    HabitCompletion.query.filter_by(habit_id=habit.id).delete()
    db.session.delete(habit)
    db.session.commit()

    return jsonify({"message": "Habit deleted successfully!"}), 200

@app.route("/hive-stats")
@login_required
def hive_stats():
    habits = Habit.query.filter_by(user_id=current_user.id).all()

    completions = (
        HabitCompletion.query.join(Habit)
        .filter(Habit.user_id == current_user.id, HabitCompletion.completed == True)
        .all()
    )
    dates_counter = Counter([c.date.strftime("%d %b") for c in completions])
    dates = list(dates_counter.keys())
    completions_count = list(dates_counter.values())

    habit_labels = []
    habit_values = []
    for h in habits:
        end_date = h.date_created.date() + timedelta(days=h.duration)
        if date.today() <= end_date:
            total_completed = HabitCompletion.query.filter(
                HabitCompletion.habit_id == h.id,
                HabitCompletion.completed == True,
                HabitCompletion.date >= h.date_created,
                HabitCompletion.date <= end_date,
            ).count()
            remaining = max(h.frequency - total_completed, 0)
        else:
            remaining = 0
        habit_labels.append(h.habit_name)
        habit_values.append(remaining)

    today = date.today()
    pending_habits = (
        Habit.query.filter_by(user_id=current_user.id)
        .filter(~Habit.completions.any(HabitCompletion.date == today))
        .all()
    )

    time_counts = {"Morning": 0, "Afternoon": 0, "Night": 0}
    preferred_times = []
    for h in pending_habits:
        if h.preferred_time in time_counts:
            time_counts[h.preferred_time] += 1
            preferred_times.append(h.preferred_time) 
    time_labels = list(time_counts.keys())
    time_values = list(time_counts.values())

    return render_template(
        "hive_stats.html",
        dates=dates,
        completions=completions_count,
        habit_labels=habit_labels,
        habit_values=habit_values,
        time_labels=time_labels,
        time_values=time_values,
        preferred_times=preferred_times
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)