from openai import OpenAI
from apscheduler.schedulers.background import BackgroundScheduler

import json
import sys
import random
import requests
import time
import os

DAEMON_MODE = False
CONFIG = {}


def prompt(text=None, personality=CONFIG["personality"]):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": text},
        ],
        max_tokens=CONFIG["tokens"],
        n=CONFIG["n"],
        stop=None,
        temperature=CONFIG["temperature"],
    )

    return response.choices[0].message.content.strip()


def daemon_mode():
    scheduled = 0
    scheduler = BackgroundScheduler(daemon=True)
    if CONFIG["the_convert"]["enabled"]:
        for t in CONFIG["the_convert"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=convert"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=convert"],
                )
            scheduled += 1
    if CONFIG["news"]["enabled"]:
        for t in CONFIG["news"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=news"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=news"],
                )
            scheduled += 1
    if CONFIG["dunewatch"]["enabled"]:
        for t in CONFIG["dunewatch"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=dunewatch"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=dunewatch"],
                )
            scheduled += 1
    if CONFIG["propaganda"]["enabled"]:
        for t in CONFIG["propaganda"]["schedule"]:
            if "minutes" in t.keys():
                scheduler.add_job(
                    doPropaganda,
                    "cron",
                    hour=t["hour"],
                    minute=t["minutes"],
                    args=["--send", "--program=propaganda"],
                )
            else:
                scheduler.add_job(
                    doPropaganda,
                    "interval",
                    hour=t["hour"],
                    args=["--send", "--program=propaganda"],
                )
            scheduled += 1
    if scheduled < 1:
        print("No programs are enabled or scheduled. Please check your configuration.")
        sys.exit(255)
    scheduler.start()
    print("Daemon mode started...")
    while True:
        time.sleep(1)


def run(args):
    send = False
    program = None
    for arg in sys.argv:
        if arg == "--daemon":
            daemon_mode()
            return
        if arg == "--send":
            send = True
        if "--program" in arg:
            if "=" not in arg:
                print(
                    "Usage: --program=propaganda (Default)|convert|news|dunewatch|random"
                )
                sys.exit(255)
            program_txt = arg.split("=")[1].lower()
            if program_txt not in [
                "propaganda",
                "convert",
                "news",
                "dunewatch",
                "random",
            ]:
                print(
                    "Usage: --program=propaganda (Default)|convert|news|dunewatch|random"
                )
                sys.exit(255)
            if program:
                print("Error: --program can only be specified once.")
                sys.exit(255)
            program = program_txt
    if not program:
        program = "propaganda"
    if program == "random":
        program = random.choice(["propaganda", "convert", "news", "dunewatch"])
    doPropaganda(send=send, program=program)


def doPropaganda(send=False, program=None):
    reply, prompt_txt = None, None
    if program == "propaganda":
        personality = CONFIG["propaganda"]["personality"]
        reply, prompt_txt = getPropaganda()
    elif program == "convert":
        personality = CONFIG["the_convert"]["personality"]
        reply, prompt_txt = getConvertProgram()
    elif program == "news":
        personality = CONFIG["news"]["personality"]
        reply, prompt_txt = getHarkonnenNews()
    elif program == "dunewatch":
        personality = CONFIG["dunewatch"]["personality"]
        reply, prompt_txt = getDuneWatch()
    if not reply:
        print("Failed to get a reply from the model.")
        if DAEMON_MODE:
            return False
        sys.exit(255)
    print(
        f'\n------------------------------\nSend: {send}\nProgram: {program}\nPrompt: "{prompt_txt}"\n\n{reply}\n------------------------------\n'
    )
    if send:
        res = sendToDiscord(reply)
        if res != 200:
            print(f"Failed to send propaganda to Discord, status code: {res}")
            if res == 400:
                reply = shorten(prompt_txt=prompt_txt, personality=personality)
                if reply is False:
                    print("Failed to get a new reply after shortening.")
                    if DAEMON_MODE:
                        return False
                    sys.exit(255)
                print(
                    f'\n------------------------------\nSend: {send}\nPrompt: "{prompt_txt}"\n\n{reply}\n------------------------------\n'
                )
                res = sendToDiscord(reply)
                if res != 200:
                    print(
                        f"Failed to send shortened propaganda to Discord, status code: {res}"
                    )
                    if DAEMON_MODE:
                        return False
                    sys.exit(255)
        else:
            print("Propaganda sent successfully.")


