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
