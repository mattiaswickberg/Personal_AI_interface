from app import app, db, login_manager, bcrypt
from app.database.models import User, ChatHistory, Summary, ConfigurationPreset
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.utilities import ask_gpt3, summarize_with_gpt3, generate_reminder_from_summary

from functools import wraps

def requires_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"message": "Unauthorized"}), 403

            # Assumes the User model has a 'role' attribute that provides access to the role name.
            if current_user.role.name != required_role:
                return jsonify({"message": "Unauthorized"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
@login_required
def chat():
    # Fetch all the configurations
    system_configs = ConfigurationPreset.query.all()
    
    # Fetch the latest summary for the user
    last_summary = Summary.query.filter_by(user_id=current_user.id).order_by(Summary.timestamp.desc()).first()

    reminder_message = None
    if last_summary:
        # If there's a summary, generate a reminder message
        reminder_message = generate_reminder_from_summary(last_summary.summary)
        
    return render_template('chat.html', system_configs=system_configs, reminder=reminder_message, username=current_user.username)


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    chat_history = data.get('chatHistory', [])
    config_id = data.get('configId')
    
    system_message, temperature, top_p, model_name = None, None, None, "gpt-3.5-turbo"
    
    # If a configuration ID is provided, fetch the configuration from the database
    if config_id:
        chosen_config = ConfigurationPreset.query.get(config_id)
        if chosen_config:
            system_message = chosen_config.system_prompt
            temperature = chosen_config.temperature
            top_p = chosen_config.top_p
            model_name = chosen_config.ai_model
    
    response = ask_gpt3(chat_history, model=model_name, system_message=system_message, temperature=temperature, top_p=top_p)
    
    return jsonify({'response': response})


@app.route('/save', methods=['POST'])
def save():
    # Handle saving of conversations here
    return jsonify({"message": "Save endpoint"})

@app.route('/load', methods=['GET'])
def load():
    # Handle loading of saved conversations here
    return jsonify({"message": "Load endpoint"})

@app.route('/register', methods=['GET', 'POST'])
@login_required
@requires_role('admin')
def register():
        if request.method == 'POST':
         # Register a new user
            username = request.form.get('username')
            password = request.form.get('password')
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if user already exists
            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify({"message": "User already exists!"}), 400

            new_user = User(username=username, hashedpw=password)
            db.session.add(new_user)
            db.session.commit()

        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # Using Bcrypt's `check_password_hash` to compare the entered password with the stored hash.
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Invalid credentials!"}), 401

        # If user exists and password matches
        login_user(user)  # This logs in the user and starts their session

        return redirect(url_for('index'))  # Redirect them wherever you want after login

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/full_ask', methods=['POST'])
def full_ask():
    question = request.form.get('question')
    
    # Save user's question to DB without user_id
    user_question = ChatHistory(message=question, is_user=True)
    db.session.add(user_question)

    # Get AI's answer
    answer = ask_gpt3(question)

    # Save AI's answer to DB without user_id
    ai_answer = ChatHistory(message=answer, is_user=False)
    db.session.add(ai_answer)
    db.session.commit()

    return jsonify({"answer": answer}), 200

@app.route('/configure', methods=['GET', 'POST'])
@requires_role('admin')
@login_required
def configure():
    if request.method == 'POST':
        preset_name = request.form.get('preset_name')
        ai_model = request.form.get('ai_model')
        system_prompt = request.form.get('system_prompt')
        temperature = request.form.get('temperature')
        top_p = request.form.get('top_p')

        
        preset = ConfigurationPreset(
            name=preset_name,
            ai_model=ai_model,
            system_prompt=system_prompt,
            temperature=temperature,
            top_p=top_p
        )
        
        db.session.add(preset)
        db.session.commit()

    presets = ConfigurationPreset.query.all()
    return render_template('configure.html', presets=presets)

@app.route('/configure/<int:preset_id>/edit', methods=['GET', 'POST'])
def edit_configure(preset_id):
    preset = ConfigurationPreset.query.get(preset_id)
    if not preset:
        return "Preset not found!", 404

    if request.method == 'POST':
        preset.name = request.form.get('preset_name')
        preset.ai_model = request.form.get('ai_model')
        preset.system_prompt = request.form.get('system_prompt')
        preset.temperature = request.form.get('temperature')
        preset.top_p = request.form.get('top_p')
        
        db.session.commit()
        return redirect(url_for('configure'))

    return render_template('edit_configure.html', preset=preset)

@app.route('/configure/<int:preset_id>/delete', methods=['POST'])
def delete_configure(preset_id):
    preset = ConfigurationPreset.query.get(preset_id)
    if not preset:
        return jsonify({"message": "Preset not found!"}), 404

    db.session.delete(preset)
    db.session.commit()
    return redirect(url_for('configure'))

@app.route('/end_session', methods=['POST'])
def end_session():
    chat_history = request.json.get('chatHistory')

    # Generate summary
    summary_text = summarize_with_gpt3(chat_history)

    # Save the summary to the database
    new_summary = Summary(user_id=current_user.id, summary=summary_text)
    db.session.add(new_summary)
    db.session.commit()

    return jsonify({"success": True, "summary": summary_text})

