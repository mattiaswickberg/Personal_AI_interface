from app import app, db, login_manager  # Importing login_manager
from app.database.models import User, ChatHistory, Summary, ConfigurationPreset
from flask_login import login_required, current_user
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_user
from app.utilities import ask_gpt3

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
@login_required
def chat():
    system_configs = ConfigurationPreset.query.all()
    return render_template('chat.html', system_configs=system_configs)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    chat_history = data.get('chatHistory', [])
    config_id = data.get('configId')
    
    system_message, temperature, top_p = None, None, None
    
    # If a configuration ID is provided, fetch the configuration from the database
    if config_id:
        chosen_config = ConfigurationPreset.query.get(config_id)
        if chosen_config:
            system_message = chosen_config.system_prompt
            temperature = chosen_config.temperature
            top_p = chosen_config.top_p
    
    response = ask_gpt3(chat_history, system_message=system_message, temperature=temperature, top_p=top_p)
    
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
def register():
        if request.method == 'POST':
         # Register a new user
            username = request.form.get('username')
            password = request.form.get('password')

    # Check if user already exists
            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify({"message": "User already exists!"}), 400

            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            if form.validate_on_submit():
            # save new user to the database
                return redirect(url_for('login'))
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or user.password != password:  # Check password here
            return jsonify({"message": "Invalid credentials!"}), 401

        # If user exists and password matches
        login_user(user)  # This logs in the user and starts their session
        return redirect(url_for('index'))  # Redirect them wherever you want after login

    return render_template('login.html')


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