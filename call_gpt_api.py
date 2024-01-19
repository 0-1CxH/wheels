import openai
import argparse
import os

from chat_message_utils import ChatHistoryFileUtil, ChatHistory, ChatMessage
from prompt_shortcuts import PROMPT_SHORTCUTS

HISTORY_FOLDER_PATH = os.path.join(os.environ["WHEELS_PATH"], "data/openai_api_usage")

"""
usage: python call_gpt_api.py prompt [-m MODEL] [-c] [-j] [-s SHORTCUT] [-h HISTORY]
the first argument is the prompt, which is required
optional arguments:
-m MODEL or --model MODEL: the model name, default to "4p"(gpt-4-preview)，options are  3t(gpt-3.5-turbo-1106), 4(gpt-4), 4p(gpt-4-1106-preview)
-c or --cont: whether to continue from history, if -c is not specified, no history will be used
-j or --json: whether to use json mode, if -j is specified, json mode will be used  
-s SHORTCUT or --shortcut SHORTCUT: the shortcut name, if -s is specified, the shortcut will be used, the shortcut options are: code_explain, cmd_generate, cmd_explain, ...
-h HISTORY or --history HISTORY: the history file path, if -h is not specified, the default history file will be used
example: python call_gpt_api.py "hello world" -m 4p -c -s shortcut_name --history /path/to/history/file
this will use the shortcut "shortcut_name" to generate the response of gpt-4-preview for "hello world", and the history of "/path/to/history/file" will be used
"""

MODEL_MAP = {
    "3t": "gpt-3.5-turbo-1106",
    "4": "gpt-4",
    "4p": "gpt-4-1106-preview",
}

# the history file will be saved in the HISTORY_FOLDER_PATH folder with filename "date_time_of_conv_start.json"


parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="prompt text")
parser.add_argument("-m", "--model", help="model name", default="4p")
parser.add_argument("-c", "--cont", help="continue from history", action="store_true")
parser.add_argument("-j", "--json", help="json mode", action="store_true")
parser.add_argument("-s", "--shortcut", help="shortcut name")
# parser.add_argument("-h", "--history", help="history file path")
parser.add_argument( "--history", help="history file path")
args = parser.parse_args()

openai_client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://api.openai.com/v1"
)


def get_history_messages(cont, history_file_path):
    """
    :param cont: -c option
    :param history_file_path: -h option
    :return: the history messages (ChatHistory object) or None if no history file is found
    """
    # if cont is True or history_file_path is not None
    # (which means even if cont is False, the history file path is specified, still load the history file)
    if cont or history_file_path:
        if not history_file_path:  # if cont is True and history_file_path is None, scan the most recent history file
            history_file_path = ChatHistoryFileUtil.scan_recent_history_files(HISTORY_FOLDER_PATH, 30)
        if history_file_path:
            history = ChatHistory.load_from_file(history_file_path)
            return history_file_path, history


def get_shortcut_system_message(shortcut):
    """
    :param shortcut: the shortcut name
    :return: the system message (ChatMessage object) or None if no shortcut is found
    """
    if shortcut:
        if shortcut in PROMPT_SHORTCUTS:
            return ChatMessage(
                role="system",
                content=PROMPT_SHORTCUTS[shortcut],
                original_content="",
            )
        else:
            return None


# check the model name
assert args.model in MODEL_MAP


# load ChatHistory or init ChatHistory if no history file is found
res = get_history_messages(args.cont, args.history)
if res is not None:
    using_hist_file_path, main_chat_history_obj = res
else:
    using_hist_file_path, main_chat_history_obj = None, None
if main_chat_history_obj is None:
    main_chat_history_obj = ChatHistory(
        model=MODEL_MAP[args.model],
        shortcut=args.shortcut,
        messages=[]
    )
assert isinstance(main_chat_history_obj, ChatHistory)

# add the system message to the main chat history
shortcut_system_message = get_shortcut_system_message(args.shortcut)
if shortcut_system_message:
    main_chat_history_obj.messages.append(shortcut_system_message)

# add the user message to the main chat history
main_chat_history_obj.messages.append(ChatMessage(
    role="user",
    content=args.prompt,
    original_content="",
))

# call the gpt api
response = openai_client.chat.completions.create(
    model=main_chat_history_obj.model,
    response_format={"type": "json_object"} if args.json else None,
    messages=[message.to_json_object(ignore_original_content=True) for message in main_chat_history_obj.messages],
)

# convert ChatCompletion object to json string

# add the gpt response to the main chat history
main_chat_history_obj.messages.append(ChatMessage(
    role=response.choices[0].message.role,
    content=response.choices[0].message.content,
    original_content=str(response),
))

# print the response
print(response.choices[0].message.content)

# delete the old history file
if using_hist_file_path is not None and os.path.exists(using_hist_file_path):
    os.remove(using_hist_file_path)

# save the main chat history to file
main_chat_history_obj.save_to_file(
    ChatHistoryFileUtil.save_history_file(HISTORY_FOLDER_PATH, main_chat_history_obj)

)


