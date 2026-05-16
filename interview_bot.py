def coding_prompt(language, level):
    return f"""
Act as a technical interviewer.

Take interview for {language} developer.

Difficulty: {level}

Ask one coding question at a time.
Then evaluate the answer.
"""