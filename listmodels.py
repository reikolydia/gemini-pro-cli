"""
This file contains code for the application "gemini-pro-cli".
Original Author: GlobalCreativeApkDev
"""


# Importing necessary libraries


import google.generativeai as genai
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

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
    load_dotenv()
    genai.configure(api_key=os.environ['GENAI_API_KEY'])
    
    table = Table(title="Available Models", show_lines=True, title_style="red on white bold")
    table.add_column("Name", justify="right")
    table.add_column("Description")
    table.add_column("Input Tokens", justify="center")
    table.add_column("Output Tokens", justify="center")
    table.add_column("Temperature", justify="center")
    table.add_column("Top P", justify="center")
    table.add_column("Top K", justify="center")
    for m in genai.list_models():
        table.add_row(str(m.name[7:]), str(m.description), str(m.input_token_limit), str(m.output_token_limit), str(m.temperature), str(m.top_p), str(m.top_k))

    console.print(table)

if __name__ == '__main__':
    main()
