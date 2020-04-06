# Smart-Mirror-Chatbot
Smart Mirror Chatbot.

## Installation

> **Install latest version of MagicMirror Project**

### Step 0: Test Audio

### Step 1: Clone the Repository:

```bash
git clone https://github.com/darkknight001/Smart-Mirror-Chatbot.git
```
### Step 2: Create virtual environment environment:

```bash
sudo apt install python3-venv
python3 -m venv magicmirror
source magicmirror/bin/activate
```
### Step 3: Install the Dependencies(In virtual Environment):

-**Install Pyaudio**

```bash
sudo apt-get install python-pyaudio python3-pyaudio
pip3 install pyaudio
```
-**Install python libraries**

```bash
pip3 install dialogflow
pip3 install google-api-core
pip3 install SpeechRecognition
pip3 install feedparser
```
-**Make Speech.sh executable**

```bash
sudo chmod u+x /home/{USER}/Smart-Mirror-Chatbot/scripts/speech.sh
```
and then test it using:

```bash
/home/{USER}/Smart-Mirror-Chatbot/scripts/./speech.sh this is a test
```
### Step 4: Test the chatbot:

-In Virtual environment:

```bash
python3 /home/{USER}/Smart-Mirror-Chatbot/Chatbot/main.py
```

