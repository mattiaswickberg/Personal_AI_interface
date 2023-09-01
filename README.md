# Personal_AI_interface

This is a simple interface for an AI chat bot, with the option of saving configurations to use in the chat. It's developed mostly for experimentation and research, and is in it's current state only designed to be run locally on a computer with a local database. Also, for now only working with OpenAIs GPT3.5-turbo. 

I'm not a developer! This is crude, simple and no security measures have been taken with this so far. 

Functionality: 
- Create and save configurations to be used in chat. Name, System prompt, temperature and top_p available for config.
- Automatically saves a summary upon clicking end session
- Looks at last summary when loading page and starts session by asking about last one. 

To be added: 
- Add configuration to chat history
- Add support for other AI models.
- Add possible behaviours on startup to configuration
- Add global configurations available to all accounts
- Fix aesthetics
- Add markdown support
