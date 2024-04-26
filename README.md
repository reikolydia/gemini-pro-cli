# gemini-pro-cli

This application allows users to use Gemini Pro on command-line interface (CLI).

# Original Source Code

The original source code for the Gemini Pro CLI application is available at 
https://github.com/GlobalCreativeApkDev/gemini-pro-cli/blob/master/main.py.

> This fork just makes it look more presentable..

To-do:
- [x] Add token counts
- [x] Add ability to change model
- [x] Add ability to edit temperature
- [ ] Add ability to edit TOP P
- [ ] Add ability to edit TOP K
- [ ] Add ability to edit max input tokens
- [ ] Add ability to edit max output tokens

Gemini 1.5 Pro To-dos:
- [x] Add customizable system instructions
- [ ] Add ability to upload media
- [ ] Add ability to generate media, like images, saved to local disk


# Original Installation Instructions

```
pip install gemini-pro-cli
```

# How to Use the Application?

Pre-requisites:
1. [Python](https://www.python.org/downloads/) installed in your device.
2. .env file in the same directory as <GEMINI_PRO_CLI_DIRECTORY> and has the value of GENAI_API_KEY.

First, open a Terminal or Command Prompt window and run the following command.

```
python3 <GEMINI_PRO_CLI_DIRECTORY>/main.py
```

**Note:** Replace <GEMINI_PRO_CLI_DIRECTORY> with the path to the directory of the application gemini-pro-cli.

Then, the application will start with something looking like in the screenshot below.

![Application](images/Application.png)

You will then be asked to input the following values.

1. Temperature - between 0 and 1 inclusive
2. Top P - between 0 and 1 inclusive
3. Top K - at least 1
4. Max output tokens - at least 1

The following screenshot shows what is displayed after inputting the mentioned values.

![Main Menu](images/Main%20Menu.png)

Next, you will have two choices:

1. Enter a non-empty prompt to receive a response from the AI.
2. Enter an empty prompt to exit the application.

Below is an example of what happens when you entered a non-empty prompt.

![AI](images/AI.png)