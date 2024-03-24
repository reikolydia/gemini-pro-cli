"""
This file contains code for the application "gemini-pro-cli".
Author: GlobalCreativeApkDev
"""


# Importing necessary libraries


import google.generativeai as genai
import os
from dotenv import load_dotenv
from mpmath import mp, mpf
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

mp.pretty = True
console = Console()


# Creating static function to be used in this application.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    load_dotenv()
    genai.configure(api_key=os.environ['GENAI_API_KEY'])

    # Asking user input values for generation config
#    temperature: str = input("Please enter temperature (0 - 1): ")
#    while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
#        temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

#    print("'Temperature' is set to: 0.75")
    float_temperature: float = float(0.75)

#    top_p: str = input("Please enter Top P (0 - 1): ")
#    while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
#        top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

#    float_top_p: float = float(top_p)
#    print("'top_p' is set to: 1")
    float_top_p: float = float(1)    

#    top_k: str = input("Please enter Top K (at least 1): ")
#    while not is_number(top_k) or int(top_k) < 1:
#        top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

#    float_top_k: int = int(top_k)
#    print("'top_k' is set to: 1")
    float_top_k: int = int(1)

#    max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
#    while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
#        max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

#    int_max_output_tokens: int = int(max_output_tokens)
#    print("'Max output tokens' is set to: 2048")
    int_max_output_tokens: int = int(2048)

    int_max_input_tokens: int = int(2048)

    # Set up the model
    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_input_tokens": int_max_input_tokens,
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

#   Alternative model: gemini-1.5-pro-latest
#   Old model: gemini-pro
    mdl = "gemini-pro"
    model = genai.GenerativeModel(model_name=mdl,
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    table = Table(title="Configuration")
    table.add_column("Model", justify="right")
    table.add_column(str(mdl))

    for i in genai.list_models():
        if str(i.name)[7:] == "gemini-pro":
            table.add_row("Description", str(i.description))
            table.add_row("Temperature", str(float_temperature) + " / " + str(i.temperature))
            table.add_row("Top P", str(float_top_p) + " / " + str(i.top_p))
            table.add_row("Top K", str(float_top_k) + " / " + str(i.top_k))
            table.add_row("Max input tokens", str(int_max_input_tokens) + " / " + str(i.input_token_limit))
            table.add_row("Max output tokens", str(int_max_output_tokens) + " / " + str(i.output_token_limit))

    console.print(table)
    console.print(Markdown("---"))
    

    convo = model.start_chat(history=[
    ])

    while True:
        prompt: str = input("User: ")
        print("")
        if prompt == "":
            return 0
        try:
            convo.send_message(prompt)
            console.print(Markdown("AI: " + str(convo.last.text)))
            console.print(Markdown("---"))
        except genai.types.generation_types.BlockedPromptException:
            print("AI: Sorry! Cannot generate response.")


if __name__ == '__main__':
    main()
