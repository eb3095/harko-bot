# 🦠 Harko-Bot

**Harko-Bot** is a fully automated, dark satire Discord bot simulating propaganda broadcasts from the fictional House Harkonnen in the *Dune* universe. Powered by OpenAI's language models and triggered by a background scheduler, Harko-Bot generates stylized psyops messages and dispatches them to a Discord channel at scheduled intervals.

---

## 🧠 Features

* ⚙️ **Daemon Mode** for background scheduling of regular posts
* 🪓 Multiple themed personas:

  * `The Convert`: An Atreides defector whispering bile-laced truths
  * `DuneWatch`: Brutal psyops from Grigoriy Vadim
  * `Propaganda`: Classic regime lies and deceit
  * `News`: Daily "Harkonnen truth" broadcasts
* 📅 Configurable cron-like scheduling
* 🎭 Prompt-based random topic generation
* 📤 Discord integration via Webhook (Slack-compatible)

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourname/harko-bot.git
cd harko-bot
```

### 2. Install dependencies

```bash
pip install openai apscheduler requests
```

### 3. Configure

The script expects a JSON config file:

```bash
# Default path fallback
/etc/harko-bot/config.json
# Or local fallback
./config.json
```

If none exists, the script will create a `config.json` with default values and prompt you to edit it.

Edit the following fields:

```json
{
  "url": "https://discord.com/api/webhooks/your_webhook_here",
  "openai_key": "sk-proj-yourkeyhere",
  ...
}
```

---

## 🧪 Usage

### Run once manually

```bash
python harko-bot.py --send --program=convert
python harko-bot.py --send --program=dunewatch
python harko-bot.py --send --program=news
python harko-bot.py --send --program=propaganda
python harko-bot.py --send --program=random
```

### Run as background daemon

```bash
python harko-bot.py --daemon
```

This uses APScheduler to run all enabled programs at the times listed in the config.

---

## 🛠 Configuration

Each persona (program) has the following settings in the JSON config:

* `enabled`: Whether the bot should post for this program
* `schedule`: Cron-style schedule (`hour`, `minute`), if only hour is specified, its by interval
* `personality`: The system prompt defining how the persona writes
* `prompts`: List of prompt templates the bot will randomly select from

These are overridden by "All" which will randomly chose one of the programs at random on its allotted schedule.

### Example: `The Convert`

```json
"the_convert": {
  "enabled": true,
  "schedule": [
    {"hour": 11, "minute": 0},
    {"hour": 15, "minute": 0}
  ],
  "personality": "You are a soft, dark, and vile actor...",
  "prompts": [
    "Write an episode of The Convert..."
  ]
}
```

---

## 💡 Customization Tips

* Limit your OpenAI responses to \~1900 characters so they fit within Discord messages.
* You can edit the `prompts` section to add new content themes.
* Modify `temperature` in the root config to control creativity.

---

## ⚠️ Warning

This project intentionally uses **vitriolic, satirical, and offensive tone** in a fictional context. It is **not** intended for real-world use or propaganda. Use responsibly and only in private or clearly fictional settings.

---

## 🧾 License

MIT. You are free to use this code, but you are responsible for your own content and its implications.

---

## 🙏 Acknowledgements

* Based on the *Dune* universe by Frank Herbert
* Powered by [OpenAI](https://openai.com/)
* Inspired by dark sci-fi satire and speculative fiction themes
* Intended for use on Discord with the game Dune: Awakening
