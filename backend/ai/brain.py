from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random

from .memory import load_memory, save_memory

model = SentenceTransformer('all-MiniLM-L6-v2')
memory = load_memory()


def encode(text):
    return model.encode([text])[0]


def generate_reply(text):
    # 会話っぽい生成
    if "こんにちは" in text:
        return random.choice([
            "こんにちは、今日はどうしたの？",
            "やあ、何してるの？",
            "こんにちは、話し相手になるよ"
        ])

    if "元気" in text:
        return random.choice([
            "まあまあかな、あなたは？",
            "元気だよ、そっちは？",
            "普通かな、今日はどう？"
        ])

    if "疲れ" in text:
        return "無理しすぎないほうがいいよ"

    if "暇" in text:
        return "何か話す？それともおすすめ出そうか"

    # デフォルト
    return random.choice([
        "それもう少し詳しく教えて",
        "なるほど、それで？",
        "それってどういう意味？",
        "もう少し聞かせて"
    ])


def get_reply(user_text):
    global memory

    # 記憶がある場合は類似検索
    if len(memory) > 0:
        user_vec = encode(user_text)

        scores = []
        for m in memory:
            vec = encode(m["user"])
            score = cosine_similarity([user_vec], [vec])[0][0]
            scores.append(score)

        best = int(np.argmax(scores))

        if scores[best] > 0.75:
            return memory[best]["ai"]

    # なければ生成
    return generate_reply(user_text)


def learn(user, ai):
    global memory

    memory.append({
        "user": user,
        "ai": ai
    })

    save_memory(memory)