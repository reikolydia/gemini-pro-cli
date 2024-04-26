# gemini-pro-cli

This application allows users to use Gemini Pro on command-line interface (CLI).

# Original Source Code

The original source code for the Gemini Pro CLI application is available at 
https://github.com/GlobalCreativeApkDev/gemini-pro-cli/blob/master/main.py.

> This fork just makes it look more presentable..

## To-do:
- [x] Add token counts
- [x] Add character counts
- [x] Add ability to change model
- [x] Add ability to edit temperature
- [x] Add ability to edit TOP P
- [x] Add ability to edit TOP K
- [ ] Add ability to edit max input tokens
- [x] Add ability to edit max output tokens
- [ ] Add ability to scroll with mouse in chat box
- [x] Catch errors from GENAI
- [ ] Catch errors from main
- [ ] Beautify the output from the AI
- [ ] Selection index of item in menus should remain after editing values
- [x] Adding cancel button in select model page
- [ ] Catch and edit QUIT to show warning pop up
- [x] Save chats to disk as text files
- [ ] Allow user to choose location to save the chat text files

#### Gemini 1.5 / Vision Pro To-dos:
- [ ] Add customizable system instructions
- [ ] Add ability to upload media
- [ ] Add ability to generate media, like images, saved to local disk


# How to Use the Application?

Pre-requisites:
1. [Python](https://www.python.org/downloads/) installed in your device.
2. .env file in the same directory as <GEMINI_PRO_CLI_DIRECTORY> and has the value of GENAI_API_KEY.
3. Then, open a Terminal or Command Prompt window and create a virtual Python environment.

```
cd <GEMINI_PRO_CLI_DIRECTORY>
python -m venv gemini
<GEMINI_PRO_CLI_DIRECTORY>/Scripts/activate
pip install -r requirements.txt
```

4. Run the application

```
python <GEMINI_PRO_CLI_DIRECTORY>/main.py
```

> **Note:** Replace <GEMINI_PRO_CLI_DIRECTORY> with the path to the directory of the application gemini-pro-cli.