def getPropaganda():
    prompt_txt = random.choice(CONFIG["propaganda"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, CONFIG["propaganda"]["personality"]), prompt_txt
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def getConvertProgram():
    prompt_txt = random.choice(CONFIG["the_convert"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, CONFIG["the_convert"]["personality"]), prompt_txt
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def getHarkonnenNews():
    prompt_txt = random.choice(CONFIG["news"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, CONFIG["news"]["personality"]), prompt_txt
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def getDuneWatch():
    prompt_txt = random.choice(CONFIG["dunewatch"]["prompts"])
    retries = 0
    while retries < 5:
        try:
            return (
                prompt(prompt_txt, CONFIG["dunewatch"]["personality"]),
                prompt_txt,
            )
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def shorten(prompt_txt=None, personality=CONFIG["propaganda"]["personality"]):
    new_prompt = f"Please shorten the following message very slightly, reply back with nothing but the shortened message.\n\n{prompt_txt}"
    retries = 0
    while retries < 5:
        try:
            return prompt(prompt_txt, personality)
        except Exception as e:
            retries += 1
            print(f"Error: {e}. Retrying ({retries}/5)...")
            time.sleep(30)
    return False


def sendToDiscord(reply):
    retries = 0
    url = CONFIG["url"]
    if url.endswith("/"):
        url = url[:-1]
    url = f"{url}/slack"
    while retries < 5:
        try:
            r = requests.post(url, {"text": reply})
            res = r.status_code
            if res == 400:
                return 400
            r.raise_for_status()
            return res
        except Exception as e:
            retries += 1
            err = f"Failed to send reply, retrying ({retries}/5)...\nError: {e}"
            err = err.replace(url, "https://discord.com/********")
            err = err.replace(CONFIG["openai_key"], "********")
            print(err)
            time.sleep(30)
    return res


# Entry point
if __name__ == "__main__":
    # Will be in this files parent dir's parent
    DEFAULTS_FILE = os.path.join(Path(__file__).parent.parent, "config.json")
    with open(DEFAULTS_FILE, "r") as f:
        try:
            CONFIG = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading default configuration file {DEFAULTS_FILE}: {e}")
            sys.exit(255)
    FILE = "/etc/harko-bot/config.json"
    if not os.path.exists(FILE):
        FILE = "config.json"
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            try:
                CONFIG.update(json.load(f))
            except json.JSONDecodeError as e:
                print(f"Error reading configuration file {FILE}: {e}")
                sys.exit(255)
    else:
        FILE = "/etc/harko-bot/config.json"
        print(f"Configuration file {FILE} does not exist. Using default configuration.")
        print(
            "Please edit the file with your OpenAI key and other settings if you want to use this script."
        )
        try:
            if not os.path.exists(os.path.dirname(FILE)):
                os.makedirs(os.path.dirname(FILE))
            with open(FILE, "w") as f:
                json.dump(CONFIG, f, indent=4)
        except Exception as e:
            print(f"Failed to create configuration file {FILE}: {e}")
            print("Trying to create locally...")
            try:
                with open("config.json", "w") as f:
                    json.dump(CONFIG, f, indent=4)
                print("Configuration file created locally as config.json.")
            except Exception as e:
                print(f"Failed to create local configuration file: {e}")
        sys.exit(255)

    client = OpenAI(api_key=CONFIG["openai_key"])

    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    run(args)
