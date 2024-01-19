import json
from dataclasses import dataclass
import os
import time

@dataclass
class ChatMessage:
    role: str
    content: str
    original_content: str

    def to_json_object(self, ignore_original_content):
        if ignore_original_content:
            return {
                "role": self.role,
                "content": self.content,
            }
        else:
            return {
                "role": self.role,
                "content": self.content,
                "original_content": self.original_content
            }

    @staticmethod
    def from_json_object(json_object):
        return ChatMessage(
            role=json_object["role"],
            content=json_object["content"],
            original_content=json_object["original_content"]
        )


@dataclass
class ChatHistory:
    model: str
    shortcut: str
    messages: list[ChatMessage]
    start_date_time: str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def to_json_object(self):
        return {
            "model": self.model,
            "shortcut": self.shortcut,
            "start_date_time": self.start_date_time,
            "messages": [message.to_json_object(ignore_original_content=False) for message in self.messages]
        }

    @staticmethod
    def from_json_object(json_object):
        return ChatHistory(
            model=json_object["model"],
            shortcut=json_object["shortcut"],
            start_date_time=json_object["start_date_time"],
            messages=[ChatMessage.from_json_object(message) for message in json_object["messages"]]
        )

    def save_to_file(self, file_path):
        with open(file_path, "w") as f:
            json.dump(self.to_json_object(), f, indent=4)

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, "r") as f:
            return ChatHistory.from_json_object(json.load(f))


class ChatHistoryFileUtil:
    @staticmethod
    def save_history_file(history_folder_path, chat_history: ChatHistory):
        """
        :param history_folder_path: the folder path to save the history file
        :param chat_history: the chat history to save
        :return: the history file path
        """
        if not os.path.exists(history_folder_path):
            os.makedirs(history_folder_path)
        file_name = time.strftime("%Y%m%d_%H%M", time.localtime()) + ".json"
        file_path = os.path.join(history_folder_path, file_name)
        chat_history.save_to_file(file_path)
        return file_path

    @staticmethod
    def scan_recent_history_files(history_folder_path, time_range):
        """
        :param history_folder_path: the folder path to scan
        :param time_range: the time range to scan, in minutes
        :return: the most recent history file path or None if no history file is found
        """
        recent_history_files = {}
        for file_name in os.listdir(history_folder_path):
            file_path = os.path.join(history_folder_path, file_name)
            if os.path.isfile(file_path):
                # the file is named as "date_time.json", example: "20240101_0930.json"
                file_name_without_extension = os.path.splitext(file_name)[0]
                date_time = file_name_without_extension.split("_")
                if len(date_time) != 2:
                    continue
                date_ = date_time[0]
                time_ = date_time[1]
                if len(date_) != 8 or len(time_) != 4:
                    continue
                try:
                    time_struct = time.strptime(date_ + time_, "%Y%m%d%H%M")
                    time_stamp = time.mktime(time_struct)
                except:
                    continue
                # if the time stamp is within the time range, and this is the most recent one, return it
                time_delta = time.time() - time_stamp
                time_delta_in_minutes = time_delta / 60
                if time_delta_in_minutes <= time_range:
                    recent_history_files[time_delta] = file_path
        if len(recent_history_files) == 0:
            return None
        else:
            return recent_history_files[min(recent_history_files.keys())]


if __name__ == '__main__':
    # test ChatHistoryFileUtil
    history_folder_path = "/Users/qhu/Wheels/data/openai_api_usage"
    chat_history = ChatHistory(
        model="4p",
        shortcut="shortcut_name",
        messages=[
            ChatMessage(role="user", content="hello world", original_content="hello world"),
            ChatMessage(role="ai", content="hello world", original_content="hello world")
        ]
    )
    # print(ChatHistoryFileUtil.save_history_file(history_folder_path, chat_history))
    print(ChatHistoryFileUtil.scan_recent_history_files(history_folder_path, 30))
    time.sleep(5)
    print(ChatHistoryFileUtil.scan_recent_history_files(history_folder_path, 1))
