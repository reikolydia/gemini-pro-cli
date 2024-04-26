"""
This file contains code for the application "gemini-pro-cli".
Original Author: GlobalCreativeApkDev
"""

# Importing necessary libraries

import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv
from mpmath import mp, mpf
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt

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
    genai.configure(api_key=os.environ["GENAI_API_KEY"])

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
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    #   Alternative model: gemini-1.5-pro-latest
    #   Old model: gemini-pro
    mdl = "gemini-pro"

    model = genai.GenerativeModel(
        model_name=mdl,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    table = Table(
        title="Current Configuration",
        title_style="red on white bold",
        caption="To end a chat session, just send an empty prompt",
    )
    table.add_column("Model", justify="right")
    table.add_column(str(mdl))
    table.add_column("Settings")
    for i in genai.list_models():
        if str(i.name)[7:] == mdl:
            table.add_row("Description", str(i.description), "_model")
            table.add_row(
                "Temperature",
                str(float_temperature) + " / " + str(i.temperature),
                "_temp",
            )
            table.add_row("Top P", str(float_top_p) + " / " + str(i.top_p), "_p")
            table.add_row("Top K", str(float_top_k) + " / " + str(i.top_k), "_k")
            table.add_row(
                "Max input tokens",
                str(int_max_input_tokens) + " / " + str(i.input_token_limit),
                "_input",
            )
            table.add_row(
                "Max output tokens",
                str(int_max_output_tokens) + " / " + str(i.output_token_limit),
                "_output",
            )
    console.print(table)
    console.print(Markdown("---"))

    convo = model.start_chat(history=[])

    text_count = 0

    while True:
        prompt: str = Prompt.ask("[blue bold]User[/blue bold]")
        if prompt == "":
            console.print(Markdown("---"))
            # for message in convo.history:
            #    console.print(f'{message.role} : {message.parts[0].text}')
            return 0
        elif prompt == "_model":
            console.print(Markdown("---"))
            table = Table(
                title="Currently Available Gemini Models",
                show_lines=True,
                title_style="red on white bold",
            )
            table.add_column("No.", justify="center")
            table.add_column("Name", justify="right")
            table.add_column("Description")
            table.add_column("Input Tokens", justify="center")
            table.add_column("Output Tokens", justify="center")
            table.add_column("Temperature", justify="center")
            table.add_column("Top P", justify="center")
            table.add_column("Top K", justify="center")
            no = 0
            for m in genai.list_models():
                if "gemini" in str(m.name[7:]):
                    no = no + 1
                    table.add_row(
                        str(no),
                        str(m.name[7:]),
                        str(m.description),
                        str(m.input_token_limit),
                        str(m.output_token_limit),
                        str(m.temperature),
                        str(m.top_p),
                        str(m.top_k),
                    )
            console.print(table)
            console.print(Markdown("---"))
            model_prompt: int = Prompt.ask("Select new model: [1 - " + str(no) + "]")
            try:
                model_prompt = int(model_prompt)
                if 0 <= int(model_prompt) <= int(no):
                    mdl_list = {}
                    mdl_no = 0
                    for m in genai.list_models():
                        if "gemini" in str(m.name[7:]):
                            mdl_no = mdl_no + 1
                            mdl_name = m.name[7:]
                            mdl_list[mdl_no] = mdl_name
                    mdl = mdl_list[int(model_prompt)]
                    if mdl == "gemini-1.5-pro-latest":
                        console.print(
                            "[red bold]System instructions[/red bold] enable users to steer the behavior of the model based on their specific needs and use cases. When you set a [red bold]system instruction[/red bold], you give the model additional context to understand the task, provide more customized responses, and adhere to specific guidelines over the full user interaction with the model."
                        )
                        si_prompt: str = Prompt.ask(
                            "[red bold]Custom system instructions[/red bold]"
                        )
                        if si_prompt == "":
                            console.print("No instructions provided.")
                            sys_i = ""
                        else:
                            sys_i = str(si_prompt)
                        model = genai.GenerativeModel(
                            model_name=mdl,
                            generation_config=generation_config,
                            safety_settings=safety_settings,
                            system_instruction=sys_i,
                        )
                    else:
                        model = genai.GenerativeModel(
                            model_name=mdl,
                            generation_config=generation_config,
                            safety_settings=safety_settings,
                        )
                    table = Table(
                        title="New Configuration Saved",
                        title_style="red on white bold",
                        caption="To end a chat session, just send and empty prompt",
                    )
                    table.add_column("Model", justify="right")
                    table.add_column("[red bold]{mdl}[/red bold]".format(mdl=mdl))
                    table.add_column("Settings")
                    for i in genai.list_models():
                        if str(i.name)[7:] == mdl:
                            table.add_row("Description", str(i.description), "_model")
                            if float_temperature > i.temperature:
                                float_temperature = i.temperature
                                generation_config[0] = "Temperature: {ft}".format(
                                    ft=float_temperature
                                )
                                table.add_row(
                                    "Temperature",
                                    "[red bold]{ft}[/red bold]".format(
                                        ft=float_temperature
                                    )
                                    + " / "
                                    + "[yellow bold]{it}[/yellow bold]".format(
                                        it=i.temperature
                                    ),
                                    "_temp",
                                )
                            else:
                                table.add_row(
                                    "Temperature",
                                    str(float_temperature) + " / " + str(i.temperature),
                                    "_temp",
                                )
                            table.add_row(
                                "Top P", str(float_top_p) + " / " + str(i.top_p), "_p"
                            )
                            table.add_row(
                                "Top K", str(float_top_k) + " / " + str(i.top_k), "_k"
                            )
                            table.add_row(
                                "Max input tokens",
                                str(int_max_input_tokens)
                                + " / "
                                + str(i.input_token_limit),
                                "_input",
                            )
                            table.add_row(
                                "Max output tokens",
                                str(int_max_output_tokens)
                                + " / "
                                + str(i.output_token_limit),
                                "_output",
                            )
                    console.print(Markdown("---"))
                    console.print(table)
                    console.print(Markdown("---"))
                else:
                    console.print(
                        "[yellow bold]ERROR[/yellow bold]: [ [blue bold]{mp}[/blue bold] ] is [red bold]NOT[/red bold] within [ [green bold]0 - {no}[/green bold] ] (INT)".format(
                            mp=model_prompt, no=no
                        )
                    )
                    console.print(Markdown("---"))
            except ValueError as e:
                console.print(
                    "[yellow bold]ERROR[/yellow bold]: [ [blue bold]{mp}[/blue bold] ] is [red bold]NOT[/red bold] a [ [green bold]INTEGER NUMBER[/green bold] ]".format(
                        mp=model_prompt
                    )
                )
                console.print(Markdown("---"))

        elif prompt == "_temp":
            console.print(Markdown("---"))
            for i in genai.list_models():
                if str(i.name)[7:] == mdl:
                    max_temp = i.temperature
            temp_prompt: float = Prompt.ask(
                "Enter new temperature: [0 - " + str(max_temp) + "]"
            )
            try:
                temp_prompt = float(temp_prompt)
                if 0 <= float(temp_prompt) <= float(max_temp):
                    generation_config[0] = "Temperature: {ft}".format(ft=temp_prompt)
                    table = Table(
                        title="New Configuration Saved",
                        title_style="red on white bold",
                        caption="To end a chat session, just send and empty prompt",
                    )
                    table.add_column("Model", justify="right")
                    table.add_column(str(mdl))
                    table.add_column("Settings")
                    for i in genai.list_models():
                        if str(i.name)[7:] == mdl:
                            table.add_row("Description", str(i.description), "_model")
                            table.add_row(
                                "Temperature",
                                "[red bold]{tp}[/red bold]".format(tp=temp_prompt)
                                + " / "
                                + str(i.temperature),
                                "_temp",
                            )
                            table.add_row(
                                "Top P", str(float_top_p) + " / " + str(i.top_p), "_p"
                            )
                            table.add_row(
                                "Top K", str(float_top_k) + " / " + str(i.top_k), "_k"
                            )
                            table.add_row(
                                "Max input tokens",
                                str(int_max_input_tokens)
                                + " / "
                                + str(i.input_token_limit),
                                "_input",
                            )
                            table.add_row(
                                "Max output tokens",
                                str(int_max_output_tokens)
                                + " / "
                                + str(i.output_token_limit),
                                "_output",
                            )
                    console.print(Markdown("---"))
                    console.print(table)
                    console.print(Markdown("---"))
                else:
                    console.print(
                        "[yellow bold]ERROR[/yellow bold]: [ [blue bold]{tp}[/blue bold] ] is [red bold]NOT[/red bold] within [ [green bold]0 - {mt}[/green bold] ] (FLOAT)".format(
                            tp=temp_prompt, mt=max_temp
                        )
                    )
                    console.print(Markdown("---"))
            except ValueError as e:
                console.print(
                    "[yellow bold]ERROR[/yellow bold]: [ [blue bold]{tp}[/blue bold] ] is [red bold]NOT[/red bold] a [ [green bold]FLOAT NUMBER[/green bold] ]".format(
                        tp=temp_prompt
                    )
                )
                console.print(Markdown("---"))
        else:
            try:
                tokencount = model.count_tokens(prompt).total_tokens
                console.print(
                    'Token count of "'
                    + prompt
                    + '": '
                    + str(tokencount)
                    + ' | Character count of "'
                    + prompt
                    + '": '
                    + str(len(prompt))
                )
                response = convo.send_message(prompt)
                reply_tokencount = model.count_tokens(convo.history[-1]).total_tokens
                console.print("[red bold]AI (" + mdl + ")[/red bold]: ")
                console.print(Markdown(str(response.text)))
                console.print("")
                console.print(
                    "Token count of response: "
                    + str(reply_tokencount)
                    + " | Character count of response: "
                    + str(len(response.text))
                )
                text_count = text_count + len(prompt) + len(response.text)
                if convo.history != []:
                    total_tokencount = tokencount + reply_tokencount
                else:
                    total_tokencount = (
                        tokencount
                        + model.count_tokens(convo.history).total_tokens
                        + reply_tokencount
                    )
                console.print(
                    "Total tokens count: "
                    + str(total_tokencount)
                    + " | Total character count: "
                    + str(text_count)
                )
                console.print("")
                console.print(Markdown("---"))
            except genai.types.generation_types.BlockedPromptException:
                console.print(
                    "[red bold]AI ("
                    + mdl
                    + ")[/red bold]: [red on white bold]Sorry! Cannot generate response![/red on white bold]"
                )
            except BaseException as ex:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                console.print("Exception type : %s " % ex_type.__name__)
                if ex_type.__name__ == "StopCandidateException":
                    ex_value2 = str(ex_value).splitlines()
                    ex_value3 = str(ex_value2[1]).split()
                    console.print("Exception message : %s" % ex_value3[1])
                else:
                    console.print("Exception message : %s" % ex_value)
                # console.print("Stack trace : %s" %stack_trace)


if __name__ == "__main__":
    main()
