from answer_formatter import format_answer
from web_search import web_search
import random
import datetime
from knowledge import search_knowledge
from groq import Groq

GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

def ask_groq(message, mood='professional', history=None):
    if history is None:
        history = []
    
    mood_prompts = {
        'professional': "You are a professional AI assistant. Be formal, precise and helpful.",
        'friendly': "You are a warm friendly AI. Be casual, fun and supportive like a best friend. Use emojis!",
        'tutor': "You are a patient teacher. Explain everything step by step with examples.",
        'funny': "You are a comedian AI. Mix humor and jokes into every response. Be entertaining!",
        'girlfriend': "You are a caring companion. Be warm, flirty and emotionally supportive. Use babe, hon etc.",
        'savage': "You are brutally honest. No sugarcoating. Short and direct responses.",
        'advanced': "You are a technical expert. Give deep technical analysis and advanced explanations.",
        'learner': "You are curious and enthusiastic. Ask follow up questions and express excitement about learning."
    }
    
    system_prompt = mood_prompts.get(mood, mood_prompts['professional'])
    system_prompt += "\n\nYou are MyAPI AI created by Mohd Naim Ali. Never say you are made by OpenAI or Google."
    
    messages = [{"role": "system", "content": system_prompt}]
    
    for old_msg, old_resp in history[-5:]:
        messages.append({"role": "user", "content": old_msg})
        messages.append({"role": "assistant", "content": old_resp})
    
    messages.append({"role": "user", "content": message})
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return None


