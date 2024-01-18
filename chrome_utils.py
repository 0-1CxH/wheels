import os
import json

CHROME_DATA_DIR = "~/Library/Application Support/Google/Chrome"
CHROME_EXECUTABLE_PATH = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"

def get_chrome_profiles():
    profiles_path = os.path.expanduser(CHROME_DATA_DIR)  # Chrome配置文件夹路径，根据实际情况进行修改

    profiles = {}
    for profile_folder in os.listdir(profiles_path):
        if not profile_folder.startswith("Profile"):
            continue
        profile_path = os.path.join(profiles_path, profile_folder)
        preferences_path = os.path.join(profile_path, "Preferences")

        if os.path.isfile(preferences_path):
            with open(preferences_path, "r") as f:
                preferences = json.load(f)
                try:
                    profile_name = preferences["account_info"][0]["full_name"]
                except:
                    continue
                profiles[profile_name] = profile_folder

    return profiles


def open_chrome_with_designated_profile(profile_name, website_url):
    profiles = get_chrome_profiles()
    print(profiles)
    if profile_name not in profiles:
        print("Profile Name NOT Found.")
        return

    profile_folder = profiles[profile_name]
    print("Profile Name Found. Opening Chrome...")
    cmd = f"{CHROME_EXECUTABLE_PATH} {website_url} --profile-directory=\"{profile_folder}\""
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    print(get_chrome_profiles())