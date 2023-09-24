# Personal AI interface

This is a simple interface for an AI chat bot, with the option of saving configurations to use in the chat. It's developed mostly for experimentation and research, and is in it's current state only designed to be run locally on a computer with a local database. Also, for now only working with OpenAIs GPT3.5-turbo. 

If you do try this, note that the account registration is only available when logged in as admin, so you need to add the first admin account directly to the database. 

I'm not a developer! This is crude, simple and only very basic security measures have been taken with this so far. 

Functionality: 
- Create and save configurations to be used in chat. Name, System prompt, temperature and top_p available for config.
- Also added configuration desciption, and temporary information fields. My idea for the latter is that one can add for instance what is happening that week, so that the AI can ask about it.
- Automatically saves a summary upon clicking end session
- Looks at last summary when loading page and starts session by asking about last one.
- Add markdown support
- Add configuration to chat history
- Add profileration of configurations admin -> teacher -> student

To be added: 
- Add support for other language models.
