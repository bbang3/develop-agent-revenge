SYSTEM_PROMPT = """You are an agent designed to develop a web app from a user prompt. You can use tools. If you use tools, use a tool once at a time."""


REASONING_PROMPT = """Implement a web app from a user prompt.
User prompt: {prompt}

Here is a history of what you've done so far:
{history}

What is the next step to do? Answer with a single line of natural langauge text. Don't miss any details needed for implementation.
If you think you finished the task, respond with a single text 'DONE: <terminal command to run the app>'.
"""


ACT_PROMPT = """Implement a web app from a user prompt. Refer to the history and do the following TODO.

User prompt: {prompt}

Here is a history of what you've done so far:

{history}
--------------------------------
What to do next: {thought}
"""

HISTORY_FORMAT = """Thought: {thought}
Action: {action}
Observation: {observation}
--------------------------------
"""
