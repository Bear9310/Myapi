def format_answer(web_text, question):

    if not web_text:
        return "I could not find information."

    lines = [x.strip() for x in web_text.split("\n") if x.strip()]

    results = []
    current = []

    for line in lines:

        if line.startswith("http"):
            current.append(line)
            continue

        if current:
            results.append(current)
            current = []

        current.append(line)

    if current:
        results.append(current)

    answer = f"Here is what I found about: {question}\n\n"

    count = 1

    for item in results[:5]:

        answer += f"{count}. {item[0]}\n"

        for extra in item[1:]:
            answer += f"{extra}\n"

        answer += "\n"
        count += 1

    answer += "Sources were collected from web search."

    return answer
