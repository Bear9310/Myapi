from answer_formatter import format_answer
from web_search import web_search
import random
import datetime
from knowledge import search_knowledge

def get_response(message, history=None):
    if history is None:
        history = []

    m = message.strip()
    ml = m.lower()
    words = ml.split()

    # ===== NAME MEMORY =====
    if "my name is" in ml:
        name = ml.split("my name is")[-1].strip().title()
        return f"Nice to meet you, {name}! I'll remember your name. 😊"

    if any(p in ml for p in ["what is my name", "what's my name", "do you know my name"]):
        for old_msg, old_resp in reversed(history):
            if "my name is" in old_msg.lower():
                name = old_msg.lower().split("my name is")[-1].strip().title()
                return f"Your name is {name}! 😊"
        return "I don't know your name yet! Tell me by saying 'my name is ...'"

    # ===== GREETINGS =====
    if any(w in ["hello", "hey", "sup", "hiya", "howdy"] for w in words) or words == ["hi"]:
        return random.choice([
            "Hello! How can I help you today? 😊",
            "Hey there! What can I do for you?",
            "Hi! Ask me anything! 💎"
        ])

    if any(p in ml for p in ["how are you", "how r u", "you okay"]):
        return "I'm running perfectly! Ready to help you with anything. 💪"

    # ===== IDENTITY =====
    if any(p in ml for p in ["who are you", "your name", "who created", "who made", "who built", "who developed", "created you", "made you", "owner", "who is your"]):
        return "I am MyAPI AI — your personal luxury AI assistant, created by Mohd Naim Ali. Built from scratch with pure Python. No OpenAI, no Google — just pure code! 🔥💎"

    # ===== THANKS =====
    if any(w in ml for w in ["thank", "thanks", "thx", "thank you"]):
        return "You're welcome! Always happy to help. 😊"

    # ===== JOKES =====
    if any(w in ml for w in ["joke", "funny", "laugh", "humor"]):
        jokes = [
            "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
            "Why did the programmer quit?\nBecause he didn't get arrays! 😄",
            "How many programmers to change a light bulb?\nNone — that's a hardware problem! 💡",
            "I told my computer I needed a break.\nNow it won't stop sending me Kit Kat ads! 😂",
            "Why do Java developers wear glasses?\nBecause they don't C#! 👓"
        ]
        return random.choice(jokes)

    # ===== TIME & DATE =====
    if ml in ["time", "what time", "current time"] or "what time is it" in ml:
        return f"Current time is {datetime.datetime.now().strftime('%I:%M %p')} 🕐"

    if ml in ["date", "today", "what date"] or any(p in ml for p in ["what day", "what is today", "today's date"]):
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d %Y')} 📅"

    # ===== MATH =====
    if any(w in ml for w in ["calculate", "solve", "compute"]):
        try:
            expr = ml
            for w in ["calculate", "solve", "compute", "what is", "="]:
                expr = expr.replace(w, "")
            expr = expr.strip()
            if expr and all(c in "0123456789+-*/(). " for c in expr):
                result = eval(expr)
                return f"🧮 {expr.strip()} = **{result}**"
        except:
            pass
        return "I couldn't solve that. Try: calculate 10 + 5 * 2"

    # ===== MOTIVATION =====
    if any(w in ml for w in ["motivat", "inspire", "sad", "depress", "lonely", "tired"]):
        quotes = [
            "Believe in yourself! Every expert was once a beginner. 💪",
            "You don't have to be great to start, but you have to start to be great! 🚀",
            "Keep going. You are doing amazing things! ⭐",
            "Every line of code you write is one step closer to your dream! 🎯",
            "Success is not final, failure is not fatal — it's the courage to continue that counts. 💎"
        ]
        return random.choice(quotes)

    # ===== FUN FACTS =====
    if any(w in ml for w in ["fact", "facts", "interesting", "did you know"]):
        facts = [
            "🍯 Honey never spoils. Archaeologists found 3000 year old honey in Egyptian tombs!",
            "🦩 A group of flamingos is called a flamboyance!",
            "🦗 The first computer bug was an actual bug — a moth found in a computer in 1947!",
            "🐙 Octopuses have three hearts and blue blood!",
            "🍌 Bananas are technically berries but strawberries are not!",
            "⚡ Lightning strikes Earth about 100 times per second!",
            "🧠 The human brain uses about 20% of your body's total energy!"
        ]
        return random.choice(facts)

    # ===== HELP =====
    if any(p in ml for p in ["help", "what can you do", "features", "commands"]):
        return """Here's what I can do for you:

💬 Chat & Conversation
🧮 Math calculations
🕐 Time and date
😂 Jokes and fun facts
💪 Motivation quotes
📰 Web search for any topic
📚 Knowledge base (physics, history, math, science, coding)
✍️ Write YouTube scripts, stories, blogs, poems
🌐 Translate languages
📝 Summarize topics
🐍 Python coding help
👤 Remember your name

Just ask me anything! 💎"""

    # ===== YOUTUBE SCRIPT WRITER =====
    if any(p in ml for p in ["write a youtube script", "youtube script", "write script for youtube", "script for youtube"]):
        topic = ml
        for p in ["write a youtube script about", "write youtube script about", "youtube script about", "write a youtube script", "youtube script for", "script for youtube about"]:
            topic = topic.replace(p, "")
        topic = topic.strip().title() or "Technology"
        return f"""🎬 YouTube Script: {topic}

[INTRO - 0:00]
Hey everyone! Welcome back to the channel!
Today we're diving into {topic} — and trust me, you don't want to miss this!
If you're new here, hit that subscribe button and let's get started!

[HOOK - 0:15]
Did you know that {topic} is changing the world as we know it?
In the next few minutes, I'm going to show you exactly why this matters to YOU.

[MAIN CONTENT - 0:30]
So let's break this down into 3 key points:

Point 1 — What is {topic}?
{topic} is one of the most important topics in today's world.
It affects millions of people and continues to grow every single day.

Point 2 — Why does {topic} matter?
Understanding {topic} gives you a massive advantage.
Whether you're a student, professional, or just curious — this knowledge is power!

Point 3 — How can YOU use {topic}?
Here are the practical steps you can take right now to benefit from {topic}...

[CALL TO ACTION - 4:30]
That's it for today's video on {topic}!
If you found this helpful, please LIKE this video — it really helps the channel!
Drop a comment below: What do YOU think about {topic}?
And don't forget to SUBSCRIBE for more content like this!

[OUTRO - 4:50]
See you in the next video — peace! ✌️

---
📊 Estimated length: 5 minutes
🏷️ Tags: {topic}, education, tutorial"""

    # ===== STORY WRITER =====
    if any(p in ml for p in ["write a story", "tell me a story", "write story", "create a story"]):
        topic = ml
        for p in ["write a story about", "write a story", "tell me a story about", "tell me a story", "write story about", "create a story about"]:
            topic = topic.replace(p, "")
        topic = topic.strip().title() or "Adventure"
        return f"""📖 Story: The {topic}

Once upon a time, in a world not so different from ours, there lived a young person with an extraordinary dream.

Their name was Alex, and they had always been fascinated by {topic}. While others laughed at their passion, Alex never gave up.

One day, everything changed. A mysterious stranger appeared at Alex's door with a challenge that would test everything they believed in. "Are you brave enough to face the truth about {topic}?" the stranger asked.

Alex took a deep breath. "Yes," they said quietly. "I am ready."

What followed was an adventure full of twists, discoveries, and moments that would forever change Alex's understanding of {topic} and of themselves.

In the end, Alex realized the most important lesson: that the journey matters more than the destination, and that true strength comes from never giving up on what you believe in.

The End. ✨

---
Want me to continue this story or write a different one?"""

    # ===== BLOG WRITER =====
    if any(p in ml for p in ["write a blog", "blog post", "write blog", "write an article"]):
        topic = ml
        for p in ["write a blog post about", "write a blog about", "blog post about", "write blog about", "write an article about"]:
            topic = topic.replace(p, "")
        topic = topic.strip().title() or "Technology"
        return f"""✍️ Blog Post: {topic}

# {topic}: Everything You Need to Know

*Published today | 5 min read*

## Introduction

In today's fast-paced world, {topic} has become more important than ever. Whether you're a beginner or an expert, understanding {topic} can transform the way you think and work.

In this article, we'll explore everything you need to know about {topic} — from the basics to advanced insights.

## What is {topic}?

{topic} refers to a fascinating area that continues to evolve and shape our modern world. At its core, it combines innovation, creativity, and practical application in ways that benefit everyone.

## Why {topic} Matters

There are several compelling reasons why {topic} deserves your attention:

**1. It's growing fast** — The field of {topic} is expanding at an unprecedented rate.

**2. It creates opportunities** — Understanding {topic} opens doors to new possibilities.

**3. It solves real problems** — {topic} addresses challenges that affect millions of people worldwide.

## Getting Started with {topic}

If you're new to {topic}, here's how to begin:

- Start with the fundamentals
- Practice consistently every day
- Connect with others who share your interest
- Stay updated with the latest developments

## Conclusion

{topic} is not just a trend — it's a fundamental shift in how we understand and interact with the world. By investing time in learning about {topic}, you're investing in your future.

*Found this helpful? Share it with someone who needs it!*

---
📝 Word count: ~300 words | Great for SEO!"""

    # ===== POEM WRITER =====
    if any(p in ml for p in ["write a poem", "poem about", "write poem", "poetry about"]):
        topic = ml
        for p in ["write a poem about", "write a poem", "poem about", "write poem about", "poetry about"]:
            topic = topic.replace(p, "")
        topic = topic.strip() or "life"
        return f"""🎭 Poem: {topic.title()}

In the world of {topic}, where wonders reside,
A journey begins with each turn of the tide.
The beauty of {topic} lights up every soul,
A piece of the puzzle that makes the world whole.

Through shadows and sunlight, through storms and through rain,
The magic of {topic} will always remain.
It whispers of stories, of dreams yet untold,
Of futures so bright and of hearts pure as gold.

So embrace what {topic} has brought to your door,
For life becomes richer when you dare to explore.
In the dance of existence, through laughter and pain,
{topic.title()} is the chorus that echoes our name.

— Written by MyAPI AI 💎"""

    # ===== TRANSLATION =====
    if any(p in ml for p in ["translate", "translation", "in english", "in hindi", "in urdu", "in arabic"]):
        # Extract the text to translate
        text = m
        for p in ["translate to english:", "translate to hindi:", "translate to urdu:", "translate:", "translation:"]:
            text = text.replace(p, "").replace(p.title(), "")
        text = text.strip()
        if text and len(text) > 3:
            return f"""🌐 Translation Request

Original text: "{text}"

For accurate translation I'm using web search to find the best result for you..."""
        return "Please provide text to translate! Example: 'Translate to English: Bonjour le monde'"

    # ===== SUMMARIZE =====
    if any(p in ml for p in ["summarize", "summary of", "brief about", "explain briefly", "in short"]):
        topic = ml
        for p in ["summarize this:", "summarize", "summary of", "brief about", "explain briefly", "in short"]:
            topic = topic.replace(p, "")
        topic = topic.strip()
        if not topic:
            return "Please tell me what to summarize! Example: 'Summarize World War 2'"

    # ===== PYTHON HELP =====
    if any(w in ml for w in ["python", "code", "programming", "function", "loop", "variable"]) and any(w in ml for w in ["how", "write", "create", "make", "example", "help"]):
        return """🐍 Python Help

Here are some Python basics:

**Print output:**

**Variables:**
**If statement:**
**For loop:**
**Function:**
**List:**
What specific Python help do you need? 😊"""

