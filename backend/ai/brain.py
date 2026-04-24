from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random

from .memory import load_memory, save_memory

memory = load_memory()

vectorizer = TfidfVectorizer()

def generate_reply(text):
    if "こんにちは" in text:
        return random.choice([
            "こんにちは、今日はどうしたの？",
            "やあ、元気？",
            "こんにちは、話そうか"
        ])

    if "元気" in text:
        return "まあまあかな、そっちは？"

    if "暇" in text:
        return "何か話す？"

    return random.choice([
        "それ詳しく教えて",
        "なるほど、それで？",
        "もう少し聞きたい"
    ])


def get_reply(user_text):
    global memory

    if len(memory) == 0:
        return generate_reply(user_text)

    texts = [m["user"] for m in memory]
    vectors = vectorizer.fit_transform(texts + [user_text])

    scores = cosine_similarity(
        vectors[-1], vectors[:-1]
    )[0]

    best = np.argmax(scores)

    if scores[best] > 0.6:
        return memory[best]["ai"]

    return generate_reply(user_text)


def learn(user, ai):
    global memory

    memory.append({
        "user": user,
        "ai": ai
    })

    save_memory(memory)