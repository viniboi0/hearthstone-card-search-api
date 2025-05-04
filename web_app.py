from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store for demo purposes
users = {}

# In-memory saved searches store: user_id -> list of search queries
saved_searches = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

API_URL = "https://api.hearthstonejson.com/v1/latest/enUS/cards.json"

def fetch_all_cards():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; HearthstoneCardSearch/1.0)"
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code != 200:
            return None, f"Failed to fetch cards: {response.status_code}"
        if not response.text.strip():
            return None, "Empty response from API"
        return response.json(), None
    except Exception as e:
        return None, str(e)

def search_cards(cards, queries):
    results = []
    queries_lower = [q.lower() for q in queries]
    for card in cards:
        card_name = card.get("name", "").lower()
        card_id = card.get("id", "").lower()
        for q in queries_lower:
            if q == card_name or q == card_id or q in card_name or q in card_id:
                import re
                raw_text = card.get('text', 'N/A')
                # Remove square bracket tags like [x], [b], [/b], etc.
                clean_text = re.sub(r'\[/?[^\]]+\]', '', raw_text)
                # Remove HTML tags like <b>, </b>, etc.
                clean_text = re.sub(r'<[^>]+>', '', clean_text)
                # Remove $ symbols from card text
                clean_text = clean_text.replace('$', '')
                card_str = (
                    f"Card id: {card.get('id', 'N/A')}\n"
                    f"Name: {card.get('name', 'N/A')}\n"
                    f"Attack: {card.get('attack', 'N/A')}\n"
                    f"Health: {card.get('health', 'N/A')}\n"
                    f"Mana Cost: {card.get('cost', 'N/A')}\n"
                    f"Card Text: {clean_text.strip()}\n"
                )
                results.append(card_str)
                break
    return results

def paginate_results(results, page, per_page=5):
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = results[start:end]
    total_pages = (total + per_page - 1) // per_page
    return paginated, total_pages

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    cards_data = []
    error = None
    saved = []
    page = request.args.get("page", 1, type=int)
    if request.method == "POST":
        card_queries_text = request.form.get("card_queries")
        if card_queries_text:
            queries = [line.strip() for line in card_queries_text.splitlines() if line.strip()]
            all_cards, err = fetch_all_cards()
            if err:
                error = err
            else:
                all_results = search_cards(all_cards, queries)
                if not all_results:
                    error = "No matching cards found."
                else:
                    # Save the search for the user
                    user_id = current_user.id
                    saved_searches.setdefault(user_id, [])
                    saved_searches[user_id].append(card_queries_text)
                    saved = saved_searches[user_id]
                    cards_data, total_pages = paginate_results(all_results, page)
        else:
            cards_data = []
            total_pages = 0
    else:
        # On GET, show saved searches for user
        user_id = current_user.id
        saved = saved_searches.get(user_id, [])
        cards_data = []
        total_pages = 0
    return render_template("index.html", cards_data=cards_data, error=error, saved=saved, user=current_user, page=page, total_pages=total_pages)

@app.route("/about")
def about():
    return render_template("about.html", user=current_user)

@app.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if any(u.username == username for u in users.values()):
            flash("Username already exists.", "danger")
            return redirect("/register")
        password_hash = generate_password_hash(form.password.data)
        user_id = str(len(users) + 1)
        user = User(user_id, username, password_hash)
        users[user_id] = user
        login_user(user)
        flash("Registration successful.", "success")
        return redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = next((u for u in users.values() if u.username == username), None)
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful.", "success")
            return redirect("/")
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect("/login")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
