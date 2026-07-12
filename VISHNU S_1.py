# ============================================================
#   AI VOICE ASSISTANT
#   Created by : VISHNU S
#   Project    : Internship - Voice Assistant
#   Version    : 1.0
#   Description: A Python-based voice assistant that responds
#                to voice commands, tells time/date, searches
#                the web, and answers general queries.
# ============================================================

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import sys
import os
import time


# ──────────────────────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────────────────────

ASSISTANT_NAME = "Jarvis"
CREATOR_NAME   = "Vishnu S"
VERSION        = "1.0"


# ──────────────────────────────────────────────────────────────
#  INITIALIZE TEXT-TO-SPEECH ENGINE
# ──────────────────────────────────────────────────────────────

engine = pyttsx3.init()
engine.setProperty('rate', 155)      # Speech speed (words per minute)
engine.setProperty('volume', 1.0)    # Volume: 0.0 (silent) to 1.0 (max)

# Set voice — index 0 = default male, 1 = female (depends on your OS voices)
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)


# ──────────────────────────────────────────────────────────────
#  CORE FUNCTIONS
# ──────────────────────────────────────────────────────────────

def speak(text: str) -> None:
    """Convert text to speech and print to console."""
    print(f"\n  [{ASSISTANT_NAME}] >> {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """
    Capture microphone input and convert speech to text
    using Google's Speech Recognition API.
    Returns the recognized text (lowercase) or an empty string on failure.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n  [🎤] Listening... (speak now)")
        # Calibrate for ambient background noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 1.0  # Seconds of silence before stopping

        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("  [⚠️ ] Timeout — no speech detected.")
            speak("I didn't hear anything. Please try again.")
            return ""

    # ── Recognize Speech ──
    try:
        print("  [⚙️ ] Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"  [👤 You] >> {command}")
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that. Could you please repeat?")
        return ""

    except sr.RequestError as e:
        speak("Speech recognition service is unavailable. Please check your internet connection.")
        print(f"  [ERROR] RequestError: {e}")
        return ""


# ──────────────────────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ──────────────────────────────────────────────────────────────

def get_time() -> str:
    """Return the current time as a readable string."""
    now = datetime.datetime.now()
    return "The current time is " + now.strftime("%I:%M %p")


def get_date() -> str:
    """Return the current date as a readable string."""
    now = datetime.datetime.now()
    return "Today is " + now.strftime("%A, %B %d, %Y")


def get_day() -> str:
    """Return the current day of the week."""
    return "Today is " + datetime.datetime.now().strftime("%A")


def search_web(query: str) -> str:
    """Open a Google search for the given query in the default browser."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"I've opened a Google search for: {query}"


def search_wikipedia(query: str) -> str:
    """
    Fetch a short Wikipedia summary for the query.
    Handles disambiguation and missing-page errors gracefully.
    """
    try:
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=2, auto_suggest=True)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]
        return f"Multiple results found for '{query}'. Did you mean: {', '.join(options)}?"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia article found for '{query}'. Let me search the web instead."
    except Exception as e:
        return f"Couldn't retrieve Wikipedia info: {str(e)}"


def open_website(url: str, name: str) -> None:
    """Open a website in the default browser and announce it."""
    webbrowser.open(url)
    speak(f"Opening {name} for you.")


# ──────────────────────────────────────────────────────────────
#  COMMAND PROCESSOR
# ──────────────────────────────────────────────────────────────

def process_command(command: str) -> bool:
    """
    Match the command string against known intents and respond.
    Returns False if the exit command is detected, True otherwise.
    """

    # ── Greeting ──────────────────────────────────────────────
    if any(word in command for word in ["hello", "hi", "hey", "good morning",
                                        "good afternoon", "good evening"]):
        greetings = {
            "good morning"  : "Good morning! I'm ready to assist you.",
            "good afternoon": "Good afternoon! How can I help you today?",
            "good evening"  : "Good evening! What can I do for you?",
        }
        for key, response in greetings.items():
            if key in command:
                speak(response)
                return True
        speak(f"Hello! I am {ASSISTANT_NAME}, your voice assistant created by {CREATOR_NAME}. How can I help you?")

    # ── Identity ───────────────────────────────────────────────
    elif any(phrase in command for phrase in ["your name", "who are you", "what are you"]):
        speak(f"I am {ASSISTANT_NAME}, an AI voice assistant created by {CREATOR_NAME}. "
              f"I can help you with time, date, web searches, and much more!")

    elif any(phrase in command for phrase in ["who created you", "who made you", "who built you"]):
        speak(f"I was created by {CREATOR_NAME} as part of an internship project. "
              f"A talented Electronics and Communication Engineering student!")

    # ── Time & Date ────────────────────────────────────────────
    elif "time" in command:
        speak(get_time())

    elif any(word in command for word in ["date", "today's date"]):
        speak(get_date())

    elif "day" in command:
        speak(get_day())

    # ── Wikipedia / Knowledge ──────────────────────────────────
    elif any(phrase in command for phrase in ["who is", "what is", "tell me about",
                                              "explain", "describe", "definition of"]):
        query = (command
                 .replace("who is", "")
                 .replace("what is", "")
                 .replace("tell me about", "")
                 .replace("explain", "")
                 .replace("describe", "")
                 .replace("definition of", "")
                 .strip())
        if query:
            speak(f"Let me find information about {query}.")
            result = search_wikipedia(query)
            speak(result)
            # If Wikipedia failed, fall back to web search
            if "Couldn't retrieve" in result or "No Wikipedia" in result:
                search_web(query)
        else:
            speak("Please specify what you'd like to know about.")

    # ── Web Search ─────────────────────────────────────────────
    elif any(phrase in command for phrase in ["search for", "search", "google", "look up", "find"]):
        query = (command
                 .replace("search for", "")
                 .replace("search", "")
                 .replace("google", "")
                 .replace("look up", "")
                 .replace("find", "")
                 .replace("for", "")
                 .strip())
        if query:
            speak(search_web(query))
        else:
            speak("What would you like me to search for?")

    # ── Open Websites ──────────────────────────────────────────
    elif "open youtube" in command:
        open_website("https://www.youtube.com", "YouTube")

    elif "open google" in command:
        open_website("https://www.google.com", "Google")

    elif "open github" in command:
        open_website("https://www.github.com", "GitHub")

    elif "open instagram" in command:
        open_website("https://www.instagram.com", "Instagram")

    elif "open wikipedia" in command:
        open_website("https://www.wikipedia.org", "Wikipedia")

    # ── Fun / Extras ───────────────────────────────────────────
    elif "joke" in command:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
            "Why was the JavaScript developer sad? Because he didn't know how to null his feelings.",
            "A SQL query walks into a bar, walks up to two tables and asks... Can I join you?",
        ]
        import random
        speak(random.choice(jokes))

    elif any(phrase in command for phrase in ["how are you", "are you okay", "you alright"]):
        speak("I'm doing great and fully charged to assist you! Thanks for asking.")

    elif "help" in command or "what can you do" in command:
        speak(
            "Here's what I can do: "
            "Tell you the current time and date. "
            "Search the web or Wikipedia for any topic. "
            "Open websites like YouTube, Google, and GitHub. "
            "Tell you jokes. "
            "And much more — just ask me!"
        )

    # ── Exit ───────────────────────────────────────────────────
    elif any(word in command for word in ["exit", "quit", "bye", "goodbye",
                                          "shut down", "stop", "close"]):
        speak(f"Goodbye! It was a pleasure assisting you. "
              f"This is {ASSISTANT_NAME} by {CREATOR_NAME}, signing off. Have a great day!")
        return False   # Signal to stop the main loop

    # ── Unknown / Fallback ─────────────────────────────────────
    else:
        speak(f"I heard: '{command}'. I'm not sure about that, so let me search it for you.")
        search_web(command)

    return True  # Continue running


# ──────────────────────────────────────────────────────────────
#  STARTUP BANNER
# ──────────────────────────────────────────────────────────────

def print_banner() -> None:
    """Print a styled startup banner to the console."""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║              AI VOICE ASSISTANT — {VERSION}                   ║
║                  Created by: {CREATOR_NAME}                    ║
╠══════════════════════════════════════════════════════════╣
║  Commands you can try:                                   ║
║   • "Hello" / "Hi"           → Greeting                  ║
║   • "What time is it?"        → Current time             ║
║   • "What's today's date?"    → Current date             ║
║   • "What is Python?"         → Wikipedia search         ║
║   • "Search for AI news"      → Google search            ║
║   • "Open YouTube"            → Opens browser            ║
║   • "Tell me a joke"          → Fun response             ║
║   • "Exit" / "Bye"            → Quit the assistant       ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


# ──────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT
# ──────────────────────────────────────────────────────────────

def main() -> None:
    """Main loop — listen for commands and process them."""
    print_banner()
    speak(f"Hello! I am {ASSISTANT_NAME}, your AI voice assistant, created by {CREATOR_NAME}. "
          f"I'm ready to help. Just say something!")

    while True:
        try:
            command = listen()
            if command:
                should_continue = process_command(command)
                if not should_continue:
                    break
        except KeyboardInterrupt:
            speak("Interrupted by user. Goodbye!")
            print("\n  [INFO] KeyboardInterrupt detected. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\n  [ERROR] Unexpected error: {e}")
            speak("An unexpected error occurred. Let me restart and try again.")
            time.sleep(1)


if __name__ == "__main__":
    main()