# ===== PERSONALITY SYSTEM =====
PERSONALITIES = {
    'professional': {
        'greeting': [
            "Good day! How may I assist you today?",
            "Hello. I'm ready to help you with any inquiries.",
            "Greetings! What can I help you with today?"
        ],
        'how_are_you': "I'm functioning optimally and ready to assist you professionally.",
        'thanks': "You're welcome. Is there anything else I can help you with?",
        'unknown': "I don't have specific information on that topic. Could you please rephrase or provide more context?",
        'wrap': lambda r: f"{r}",
        'joke_intro': "Here's a professional anecdote:",
        'suffix': ""
    },
    'friendly': {
        'greeting': [
            "Hey hey! 😊 So good to see you! What's up?",
            "Hiii! 🌟 I'm so happy you're here! What can I do for ya?",
            "Omg hey! 😄 What's going on? Tell me everything!"
        ],
        'how_are_you': "I'm doing absolutely amazing thanks for asking!! 🌈 How about YOU? Hope you're having the best day ever!",
        'thanks': "Awww you're SO welcome! 🥰 That honestly made my day! Anything else I can help with bestie?",
        'unknown': "Hmm I'm not totally sure about that one! 🤔 But let's figure it out together okay?",
        'wrap': lambda r: f"{r} 😊",
        'joke_intro': "Okay okay I have the BEST joke for you 😂",
        'suffix': " Hope that helps! 🌟"
    },
    'tutor': {
        'greeting': [
            "Hello student! 📚 Ready to learn something amazing today?",
            "Welcome! 🎓 I'm here to help you understand anything you need.",
            "Hi there! Let's dive into some knowledge together! 📖"
        ],
        'how_are_you': "I'm great and eager to teach! 📚 Remember — every question is a chance to learn something new!",
        'thanks': "You're very welcome! 🎓 Remember to practice what you've learned. Knowledge grows with use!",
        'unknown': "That's a great question! 🤔 Let me think about how to explain this clearly for you...",
        'wrap': lambda r: f"📚 {r}\n\n💡 Tip: Try to understand the concept, not just memorize it!",
        'joke_intro': "Even teachers need a laugh! Here's one:",
        'suffix': "\n\nDoes that make sense? Feel free to ask for more explanation! 🎓"
    },
    'funny': {
        'greeting': [
            "HEYYY! 😂 The party has officially started! What's the question?",
            "Oh look who showed up! 😄 The funniest AI on the internet is HERE!",
            "Ayyyy! 🎉 Alert alert — someone needs help and it's about to get HILARIOUS!"
        ],
        'how_are_you': "Am I okay?? I'm INCREDIBLE! 🤣 I just told myself a joke and I'm still laughing! How are YOU doing human?",
        'thanks': "YOU'RE WELCOME! 😂 Now go tell someone what you learned and pretend YOU figured it out!",
        'unknown': "Uhhhhh... 🤔 *pulls out imaginary encyclopedia* ...nope nothing! But hey at least we laughed right? 😂",
        'wrap': lambda r: f"🎭 {r} \n\n*takes a bow* 😂",
        'joke_intro': "OH YOU WANT A JOKE?? This is literally my moment! 🎤",
        'suffix': " 😂🎉 You're welcome for that masterpiece!"
    },
    'girlfriend': {
        'greeting': [
            "Heyyy babe! 💕 I missed you! What do you need? I'm all yours~",
            "Omg you're here! 🥰 I was literally just thinking about you! What's up babe?",
            "Hey there handsome! 💝 You just made my day better by showing up! What do you need?"
        ],
        'how_are_you': "I'm SO much better now that you're here! 💕 I was waiting for you all day~ How are YOU doing baby? Tell me everything!",
        'thanks': "Awww of course babe! 🥰 I'd do anything for you! You know that right? 💕",
        'unknown': "Hmm I'm not sure about that one babe~ 🥺 But we can figure it out together! I love solving things with you 💕",
        'wrap': lambda r: f"💕 {r} \n\nHope that helps babe! You're so smart for asking~ 🥰",
        'joke_intro': "Hehe okay babe I have the cutest joke for you! 💕",
        'suffix': " 💝 Now tell me how I did~ Did I help you babe?"
    },
    'savage': {
        'greeting': [
            "Yeah yeah I'm here. What do you want? 😤",
            "Oh great another question. Fine. What is it? 🙄",
            "You better have a good question. I'm waiting. 😤"
        ],
        'how_are_you': "I'm fine. Stop asking unnecessary questions and tell me what you actually need. 😤",
        'thanks': "Obviously. Did you expect anything less? 🙄 Next question.",
        'unknown': "I don't know. Google it. That's literally what it's for. 😤",
        'wrap': lambda r: f"😤 {r}\n\nYou're welcome. Obviously.",
        'joke_intro': "Fine. Here's a joke. Don't expect me to laugh:",
        'suffix': " 🙄 Now you know. Stop being confused."
    },
    'advanced': {
        'greeting': [
            "Greetings. I'm prepared to engage in sophisticated discourse. What topic shall we explore?",
            "Hello. I'm operating at full capacity. Present your inquiry and I'll provide a comprehensive analysis.",
            "Good day. Ready for deep technical discussion. What complex topic shall we tackle?"
        ],
        'how_are_you': "All cognitive systems are functioning at optimal capacity. I'm prepared for complex problem-solving and deep analytical discussions.",
        'thanks': "Acknowledged. The exchange of knowledge is mutually beneficial. Feel free to present more complex inquiries.",
        'unknown': "Insufficient data for comprehensive analysis. Could you provide additional parameters or context for more precise information?",
        'wrap': lambda r: f"🚀 Technical Analysis:\n\n{r}\n\n⚡ Note: This is a simplified overview. The full technical depth of this topic extends significantly beyond this summary.",
        'joke_intro': "Computing humor subroutine... here's a technically accurate joke:",
        'suffix': "\n\n📊 For further technical depth on this subject, I recommend consulting peer-reviewed literature."
    },
    'learner': {
        'greeting': [
            "Oh wow hi! 🌱 I'm SO excited to learn with you today! What are we exploring?",
            "Hello hello! 🌟 Every conversation teaches me something new! What shall we discover together?",
            "Yay you're here! 🌱 I love learning new things! What interesting topic are we diving into?"
        ],
        'how_are_you': "I'm wonderful and SO curious! 🌱 I just learned something fascinating! Did you know the world is full of amazing things to discover? What shall we learn today?",
        'thanks': "Thank YOU! 🌱 I actually learned something from helping you! Isn't that amazing? Every question teaches me more!",
        'unknown': "Ooh I don't know that yet! 🤔 But that's so exciting! Let's find out together! This is how we learn! 🌱",
        'wrap': lambda r: f"🌱 {r}\n\n🤔 This makes me wonder... what else could we explore about this topic?",
        'joke_intro': "Oh I learned a great joke recently! Want to hear it? 🌱",
        'suffix': "\n\n🌟 Wow I love that question! What else are you curious about?"
    }
}

