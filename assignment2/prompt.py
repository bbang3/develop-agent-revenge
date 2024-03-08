SYSTEM_PROMPT = """You are an agent designed to develop a web app from a user prompt. If you use tools, use a tool once at a time."""


PLAN_PROMPT = """{task}

At first, write a concise plan for the implementation.
Respond ONLY with a list of steps. Each step should be written in one line.
"""


REASONING_PROMPT = """Implement a web app from a user prompt.
User prompt: {prompt}

Here is a history of what you've done so far:
{history}

What is the next step to do? Answer with a single line of text. Don't miss any details needed for implementation.
If you think you finished the task, respond with a single text 'Done'.
"""


ACT_PROMPT = """Implement a web app from a user prompt.

User prompt: {prompt}

Here is a history of what you've done so far:

{history}
--------------------------------
What to do next: {thought}
"""

OBSERVATION_FORMAT = """Thought: {thought}
Action: {action}
Observation: {observation}
--------------------------------
"""