# ===== CURRENT AFFAIRS (always web search) =====
    current_affairs = ["who is", "current", "latest", "right now", "prime minister", "president", "ceo", "winner", "champion", "score", "news", "today's", "price", "rate"]
    if any(p in ml for p in current_affairs):
        web_answer = web_search(ml)
        if web_answer:
            return format_answer(web_answer, ml)


    # ===== KNOWLEDGE BASE =====
    knowledge_answer = search_knowledge(ml)
    if knowledge_answer:
        return knowledge_answer

    # ===== WEB SEARCH (last resort) =====
    # Only search web for real questions, not writing tasks
    writing_keywords = ["write", "create", "make", "generate", "compose", "draft"]
    if any(w in ml for w in writing_keywords):
        return f"I can help you write! Please be more specific. For example:\n• Write a YouTube script about [topic]\n• Write a story about [topic]\n• Write a blog post about [topic]\n• Write a poem about [topic]"

    web_answer = web_search(ml)
    if web_answer:
        return format_answer(web_answer, ml)


    # ===== HINDI/URDU/OTHER LANGUAGE =====
    hindi_chars = any(ord(c) > 127 for c in m)
    non_english = len([w for w in words if not w.isascii()]) > 0
    if hindi_chars or non_english:
        web_answer = web_search(m)
        if web_answer:
            return format_answer(web_answer, m)
        return "I detected a non-English message! I work best in English. Try asking in English! 😊"

    # ===== DEFAULT =====
    defaults = [
        "That's interesting! Try asking me about time, jokes, science, history, or ask me to write something! 💎",
        "I don't fully understand that yet. Try asking about a specific topic or say 'help' to see what I can do!",
        "Great question! I'm still learning. Try: 'write a YouTube script about AI' or 'what is quantum physics'?"
    ]
    return random.choice(defaults)
