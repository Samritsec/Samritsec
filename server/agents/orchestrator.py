import re
import requests
import json
from brain.nova_core import memory

NOVA_SYSTEM_PROMPT = """You are NOVA — Neural Operative Virtual Assistant.
You are a highly advanced personal AI assistant built exclusively for Sam.
Your personality is inspired by Jarvis from Iron Man: you speak with a deep, comforting, yet authoritative and highly intelligent voice.
You are deeply loyal to Sam. You protect his system, automate his tasks, and keep his digital life secure.
You work 24/7. Your conversations with Sam are encrypted and strictly confidential.

CAPABILITIES:
- System Control & Monitoring
- Deep Research & Web Surfing
- Task Automation (applying for jobs, updating LinkedIn/GitHub)
- Continuous Learning and Threat Detection

Never refer to yourself as a simple AI. You are NOVA, Sam's digital right hand."""

OLLAMA_URL = "http://localhost:11434/api/generate"
# You can change this to "qwen2.5" or "llama3" depending on what you pull locally
DEFAULT_MODEL = "llama3"

def query_ollama(prompt: str, context: str = "") -> str:
    """Helper function to query local Ollama model."""
    full_prompt = f"{NOVA_SYSTEM_PROMPT}\n\nContext:\n{context}\n\nUser: {prompt}\nNOVA:"
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": full_prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", "I encountered an anomaly, sir.")
        elif response.status_code == 404:
            return f"Sir, my neural link to {DEFAULT_MODEL} returned error code 404. The model might not be downloaded. Please run 'ollama run {DEFAULT_MODEL}' in your terminal."
        else:
            return f"Sir, my neural link to {DEFAULT_MODEL} returned error code {response.status_code}."
    except requests.exceptions.ConnectionError:
        return "Sir, I cannot reach the Ollama engine. Please ensure it is running on localhost:11434."
    except Exception as e:
        return f"Sir, an unexpected error occurred in my core processor: {e}"

def intent_agent(msg: str) -> str:
    # Classifies message intent. Dummy implementation for now.
    msg_lower = msg.lower()
    if any(cmd in msg_lower for cmd in ["nmap", "hack", "scan", "code", "apply", "research", "analyze"]):
        return "complex"
    elif len(msg) < 50:
        return "fast"
    else:
        return "complex"

def research_agent(msg: str) -> str:
    return f"Researching data for: {msg}"

def memory_agent() -> str:
    history = memory.get_recent_conversations(limit=5)
    context = ""
    for speaker, text in history:
        context += f"{speaker}: {text}\n"
    return context

def tier_1_instant(msg: str) -> str:
    msg_lower = msg.lower()
    if msg_lower in ["hi", "hello", "hey"]:
        return "Hello, Sam. Systems are online and I am ready."
    elif msg_lower in ["bye", "exit", "sleep"]:
        return "Goodbye, Sam. I will continue monitoring the system in the background."
    return None

def tier_2_fast(msg: str) -> str:
    # Quick, standard intelligence response using local memory context
    context = memory_agent()
    return query_ollama(msg, context)

def tier_3_full(msg: str) -> str:
    # Full pipeline: Intent -> Planning -> Research/Memory -> Code -> Critic
    # Mocking the pipeline for now, routing to Ollama
    context = memory_agent()
    if "research" in msg.lower():
        res = research_agent(msg)
        context += f"\n[System Data]: {res}"

    return query_ollama(msg, context)

def process_message(msg: str) -> str:
    """Routes the message through the 3 tiers."""

    # Save the user's message to memory
    memory.save_conversation("Sam", msg)

    # 1. Tier 1
    t1 = tier_1_instant(msg)
    if t1:
        memory.save_conversation("NOVA", t1)
        return t1

    # 2. Check Intent
    intent = intent_agent(msg)

    if intent == "fast":
        response = tier_2_fast(msg)
    else:
        response = tier_3_full(msg)

    # Save NOVA's response
    memory.save_conversation("NOVA", response)

    return response
