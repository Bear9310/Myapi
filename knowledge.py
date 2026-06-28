import os

KNOWLEDGE_FOLDER = "knowledge"

def search_knowledge(query):
    query = query.lower().strip()

    if not os.path.exists(KNOWLEDGE_FOLDER):
        return None

    skip_words = ["what","is","the","a","an","tell","me","about",
                  "explain","define","how","does","do","are","was",
                  "were","can","could","please","give","show","of",
                  "for","in","on","to","and","or","write","able","who","you","developed","created","built"]

    words = [w for w in query.split() if w not in skip_words and len(w) > 1]

    if not words:
        return None

    best_match = None
    best_score = 0

    for filename in os.listdir(KNOWLEDGE_FOLDER):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(KNOWLEDGE_FOLDER, filename)

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        sections = content.strip().split("\n\n")

        for section in sections:
            section_lower = section.lower()
            first_line = section.split("\n")[0].lower()
            score = 0

            if query in section_lower:
                score += 20

            numbers = [w for w in query.split() if w.isdigit()]
            if numbers:
                if all(n in first_line for n in numbers):
                    score += 15

            first_line_matches = sum(1 for w in words if w in first_line)
            if first_line_matches == len(words):
                score += 10
            else:
                score += first_line_matches * 3

            for word in words:
                if word in section_lower:
                    score += 1

            if score > best_score:
                best_score = score
                best_match = section.strip()

    if best_score >= 5:
        return best_match

    return None