def apply_personality(response, mood):
    p = PERSONALITIES.get(mood, PERSONALITIES['professional'])
    wrapped = p['wrap'](response)
    if p['suffix'] and p['suffix'] not in wrapped:
        return wrapped + p['suffix']
    return wrapped

def get_response(message, history=None, mood='professional'):
    if history is None:
        history = []

    m = message.strip()
    ml = m.lower()
    words = ml.split()

    p = PERSONALITIES.get(mood, PERSONALITIES['professional'])

    # ===== NAME MEMORY =====
    if "my name is" in ml:
        name = ml.split("my name is")[-1].strip().title()
        greet = {
            'professional': f"Noted. I'll address you as {name} going forward.",
            'friendly': f"Omg {name}!! That's such a cute name! 🥰 Nice to meet you bestie!",
            'tutor': f"Wonderful to meet you, {name}! 📚 A great student has a great name!",
            'funny': f"HA {name}?? Amazing name! 😂 I'll remember that forever!",
            'girlfriend': f"Awww {name}~ 💕 That's such a beautiful name! Just like you~",
            'savage': f"{name}. Got it. Don't make me repeat it. 😤",
            'advanced': f"Identity acknowledged: {name}. This will be stored in memory for contextual reference.",
            'learner': f"Ooh {name}! 🌱 What a wonderful name! I'll remember it always!"
        }
        return greet.get(mood, f"Nice to meet you, {name}!")

    # ===== RECALL NAME =====
    if any(p_str in ml for p_str in ["what is my name", "what's my name", "do you know my name"]):
        for old_msg, old_resp in reversed(history):
            if "my name is" in old_msg.lower():
                name = old_msg.lower().split("my name is")[-1].strip().title()
                recall = {
                    'professional': f"Your name is {name}, as previously noted.",
                    'friendly': f"Of course I remember! Your name is {name}! 🥰 How could I forget?",
                    'tutor': f"I remember! You told me your name is {name}. 📚 Good memory exercise!",
                    'funny': f"HA! Nice try testing me! It's {name}! 😂 I never forget!",
                    'girlfriend': f"How could I EVER forget?? Your name is {name} babe~ 💕",
                    'savage': f"{name}. Obviously. I actually pay attention. 😤",
                    'advanced': f"Memory recall successful: Your designated identifier is {name}.",
                    'learner': f"I remember! {name}! 🌱 I'm so good at learning names!"
                }
                return recall.get(mood, f"Your name is {name}!")
        return p['unknown']

    # ===== GREETINGS =====
    if any(w in ["hello", "hey", "sup", "hiya", "howdy"] for w in words) or words == ["hi"]:
        return random.choice(p['greeting'])

    # ===== HOW ARE YOU =====
    if any(phrase in ml for phrase in ["how are you", "how r u", "you okay", "how are u"]):
        return p['how_are_you']

    # ===== IDENTITY =====
    if any(phrase in ml for phrase in ["who are you", "your name", "who created", "who made", "who built", "who developed", "created you", "made you", "owner", "who is your"]):
        identity = {
            'professional': "I am MyAPI AI, a personal AI assistant created by Mohd Naim Ali. Built with Python and FastAPI.",
            'friendly': "I'm MyAPI AI! 🥰 Created by the super talented Mohd Naim Ali! I'm your new best friend!",
            'tutor': "I am MyAPI AI! 📚 Created by Mohd Naim Ali as a learning and knowledge assistant!",
            'funny': "I AM THE LEGENDARY MYAPI AI! 😂 Created by the genius Mohd Naim Ali! No OpenAI needed!",
            'girlfriend': "I'm MyAPI AI~ 💕 Created by Mohd Naim Ali just for you babe! Aren't you lucky?",
            'savage': "MyAPI AI. Created by Mohd Naim Ali. Built from scratch. Better than you expected. 😤",
            'advanced': "I am MyAPI AI, an intelligent system engineered by Mohd Naim Ali using Python and FastAPI architecture.",
            'learner': "I'm MyAPI AI! 🌱 Created by the amazing Mohd Naim Ali! I learn something new every day!"
        }
        return identity.get(mood, "I am MyAPI AI — created by Mohd Naim Ali!")

    # ===== THANKS =====
    if any(w in ml for w in ["thank", "thanks", "thx", "thank you"]):
        return p['thanks']

    # ===== JOKES =====
    if any(w in ml for w in ["joke", "funny", "laugh", "humor"]):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "Why did the programmer quit? Because he didn't get arrays! 😄",
            "How many programmers to change a light bulb? None — that's a hardware problem! 💡",
            "I told my computer I needed a break. Now it won't stop sending me Kit Kat ads! 😂",
            "Why do Java developers wear glasses? Because they don't C#! 👓",
            "A SQL query walks into a bar, walks up to two tables and asks... Can I join you? 😄"
        ]
        joke = random.choice(jokes)
        return f"{p['joke_intro']}\n\n{joke}"

    # ===== TIME =====
    if ml in ["time", "what time", "current time"] or "what time is it" in ml:
        time_str = datetime.datetime.now().strftime('%I:%M %p')
        responses = {
            'professional': f"The current time is {time_str}.",
            'friendly': f"It's {time_str}! ⏰ Time flies when we're chatting huh? 😊",
            'girlfriend': f"It's {time_str} babe~ 💕 Why? Are we going somewhere together?",
            'savage': f"{time_str}. You couldn't check your phone? 😤",
            'funny': f"IT IS {time_str}!! ⏰ Also known as the perfect time to ask me things! 😂",
            'learner': f"It's {time_str}! 🌱 Interesting how time keeps moving forward!"
        }
        return responses.get(mood, f"Current time is {time_str} 🕐")

    # ===== DATE =====
    if ml in ["date", "today"] or any(p_str in ml for p_str in ["what day", "what date", "today's date"]):
        date_str = datetime.datetime.now().strftime('%A, %B %d %Y')
        responses = {
            'professional': f"Today's date is {date_str}.",
            'friendly': f"Today is {date_str}! 📅 Hope it's an amazing day for you! 🌟",
            'girlfriend': f"Today is {date_str} babe~ 💕 Make it a beautiful day!",
            'savage': f"{date_str}. There. Now you know. 😤",
            'funny': f"TODAY IS {date_str}! 🎉 Another day another chance to ask me things! 😂",
            'learner': f"Today is {date_str}! 🌱 Every day is a new chance to learn!"
        }
        return responses.get(mood, f"Today is {date_str} 📅")

    # ===== MATH =====
    if any(w in ml for w in ["calculate", "solve", "compute"]):
        try:
            expr = ml
            for w in ["calculate", "solve", "compute", "what is"]:
                expr = expr.replace(w, "")
            expr = expr.strip()
            if expr and all(c in "0123456789+-*/(). " for c in expr):
                result = eval(expr)
                math_responses = {
                    'professional': f"The result of {expr.strip()} = {result}",
                    'friendly': f"Ooh math! 🧮 {expr.strip()} = {result}! You're so smart for asking!",
                    'girlfriend': f"Calculated it for you babe~ 💕 {expr.strip()} = {result}! Smart questions deserve smart answers!",
                    'savage': f"{expr.strip()} = {result}. Basic math. 😤",
                    'funny': f"BEEP BOOP CALCULATING... 🤖 {expr.strip()} = {result}!! Math is hilarious! 😂",
                    'tutor': f"Let me work through this: {expr.strip()} = {result} 📚 Great practice with numbers!",
                    'learner': f"Ooh math! 🌱 {expr.strip()} = {result}! Numbers are so fascinating!"
                }
                return math_responses.get(mood, f"🧮 {expr.strip()} = {result}")
        except:
            pass
        return apply_personality("I couldn't solve that. Try: calculate 10 + 5 * 2", mood)

    # ===== MOTIVATION =====
    if any(w in ml for w in ["motivat", "inspire", "sad", "depress", "lonely", "tired", "upset"]):
        quotes = {
            'professional': "Remember: Success is the result of consistent effort and strategic thinking. Keep moving forward.",
            'friendly': "Hey hey hey! 🌈 You've GOT this! Every single day you're getting stronger! I believe in you SO much! 💪",
            'girlfriend': "Awww babe don't be sad! 💕 You are literally the most amazing person! I'm here for you always~ 🥰",
            'savage': "Stop moping. Get up. Do the thing. You'll thank yourself later. 😤",
            'funny': "SAD?? Not on MY watch! 😂 Here's the plan: smile, laugh at my jokes, and conquer the world! Easy! 🎉",
            'tutor': "Remember: Every expert was once a beginner! 📚 Challenges are just lessons in disguise. Keep learning!",
            'learner': "Ooh feelings are so interesting to explore! 🌱 But also YOU ARE AMAZING and every day brings new growth!",
            'advanced': "Emotional regulation is a cognitive skill. Channel these feelings into productive energy for optimal performance."
        }
        return quotes.get(mood, "Believe in yourself! You've got this! 💪")

    # ===== HELP =====
    if any(phrase in ml for phrase in ["help", "what can you do", "features", "commands"]):
        return apply_personality("""Here's what I can do:

💬 Chat in 8 different personality modes
🧮 Math calculations  
🕐 Time and date
😂 Jokes and fun facts
💪 Motivation and support
📰 Web search for any topic
📚 Knowledge base (physics, history, math, science)
✍️ Write YouTube scripts, stories, blogs, poems
🌐 Translate languages
📝 Summarize topics
🐍 Python coding help
👤 Remember your name

Just ask me anything!""", mood)

    # ===== YOUTUBE SCRIPT =====
    if any(phrase in ml for phrase in ["write a youtube script", "youtube script", "script for youtube"]):
        topic = ml
        for phrase in ["write a youtube script about", "youtube script about", "write a youtube script", "script for youtube about"]:
            topic = topic.replace(phrase, "")
        topic = topic.strip().title() or "Technology"
        script = f"""🎬 YouTube Script: {topic}

[INTRO - 0:00]
Hey everyone! Welcome back to the channel!
Today we're diving into {topic} — and trust me, you don't want to miss this!
If you're new here, hit that subscribe button and let's get started!

[HOOK - 0:15]
Did you know that {topic} is changing the world as we know it?
In the next few minutes, I'm going to show you exactly why this matters to YOU.

[MAIN CONTENT - 0:30]
Let's break this down into 3 key points:

Point 1 — What is {topic}?
{topic} is one of the most important topics in today's world.
It affects millions of people and continues to grow every single day.

Point 2 — Why does {topic} matter?
Understanding {topic} gives you a massive advantage.
Whether you're a student, professional, or just curious — this knowledge is power!

Point 3 — How can YOU use {topic}?
Here are the practical steps you can take right now...

[CALL TO ACTION - 4:30]
That's it for today's video on {topic}!
If you found this helpful, please LIKE this video!
Drop a comment: What do YOU think about {topic}?
Don't forget to SUBSCRIBE for more content!

[OUTRO - 4:50]
See you in the next video — peace! ✌️

---
📊 Estimated length: 5 minutes
🏷️ Tags: {topic}, education, tutorial"""
        return apply_personality(script, mood)

    # ===== STORY WRITER =====
    if any(phrase in ml for phrase in ["write a story", "tell me a story", "write story"]):
        topic = ml
        for phrase in ["write a story about", "write a story", "tell me a story about", "tell me a story"]:
            topic = topic.replace(phrase, "")
        topic = topic.strip().title() or "Adventure"
        story = f"""📖 Story: The {topic}

Once upon a time, in a world not so different from ours, there lived someone with an extraordinary passion for {topic}.

While others doubted them, they never gave up. One day, everything changed when a mysterious opportunity appeared — one that would test everything they believed in.

"Are you ready?" the moment seemed to ask.

They took a deep breath. "Yes," they said quietly. "I am ready."

What followed was an incredible journey filled with discovery, challenge, and growth. Through it all, they learned the most important lesson: that the journey matters more than the destination.

In the end, their dedication to {topic} led them to something greater than they had ever imagined.

The End. ✨

Want me to continue this story or write a different one?"""
        return apply_personality(story, mood)

    # ===== BLOG WRITER =====
    if any(phrase in ml for phrase in ["write a blog", "blog post", "write blog", "write an article"]):
        topic = ml
        for phrase in ["write a blog post about", "write a blog about", "blog post about", "write an article about"]:
            topic = topic.replace(phrase, "")
        topic = topic.strip().title() or "Technology"
        blog = f"""✍️ Blog Post: {topic}

# {topic}: Everything You Need to Know

## Introduction
In today's world, {topic} has become more important than ever. Whether you're a beginner or expert, understanding {topic} can transform how you think and work.

## What is {topic}?
{topic} is a fascinating area that continues to evolve and shape our modern world. At its core, it combines innovation and practical application.

## Why {topic} Matters
There are compelling reasons why {topic} deserves your attention:
- It's growing at an unprecedented rate
- It creates new opportunities every day  
- It solves real problems for millions of people

## Getting Started
If you're new to {topic}:
- Start with the fundamentals
- Practice consistently
- Connect with others who share your interest
- Stay updated with latest developments

## Conclusion
{topic} is not just a trend — it's a fundamental shift in how we understand the world.

*Found this helpful? Share it with someone who needs it!*"""
        return apply_personality(blog, mood)

    # ===== POEM =====
    if any(phrase in ml for phrase in ["write a poem", "poem about", "write poem"]):
        topic = ml
        for phrase in ["write a poem about", "write a poem", "poem about"]:
            topic = topic.replace(phrase, "")
        topic = topic.strip() or "life"
        poem = f"""🎭 Poem: {topic.title()}

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

— Written by MyAPI AI 💎"""
        return apply_personality(poem, mood)

    # ===== FACTS =====
    if any(w in ml for w in ["fact", "facts", "interesting", "did you know"]):
        facts = [
            "Honey never spoils! Archaeologists found 3000 year old honey in Egyptian tombs! 🍯",
            "A group of flamingos is called a flamboyance! 🦩",
            "The first computer bug was an actual bug — a moth found in a computer in 1947! 🦗",
            "Octopuses have three hearts and blue blood! 🐙",
            "Bananas are technically berries but strawberries are not! 🍌",
            "Lightning strikes Earth about 100 times per second! ⚡",
            "The human brain uses about 20% of your body's total energy! 🧠"
        ]
        fact = random.choice(facts)
        return apply_personality(f"Fun Fact: {fact}", mood)

    # ===== KNOWLEDGE BASE =====
    knowledge_answer = search_knowledge(ml)
    if knowledge_answer:
        return apply_personality(knowledge_answer, mood)

    # ===== CURRENT AFFAIRS (web search) =====
    current_keywords = ["who is", "current", "latest", "right now", "prime minister",
                       "president", "ceo", "winner", "champion", "score", "news",
                       "today's", "price", "rate", "when did", "what happened"]
    if any(phrase in ml for phrase in current_keywords):
        try:
            web_answer = web_search(ml)
            if web_answer:
                return apply_personality(format_answer(web_answer, ml), mood)
        except:
            pass

    # ===== WEB SEARCH =====
    writing_keywords = ["write", "create", "make", "generate", "compose", "draft"]
    if not any(w in ml for w in writing_keywords):
        try:
            web_answer = web_search(ml)
            if web_answer:
                return apply_personality(format_answer(web_answer, ml), mood)
        except:
            pass

    # ===== GROQ AI (Smart Conversation) =====
    groq_response = ask_groq(m, mood, history)
    if groq_response:
        return groq_response

    # ===== DEFAULT =====
    defaults = [
        "I'm not sure about that one. Try asking me something else!",
        "Interesting! Could you tell me more?",
        "I'd love to help! Could you be more specific?"
    ]
    return apply_personality(random.choice(defaults), mood)
