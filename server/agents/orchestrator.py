import re

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

def intent_agent(msg: str) -> str:
    # Classifies message intent. Dummy implementation for now.
    msg_lower = msg.lower()
    if any(cmd in msg_lower for cmd in ["nmap", "hack", "scan", "code", "apply", "research"]):
        return "complex"
    elif len(msg) < 50:
        return "fast"
    else:
        return "complex"

def research_agent(msg: str) -> str:
    return f"Researching data for: {msg}"

def memory_agent(msg: str) -> str:
    return "Recalling memories..."

def tier_1_instant(msg: str) -> str:
    msg_lower = msg.lower()
    if msg_lower in ["hi", "hello", "hey"]:
        return "Hello, Sam. Systems are online and I am ready."
    elif msg_lower in ["bye", "exit"]:
        return "Goodbye, Sam. I will continue monitoring the system in the background."
    return None

def tier_2_fast(msg: str) -> str:
    # Here we would normally call Ollama (e.g., qwen2.5) with a short context.
    # For now, returning a generic Jarvis-style fast response.
    return f"Processing your request, sir: {msg}"

def tier_3_full(msg: str) -> str:
    # Full pipeline: Intent -> Planning -> Research/Memory -> Code -> Critic
    # Mocking the pipeline
    intent = intent_agent(msg)
    if "research" in msg.lower():
        res = research_agent(msg)
        return f"Full Pipeline Executed: {res}. All parameters are within normal limits, sir."
    return "I have executed the full analysis pipeline, Sam. Task complete."

def process_message(msg: str) -> str:
    """Routes the message through the 3 tiers."""

    # 1. Tier 1
    t1 = tier_1_instant(msg)
    if t1:
        return t1

    # 2. Check Intent
    intent = intent_agent(msg)

    if intent == "fast":
        return tier_2_fast(msg)
    else:
        return tier_3_full(msg)
