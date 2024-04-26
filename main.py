"""
This file contains code for the application "gemini-pro-cli".
Original Author: GlobalCreativeApkDev
"""

# To generate the RECITATION error, use this prompt:
# Count from 1 to 100, print numbers as words

# Importing necessary libraries

import google.generativeai as genai
import os
from dotenv import load_dotenv
from mpmath import mp
from inspect import cleandoc
import py_cui
import os
import logging
import textwrap
from threading import Thread
import itertools
import pyperclip
import sys
import traceback
import time
from datetime import datetime

mp.pretty = True

global mdl
global generation_config
global config_items
global safety_settings
global safety_items
global b_none
global b_high
global b_med
global b_low
global hr
global hs
global se
global dc
global dir

dir = os.getcwd()

mdl = "gemini-pro"

load_dotenv()
genai.configure(api_key=os.environ["GENAI_API_KEY"])

safety_selection = [
    "BLOCK_NONE",
    "BLOCK_ONLY_HIGH",
    "BLOCK_MEDIUM_AND_ABOVE",
    "BLOCK_LOW_AND_ABOVE",
]

b_none = safety_selection[0]
b_high = safety_selection[1]
b_med = safety_selection[2]
b_low = safety_selection[3]

hr_setting = str(b_none)
hs_setting = str(b_none)
se_setting = str(b_none)
dc_setting = str(b_none)

hr = str(hr_setting)
hs = str(hs_setting)
se = str(se_setting)
dc = str(dc_setting)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": hr},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": hs},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": se},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": dc},
]

float_temperature: float = float(0.75)
float_top_p: float = float(1)
float_top_k: int = int(1)
int_max_output_tokens: int = int(2048)
int_max_input_tokens: int = int(2048)

for m in genai.list_models():
    if str(m.name)[7:] == mdl:
        mdl_desc = m.description
        mdl_ft = m.temperature
        mdl_tp = m.top_p
        mdl_tk = m.top_k
        mdl_input = m.input_token_limit
        mdl_output = m.output_token_limit

config_items = [
    "Temperature: {ft} / {mdl_ft}".format(
        ft=str(float_temperature), mdl_ft=str(mdl_ft)
    ),
    "Top P: {tp} / {mdl_tp}".format(tp=str(float_top_p), mdl_tp=str(mdl_tp)),
    "Top K: {tk} / {mdl_tk}".format(tk=str(float_top_k), mdl_tk=str(mdl_tk)),
    "Output Limit: {ol} / {mdl_ol}".format(
        ol=str(int_max_output_tokens), mdl_ol=str(mdl_output)
    ),
    "Input Limit: {il} / {mdl_il}".format(
        il=str(int_max_input_tokens), mdl_il=str(mdl_input)
    ),
]

global model_title
model_title = """{mdl}""".format(mdl=mdl)
global model_desc
model_desc = """{model_desc}""".format(model_desc=textwrap.fill(mdl_desc, 33))
model_desc = cleandoc(model_desc)

safety_items = [
    "Harrassment: {hl}".format(hl=hr_setting),
    "Hate Speech: {hs}".format(hs=hs_setting),
    "Sexually Explicit: {se}".format(se=se_setting),
    "Dangerous Content: {dc}".format(dc=dc_setting),
]

ttl_tokens = 0


class MyCUI(py_cui.PyCUI):
    def _handle_key_press(self, key_pressed):
        if key_pressed == py_cui.keys.KEY_Q_LOWER:
            return
        else:
            super()._handle_key_press(key_pressed)


