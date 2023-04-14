import requests
import json
from bs4 import BeautifulSoup
import re
import time
import os

# Import the appropriate library for your platform
import platform
if platform.system() == "Windows":
    import winsound
else:
    from beep import beep

def extract_json_from_html(soup):
    html_content = str(soup)
    json_matches = re.findall(r"({[\s\S]*})", html_content)

    for json_str in json_matches:
        try:
            data = json.loads(json_str)
            if "keyInfo" in data or "keys" in data or "proxies" in data or "gpt-4" in data:
                return data
        except json.JSONDecodeError:
            pass

    return None

def check_gpt4_status(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        data = extract_json_from_html(soup)

        if not data:
            return "No JSON content"

        gpt4_status = None
        quota_left = None
        if 'keyInfo' in data:
            gpt4_status = data['keyInfo']['gpt4']
            if 'quotaLeft' in data['keyInfo']:
                quota_left_data = data['keyInfo']['quotaLeft']
                if 'gpt4' in quota_left_data:
                    quota_left = quota_left_data['gpt4']
                elif 'all' in quota_left_data:
                    quota_left = quota_left_data['all']
        elif 'keys' in data:
            gpt4_status = data['keys']['gpt4']
        elif 'proxies' in data:
            gpt4_status = data['proxies']['gpt4']
        elif 'gpt-4' in data:
            gpt4_status = data['gpt-4']['all']
            if 'remaining' in data['gpt-4']:
                quota_left = data['gpt-4']['remaining']

        if gpt4_status is not None and isinstance(gpt4_status, int) and gpt4_status > 0 and quota_left is not None:
            return f"{gpt4_status} ({quota_left} quota left)"
        else:
            return gpt4_status

    except requests.exceptions.RequestException as e:
        return "Proxy down or other error encountered"
    except json.JSONDecodeError as e:
        return "Proxy down or other error encountered"

def sound_notification():
    if platform.system() == "Windows":
        frequency = 1000  # Set frequency to 1kHz
        duration = 1000  # Set duration to 1 second
        winsound.Beep(frequency, duration)
    else:
        frequency = 1000
        duration = 1
        beep(frequency, duration)

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    websites = [
        "https://whocars123-oai-proxy.hf.space/",
        "https://whocars123-oai-proxy2.hf.space/",
        "https://moxxie-knolastname-530560494330.hf.space/",
        "https://maceter636-8874416364.hf.space/",
        "https://anonjegger340-coom-tunnel.hf.space/",
        "https://idosal-oai-proxy.hf.space/",
        #Add more if needed
    ]

    previous_statuses = {}

    while True:
        clear_console()
        for url in websites:
            gpt4_status = check_gpt4_status(url)
            print(f"Website: {url}\nGPT-4 Keys: {gpt4_status}\n")

            if url not in previous_statuses:
                previous_statuses[url] = gpt4_status
            else:
                if previous_statuses[url] == 0 and gpt4_status != 0 and isinstance(gpt4_status, int):
                    sound_notification()

            previous_statuses[url] = gpt4_status
        
        time.sleep(5 * 60)  # Sleep for 5 minutes

if __name__ == "__main__":
    main()