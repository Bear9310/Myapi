def summarize_web(text):
    if not text:
        return "No information found."

    lines = text.split("\n")

    answer = "Based on web results:\n\n"

    count = 0

    for line in lines:
        line = line.strip()

        if not line:
            continue

        answer += line + "\n"

        if line.startswith("http"):
            count += 1
            answer += "\n"

        if count >= 5:
            break

    return answer