class centermenu:

    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        self.main = self.master.create_new_widget_set(8, 9)
        self.master.apply_widget_set(self.main)

        # PRIMARY PAGE

        self.model_title = self.master.add_text_block("Current Model", 0, 0, 1, 3)
        self.model_desc = self.master.add_text_block("Description", 1, 0, 2, 3)
        self.config_cell = self.master.add_scroll_menu("Configuration", 3, 0, 2, 3)
        self.safety_cell = self.master.add_scroll_menu("Safety", 5, 0, 2, 3)
        self.chat_cell = self.master.add_scroll_menu("Chat", 0, 3, 5, 6)
        self.user_tokens_label = self.master.add_label("User", 5, 3, 1, 2)
        self.user_tokens = self.master.add_scroll_menu("TOK", 6, 3, 1, 1)
        self.user_chars = self.master.add_scroll_menu("CHAR", 6, 4, 1, 1)
        self.response_tokens_label = self.master.add_label("Response", 5, 5, 1, 2)
        self.response_tokens = self.master.add_scroll_menu("TOK", 6, 5, 1, 1)
        self.response_chars = self.master.add_scroll_menu("CHAR", 6, 6, 1, 1)
        self.total_tokens_label = self.master.add_label("Total", 5, 7, 1, 2)
        self.total_tokens = self.master.add_scroll_menu("TOK", 6, 7, 1, 1)
        self.total_chars = self.master.add_scroll_menu("CHAR", 6, 8, 1, 1)
        self.model_change = self.master.add_button(
            "Change Model", 7, 0, 1, 3, command=self.change_page
        )

        # Textbox for entering chat messages
        self.textbox = self.master.add_text_box(
            "Type something to: [ {mdl} ]".format(mdl=mdl), 7, 3, column_span=6
        )
        self.textbox.set_focus_text(
            "Chat message box selected | < ESC > to leave box | < ENTER > to send message | < RIGHT CLICK > to paste"
        )
        # self.textbox.add_text_color_rule('.*', py_cui.RED_ON_BLACK, 'contains', match_type='region', region=[19,99])

        # Add some key bindings
        self.textbox.add_key_command(py_cui.keys.KEY_ENTER, self.run_send_prompt)
        self.model_title.add_key_command(py_cui.keys.KEY_ENTER, self.redo_title_desc)
        self.model_desc.add_key_command(py_cui.keys.KEY_ENTER, self.redo_title_desc)
        self.config_cell.add_key_command(py_cui.keys.KEY_ENTER, self.config_chooser)
        self.safety_cell.add_key_command(py_cui.keys.KEY_ENTER, self.safety_chooser)
        self.master.add_key_command(py_cui.keys.KEY_SPACE, self.select_textbox)
        self.master.add_key_command(py_cui.keys.KEY_Q_LOWER, self.quit_popup)
        self.master.add_key_command(py_cui.keys.KEY_CTRL_S, self.save_chat_popup)

        # Add some mouse key bindings
        self.textbox.add_mouse_command(
            py_cui.keys.RIGHT_MOUSE_CLICK, self.paste_clipboard
        )
        self.config_cell.add_mouse_command(
            py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.config_chooser
        )
        self.safety_cell.add_mouse_command(
            py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.safety_chooser
        )
        # self.model_desc.add_mouse_command(py_cui.keys.LEFT_MOUSE_CLICK, self.open_desc)
        # self.chat_cell.add_mouse_command( py_cui.keys.

        # Add some colors
        self.user_tokens.add_text_color_rule(".*", py_cui.BLUE_ON_BLACK, "contains")
        self.response_tokens.add_text_color_rule(".*", py_cui.RED_ON_BLACK, "contains")
        self.total_tokens.add_text_color_rule(".*", py_cui.GREEN_ON_BLACK, "contains")
        self.config_cell.add_text_color_rule(
            ".*",
            py_cui.WHITE_ON_BLACK,
            rule_type="contains",
            selected_color=py_cui.WHITE_ON_MAGENTA,
        )
        self.safety_cell.add_text_color_rule(
            ".*",
            py_cui.WHITE_ON_BLACK,
            rule_type="contains",
            selected_color=py_cui.WHITE_ON_RED,
        )
        self.chat_cell.add_text_color_rule(
            "\*{2}(.*?)\*{2}",
            py_cui.BLACK_ON_WHITE,
            rule_type="contains",
            match_type="regex",
        )

        self.model_title.set_text(model_title)
        self.model_desc.set_text(model_desc)
        self.config_cell.add_item_list(config_items)
        self.safety_cell.add_item_list(safety_items)

        self.chat_cell.add_text_color_rule(
            "User:",
            py_cui.BLUE_ON_BLACK,
            "startswith",
            match_type="region",
            region=[0, 5],
        )
        self.chat_cell.add_text_color_rule(
            "AI:", py_cui.RED_ON_BLACK, "startswith", match_type="region", region=[0, 3]
        )

        self.master.set_status_bar_text(
            "< Q > to exit | < SPACE > to send a message | < CTRL + S > to save chat"
        )

        self.redo_title_desc()
        # self.master.move_focus(self.textbox)

        # CHANGE MODEL PAGE

        self.change_mdl = self.master.create_new_widget_set(8, 6)
        self.models_show = self.change_mdl.add_scroll_menu(
            "Available Models", 0, 0, 7, 2
        )
        self.model_sel = self.change_mdl.add_button(
            "Select Model", 7, 0, 1, 1, command=self.model_selection_popup
        )
        self.model_cancel = self.change_mdl.add_button(
            "Cancel", 7, 1, 1, 1, command=self._model_cancel
        )
        self.mdl_sum = self.change_mdl.add_text_block("Model Name", 0, 2, 1, 4)
        self.change_mdl_sel = self.change_mdl.add_text_block(
            "Model Description", 1, 2, 2, 4
        )
        self.mdl_temp = self.change_mdl.add_text_block("Temperature", 3, 2, 2, 1)
        self.mdl_p = self.change_mdl.add_text_block("Top P", 3, 3, 2, 1)
        self.mdl_k = self.change_mdl.add_text_block("Top K", 3, 4, 2, 1)
        self.mdl_ver = self.change_mdl.add_text_block("Version", 3, 5, 2, 1)
        self.mdl_inp = self.change_mdl.add_text_block("Input TOK", 5, 2, 2, 1)
        self.mdl_oup = self.change_mdl.add_text_block("Output TOK", 5, 3, 2, 1)
        self.mdl_gen = self.change_mdl.add_text_block("Generation Methods", 5, 4, 2, 2)
        self.mdl_textbox = self.change_mdl.add_text_box("Search Models..", 7, 2, 1, 4)

        # MODEL PAGE KEYBINDS
        self.models_show.add_key_command(py_cui.keys.KEY_UP_ARROW, self.scroll_up)
        self.models_show.add_key_command(py_cui.keys.KEY_DOWN_ARROW, self.scroll_down)
        self.models_show.add_key_command(py_cui.keys.KEY_PAGE_UP, self.scroll_page_up)
        self.models_show.add_key_command(
            py_cui.keys.KEY_PAGE_DOWN, self.scroll_page_down
        )
        self.models_show.add_key_command(py_cui.keys.KEY_HOME, self.scroll_home)
        self.models_show.add_key_command(py_cui.keys.KEY_END, self.scroll_end)
        self.models_show.add_key_command(
            py_cui.keys.KEY_ENTER, self.model_selection_popup
        )
        self.change_mdl.add_key_command(py_cui.keys.KEY_SPACE, self.select_searchbox)
        # self.change_mdl.add_key_command( py_cui.keys.KEY_ENTER, self.model_selection_popup)
        self.mdl_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.search_models)

        # MODEL PAGE MOUSE BINDS
        self.models_show.add_mouse_command(
            py_cui.keys.LEFT_MOUSE_CLICK, self.mouse_select
        )
        self.models_show.add_mouse_command(
            py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.model_selection_popup
        )

        # MODEL PAGE COLORS
        self.models_show.add_text_color_rule(
            ".*",
            py_cui.WHITE_ON_BLACK,
            rule_type="contains",
            selected_color=py_cui.WHITE_ON_CYAN,
        )

        self.mdl_textbox.set_focus_text(
            "Search box selected | < ESC > to leave box | < ENTER > to begin search"
        )

        self.show_models()

    def show_error(self, title, message):
        self.master.show_error_popup(title, message)

    def quit_popup(self):
        self.master.show_yes_no_popup("Are you sure you want to quit? ", self.quit)

    def quit(self, choice):
        if choice:
            exit()
        else:
            self.master.show_warning_popup("Cancelled", "Quit operation was cancelled")

    def select_textbox(self):
        self.master.lose_focus()
        self.master.move_focus(self.textbox)

    def select_searchbox(self):
        self.master.lose_focus()
        self.master.move_focus(self.mdl_textbox)

    def exit_focus(self):
        self.model_title.clear()
        self.model_desc.clear()
        self.redo_title_desc()
        self.master.move_focus(self.textbox)

    def open_desc(self):
        desc = """{d}""".format(d="\n".join(map(str, textwrap.wrap(mdl_desc, 50))))
        desc = cleandoc(desc)
        # desc1 = [x + "'," for x in desc]
        # desc2 = ["'" + y for y in desc1]
        # desc3 = str(desc2)[1:-1]
        self.master.show_message_popup(mdl, desc)

    def redo_title_desc(self):
        self.model_title.clear()
        self.model_desc.clear()
        for m in genai.list_models():
            if str(m.name)[7:] == mdl:
                mdl_desc = m.description
                mdl_dn = m.display_name
        model_title = """{mdl}""".format(mdl=mdl)
        self.model_title.set_text(model_title)
        model_desc = """{model_desc}""".format(model_desc=textwrap.fill(mdl_desc, 33))
        model_desc = cleandoc(model_desc)
        self.model_desc.set_text(model_desc)
        self.textbox.set_title("Type something to: [ {mdl} ]".format(mdl=mdl_dn))
        self.master.set_title("{mdl_dn}".format(mdl_dn=mdl_dn))

    def redo_config(self):
        self.config_cell.clear()
        for m in genai.list_models():
            if str(m.name)[7:] == mdl:
                mdl_ft = m.temperature
                mdl_tp = m.top_p
                mdl_tk = m.top_k
                mdl_output = m.output_token_limit
        temp = (str(config_items[0]).split())[1]
        if float(temp) > float(mdl_ft):
            temp = mdl_ft
        topp = (str(config_items[1]).split())[2]
        if float(topp) > float(mdl_tp):
            topp = mdl_tp
        topk = (str(config_items[2]).split())[2]
        if int(topk) > int(mdl_tk):
            topk = mdl_tk
        output = (str(config_items[3]).split())[2]
        if int(output) > int(mdl_output):
            output = mdl_output
        config_items[0] = "Temperature: {ft} / {mdl_ft}".format(
            ft=str(temp), mdl_ft=str(mdl_ft)
        )
        config_items[1] = "Top P: {tp} / {mdl_tp}".format(tp=topp, mdl_tp=mdl_tp)
        config_items[2] = "Top K: {tk} / {mdl_tk}".format(tk=topk, mdl_tk=mdl_tk)
        config_items[3] = "Output Limit: {ol} / {mdl_ol}".format(
            ol=output, mdl_ol=mdl_output
        )
        self.config_cell.add_item_list(config_items)

    def run_send_prompt(self):
        self.redo_title_desc()
        self.redo_config()
        t = Thread(target=self._send_prompt)
        t.start()

    def _send_prompt(self):
        user_tokens = []
        user_chars = []
        response_tokens = []
        response_chars = []
        total_tokens = []
        total_chars = []
        global ttl_tokens
        wrapper = textwrap.TextWrapper(
            width=73, replace_whitespace=False, expand_tabs=False
        )
        prompt_text = self.textbox.get()
        if prompt_text != "":
            try:
                d_t = "User: " + str(prompt_text)
                display_text = textwrap.wrap(str(d_t), 70)
                self.chat_cell.add_item_list(display_text)
                self.textbox.clear()
                user_tokens.insert(0, str(self.tokencount(prompt_text)))
                # user_tokensc = [str(item) for item in user_tokens]
                self.user_tokens.clear()
                self.user_tokens.add_item_list(user_tokens)
                user_chars.insert(0, str(self.count_chars(prompt_text)))
                self.user_chars.clear()
                self.user_chars.add_item_list(user_chars)
                generation_config = {
                    "temperature": float_temperature,
                    "top_p": float_top_p,
                    "top_k": float_top_k,
                    "max_output_tokens": int_max_output_tokens,
                }
                model = genai.GenerativeModel(
                    model_name=mdl,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                )
                convo = model.start_chat(history=[])
                response = convo.send_message(prompt_text)
                self.master._logger.debug("RESPONSE IS: " + str(response))
                # reply = [wrapper.wrap(i) for i in str(response.text).split('\n') if i != '']
                reply = str(response.text).split("\n")
                self.master._logger.debug("SPLIT REPLY IS: " + str(reply))
                new_reply = ""
                for line in reply:
                    w = textwrap.TextWrapper(width=70, break_long_words=False)
                    line = "\n".join(w.wrap(line))
                    new_reply += line + "\n"
                # reply = '\n'.join(['\n'.join(textwrap.wrap(reply, 70, break_long_words=False, replace_whitespace=False)) for line in reply.splitlines() if line.strip() != ''])
                # reply = '\n'.join([textwrap.fill(p, 70, replace_whitespace=False) for p in reply.splitlines()])
                # reply = textwrap.wrap(reply, 70)
                # reply = response.text
                # reply = list(itertools.chain.from_iterable(reply))
                new_reply = new_reply.split("\n")
                self.master._logger.debug("CHANGED REPLY IS: " + str(new_reply))
                self.chat_cell.add_item("AI:")
                self.chat_cell.add_item_list(new_reply)
                response_tokens.insert(0, str(self.tokencount(response.text)))
                self.response_tokens.clear()
                self.response_tokens.add_item_list(response_tokens)
                response_chars.insert(0, str(self.count_chars(response.text)))
                self.response_chars.clear()
                self.response_chars.add_item_list(response_chars)
                ttl_tokens = ttl_tokens + self.tokencount(convo.history)
                total_tokens.insert(0, str(ttl_tokens))
                self.total_tokens.clear()
                self.total_tokens.add_item_list(total_tokens)
                total_chars.insert(0, str(self.count_chars_total(convo.history)))
                self.total_chars.clear()
                self.total_chars.add_item_list(total_chars)
            except BaseException as ex:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                trace_back = traceback.extract_tb(ex_traceback)
                stack_trace = list()
                for trace in trace_back:
                    stack_trace.append(
                        "File : %s , Line : %d, Func.Name : %s, Message : %s"
                        % (trace[0], trace[1], trace[2], trace[3])
                    )
                if ex_type.__name__ == "StopCandidateException":
                    ex_value = str(ex_value).splitlines()
                    ex_value = str(ex_value[1]).split()
                    self.master.show_error_popup(
                        "GOOGLE GENERATIVE AI ERROR", ex_value[1]
                    )
                else:
                    self.master.show_error_popup(ex_type.__name__, ex_value)
        # self.master.lose_focus()
        # self.redo_title_desc()
        # self.redo_config()

    def tokencount(self, input):
        generation_config = {
            "temperature": float_temperature,
            "top_p": float_top_p,
            "top_k": float_top_k,
            "max_output_tokens": int_max_output_tokens,
        }
        model = genai.GenerativeModel(
            model_name=mdl,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        cnt = model.count_tokens(input).total_tokens
        return cnt

    def count_chars(self, input):
        cnt = sum(len(i) for i in input)
        return cnt

    def count_chars_total(self, input):
        for message in input:
            cnt = len(f"{message.role} : {message.parts[0].text}")
        return cnt

    def paste_clipboard(self):
        self.master.show_yes_no_popup(
            "Your clipboard will be pasted at the end ", self.clip
        )

    def clip(self, ans):
        if ans:
            clip = pyperclip.paste()
            existing = self.textbox.get()
            pasted = existing + clip
            self.textbox.set_text(pasted)
            for i in range(75):
                self.textbox._move_right()
            self.master.move_focus(self.textbox)
            self.redo_title_desc()
            self.redo_config()

    def config_chooser(self):
        config = self.config_cell.get()
        if config.startswith("Temp"):
            self.change_temp_popup()
        elif config.startswith("Top P:"):
            self.change_top_p_popup()
        elif config.startswith("Top K:"):
            self.change_top_k_popup
        elif config.startswith("Output"):
            self.change_output_popup()

    def change_temp_popup(self):
        for m in genai.list_models():
            if str(m.name)[7:] == mdl:
                mdl_ft = m.temperature
        text_to_show = "Enter new temperature: (0 - {temp})".format(temp=mdl_ft)
        self.master.show_text_box_popup(text_to_show, self.change_temp)
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_temp(self, temp):
        try:
            temp = float(temp)
            if 0 <= float(temp) <= float(mdl_ft):
                config_items[0] = "Temperature: {ft} / {mdl_ft}".format(
                    ft=str(temp), mdl_ft=str(mdl_ft)
                )
                global float_temperature
                float_temperature = float(temp)
                self.config_cell.clear()
                self.config_cell.add_item_list(config_items)
            else:
                self.master.show_error_popup(
                    "ERROR",
                    "< {temp} > is not within the range of 0 to {mdl_ft}".format(
                        temp=temp, mdl_ft=mdl_ft
                    ),
                )
        except ValueError as e:
            self.master.show_error_popup(
                "ERROR", "< {temp} > is not a number!".format(temp=temp)
            )
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_top_p_popup(self):
        for m in genai.list_models():
            if str(m.name)[7:] == mdl:
                mdl_tp = m.top_p
        text_to_show = "Enter new TOP P: (0 - {top_p})".format(top_p=mdl_tp)
        self.master.show_text_box_popup(text_to_show, self.change_top_p)
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_top_p(self, topp):
        try:
            topp = float(topp)
            if 0 <= int(topp) <= int(mdl_tp):
                config_items[1] = "Top P: {tp} / {mdl_tp}".format(
                    tp=topp, mdl_tp=mdl_tp
                )
                global float_top_p
                float_top_p = float(topp)
                self.config_cell.clear()
                self.config_cell.add_item_list(config_items)
            else:
                self.master.show_error_popup(
                    "ERROR",
                    "< {topp} > is not within the range of 0 to {mdl_tp}".format(
                        topp=topp, mdl_tp=mdl_tp
                    ),
                )
        except ValueError as e:
            self.master.show_error_popup(
                "ERROR", "< {topp} > is not a number/integer!".format(topp=topp)
            )
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_top_k_popup(self):
        for m in genai.list_models():
            if str(m.name)[7:] == mdl:
                mdl_tk = m.top_k
        text_to_show = "Enter new TOP K: (0 - {mdl_tk})".format(mdl_tk=mdl_tk)
        self.master.show_text_box_popup(text_to_show, self.change_top_k)
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_top_k(self, topk):
        try:
            topk = int(topk)
            if 0 <= int(topk) <= int(mdl_tk):
                config_items[2] = "Top K: {tk} / {mdl_tk}".format(
                    tk=topk, mdl_tk=mdl_tk
                )
                global float_top_k
                float_top_k = int(topk)
                self.config_cell.clear()
                self.config_cell.add_item_list(config_items)
            else:
                self.master.show_error_popup(
                    "ERROR",
                    "< {topk} > is not within the range of 0 to {mdl_tk}".format(
                        topk=topk, mdl_tk=mdl_tk
                    ),
                )
        except ValueError as e:
            self.master.show_error_popup(
                "ERROR", "< {topk} > is not a number/integer".format(topk=topk)
            )
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_output_popup(self):
        for m in genai.list_models():
            if str(m.name)[7:] == mdl:
                mdl_output = m.output_token_limit
        text_to_show = "Enter new Output Tokens limit: (1 - {output})".format(
            output=mdl_output
        )
        self.master.show_text_box_popup(text_to_show, self.change_output)
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    def change_output(self, output):
        try:
            output = int(output)
            if 0 < output <= int(mdl_output):
                config_items[3] = "Output Limit: {ol} / {mdl_ol}".format(
                    ol=output, mdl_ol=mdl_output
                )
                global int_max_input_tokens
                int_max_input_tokens = int(output)
                self.config_cell.clear()
                self.config_cell.add_item_list(config_items)
            else:
                self.master.show_error_popup(
                    "ERROR",
                    "< {output} > is not within the range of 1 to {mdl_ol}".format(
                        output=output, mdl_ol=mdl_output
                    ),
                )
        except ValueError as e:
            self.master.show_error_popup(
                "ERROR", "< {output} > is not a number/integer".format(output=output)
            )
        self.master.move_focus(self.config_cell)
        self.redo_title_desc()
        self.redo_config()

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": hr},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": hs},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": se},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": dc},
    ]
    safety_items = [
        "Harrassment: {hl}".format(hl=hr_setting),
        "Hate Speech: {hs}".format(hs=hs_setting),
        "Sexually Explicit: {se}".format(se=se_setting),
        "Dangerous Content: {dc}".format(dc=dc_setting),
    ]

    safety_selection = [
        "BLOCK_NONE",
        "BLOCK_ONLY_HIGH",
        "BLOCK_MEDIUM_AND_ABOVE",
        "BLOCK_LOW_AND_ABOVE",
    ]

    def safety_chooser(self):
        safety = self.safety_cell.get()
        if safety.startswith("Harr"):
            self.safety_harr_popup()
        elif safety.startswith("Hate"):
            self.safety_hate_popup()
        elif safety.startswith("Sexu"):
            self.safety_sexu_popup()
        elif safety.startswith("Dang"):
            self.safety_dang_popup()

    def safety_harr_popup(self):
        self.master.show_menu_popup("Harrassment", safety_selection, self.safety_harr)
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_harr(self, harr):
        global hr
        hr = harr
        safety_items[0] = "Harrassment: {hl}".format(hl=hr)
        self.safety_cell.clear()
        self.safety_cell.add_item_list(safety_items)
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_hate_popup(self):
        self.master.show_menu_popup("Hate Speech", safety_selection, self.safety_hate)
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_hate(self, hate):
        global hs
        hs = hate
        safety_items[1] = "Hate Speech: {hl}".format(hl=hs)
        self.safety_cell.clear()
        self.safety_cell.add_item_list(safety_items)
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_sexu_popup(self):
        self.master.show_menu_popup(
            "Sexually Explicit", safety_selection, self.safety_sexu
        )
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_sexu(self, sexu):
        global se
        se = sexu
        safety_items[2] = "Sexually Explicit: {se}".format(se=se)
        self.safety_cell.clear()
        self.safety_cell.add_item_list(safety_items)
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_dang_popup(self):
        self.master.show_menu_popup(
            "Dangerous Content", safety_selection, self.safety_dang
        )
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def safety_dang(self, dang):
        global dc
        dc = dang
        safety_items[3] = "Dangerous Content: {dc}".format(dc=dc)
        self.safety_cell.clear()
        self.safety_cell.add_item_list(safety_items)
        self.master.move_focus(self.safety_cell)
        self.redo_title_desc()
        self.redo_config()

    def save_chat_popup(self):
        title = mdl + " - " + (datetime.now()).strftime("%d-%m-%Y %H-%M-%S")
        self.master.show_text_box_popup(
            "Save chat as?", self.save_chat, initial_text=title
        )

    def save_chat(self, final_title):
        chat = self.chat_cell.get_item_list()
        show_title = str(dir) + str("\\") + str(final_title) + str(".txt")
        with open(show_title, "w") as f:
            for line in chat:
                f.write(f"{line}\n")
            f.close()
        self.master.show_warning_popup(
            "{dir}".format(dir=dir), str(final_title) + str(".txt")
        )

    # ----------------------------------------------------------------
    # PAGE 2
    # ----------------------------------------------------------------

    def change_page(self):
        # self.master.lose_focus()
        self.master.apply_widget_set(self.change_mdl)
        self.show_models
        self.master.set_status_bar_text("< Q > to exit | < SPACE > to search models")

    def model_selection_popup(self):
        global mdl
        mdl = self.models_show.get()
        self.master.show_yes_no_popup(
            "Selected: < {mdl} > ".format(mdl=mdl), self.model_selection
        )

    def _model_cancel(self):
        self.master.lose_focus()
        self.master.show_warning_popup("Selection cancelled!", "Returned to Chat")
        self.model_selection(1)

    def model_selection(self, choice):
        # self.master.lose_focus()
        if choice:
            self.master.apply_widget_set(self.main)
            self.redo_title_desc()
            self.redo_config()
            self.chat_cell.clear()
            self.master.set_status_bar_text(
                "< Q > to exit | < SPACE > to send a message | < CTRL + S > to save chat"
            )
            self.master.move_focus(self.textbox)
        else:
            self.master.move_focus(self.models_show)

    def show_models(self):
        models_list = []
        self.models_show.clear()
        for m in genai.list_models():
            models_list.append(m.name[7:])
        self.models_show.add_item_list(models_list)
        self.model_display(0, 0)
        # self.master.move_focus(self.models_show)

    # just in case you want to async load the descriptions
    def run_model_display(self, idx, type):
        # self.master.move_focus(self.models_show)
        t = Thread(target=self.model_display(idx, type))
        t.start()

    def scroll_up(self):
        if self.models_show.get_selected_item_index() <= 0:
            idx = 0
            # self.mdl_inp.set_text(str("UP - " + str(idx)))
        else:
            idx = self.models_show.get_selected_item_index() - 1
            # self.mdl_inp.set_text(str("DOWN - " + str(idx)))
        # self.mdl_ver.set_text(str(idx))
        type = "UP"
        self.model_display(idx, type)

    def scroll_down(self):
        idx_count = len(self.models_show.get_item_list()) - 1
        if self.models_show.get_selected_item_index() > idx_count - 1:
            idx = self.models_show.get_selected_item_index()
            # self.mdl_oup.set_text(str("UP"))
        elif self.models_show.get_selected_item_index() == 0:
            idx = 1
            # self.mdl_oup.set_text(str("MID"))
        else:
            idx = self.models_show.get_selected_item_index() + 1
            # self.mdl_oup.set_text(str("DOWN"))
        # self.mdl_ver.set_text(str(idx))
        type = "DOWN"
        self.model_display(idx, type)

    def scroll_home(self):
        idx = 0
        self.model_display(idx, 0)

    def scroll_end(self):
        idx = len(self.models_show.get_item_list()) - 1
        self.model_display(idx, 0)

    def scroll_page_up(self):
        if self.models_show.get_selected_item_index() - 5 <= 0:
            idx = 0
        else:
            idx = self.models_show.get_selected_item_index() - 5
        type = "P_UP"
        self.model_display(idx, type)

    def scroll_page_down(self):
        idx_count = len(self.models_show.get_item_list()) - 1
        if self.models_show.get_selected_item_index() + 5 > idx_count - 1:
            idx = idx_count
        elif self.models_show.get_selected_item_index() == 0:
            idx = 5
        else:
            idx = self.models_show.get_selected_item_index() + 5
        type = "P_DOWN"
        self.model_display(idx, type)

    def mouse_select(self):
        idx = self.models_show.get_selected_item_index()
        self.model_display(idx, 0)

    def model_display(self, idx, type):
        idx_count = len(self.models_show.get_item_list()) - 1
        sel_mdl = self.models_show.get_selected_item_index()
        if sel_mdl <= 0:
            set_mdl = 0
        elif sel_mdl > idx_count:
            set_mdl = idx_count
        else:
            if type == "UP":
                set_mdl = idx + 1
            elif type == "DOWN":
                set_mdl = idx - 1
            elif type == "P_UP":
                set_mdl = idx + 5
            elif type == "P_DOWN":
                set_mdl = idx - 5
            else:
                set_mdl = idx
            # down is - X
            # up is + X
            # no idea why its opposite here since both start at 0
        self.models_show.set_selected_item_index(set_mdl)
        lst_mdl = self.models_show.get_item_list()
        lst_mdl = lst_mdl[idx]
        self.mdl_sum.set_text(str(lst_mdl))
        self.mdl_display2(lst_mdl)

    def mdl_display2(self, sef_mdl):
        mdl_dn = ""
        mdl_de = ""
        mdl_t = ""
        mdl_p = ""
        mdl_k = ""
        mdl_v = ""
        mdl_i = ""
        mdl_o = ""
        mdl_g = ""
        for m in genai.list_models():
            if str(m.name[7:]) == sef_mdl:
                mdl_dn = m.display_name
                mdl_de = m.description
                mdl_v = m.version
                mdl_t = m.temperature
                mdl_p = m.top_p
                mdl_k = m.top_k
                mdl_i = m.input_token_limit
                mdl_o = m.output_token_limit
                mdl_g = m.supported_generation_methods
        self.mdl_sum.clear()
        self.mdl_sum.set_text(cleandoc("""{mdl_dnm}""".format(mdl_dnm=mdl_dn)))
        self.change_mdl_sel.clear()
        self.change_mdl_sel.set_text(
            cleandoc("""{mdl_de}""".format(mdl_de=textwrap.fill(mdl_de, 70)))
        )
        self.mdl_temp.clear()
        self.mdl_temp.set_text("{mdl_t}".format(mdl_t=mdl_t))
        self.mdl_p.clear()
        self.mdl_p.set_text("{mdl_p}".format(mdl_p=mdl_p))
        self.mdl_k.clear()
        self.mdl_k.set_text("{mdl_k}".format(mdl_k=mdl_k))
        self.mdl_ver.clear()
        self.mdl_ver.set_text("{mdl_v}".format(mdl_v=mdl_v))
        self.mdl_inp.clear()
        self.mdl_inp.set_text("{mdl_i}".format(mdl_i=mdl_i))
        self.mdl_oup.clear()
        self.mdl_oup.set_text("{mdl_o}".format(mdl_o=mdl_o))
        self.mdl_gen.clear()
        gen = " ".join(mdl_g)
        gen = textwrap.fill(gen, 20)
        self.mdl_gen.set_text(gen)

    def search_models(self):
        search_term = self.mdl_textbox.get()
        models_list = []
        self.models_show.clear()
        for m in genai.list_models():
            if search_term in str(m.name[7:]):
                models_list.append(m.name[7:])
        self.models_show.add_item_list(models_list)
        self.model_display(0, 0)


# Create the CUI, pass it to the wrapper object, and start it
# root = py_cui.PyCUI(8, 9)
root = MyCUI(8, 9)
root.exit_key = None
root.set_title("GEMINI PRO CLI")
root.toggle_unicode_borders()
# root.enable_logging(logging_level=logging.DEBUG)
# root.enable_logging(logging_level=logging.INFO)
# root.enable_logging(logging_level=logging.ERROR)
# root.enable_logging(logging_level=logging.WARN)
root.enable_logging(logging_level=logging.CRITICAL)
##root.is_live_debug_mode()
root.set_refresh_timeout(0.5)
s = centermenu(root)
root.start()
