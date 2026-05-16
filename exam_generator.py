def create_exam_prompt(subject, difficulty, questions):
    return f"""
Generate a {difficulty} level exam paper for {subject}.

Include:
- {questions} questions
- Mix of short and long answers
- Clean formatting
- Numbered questions
"""