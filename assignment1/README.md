# Assignment 1
- Build an agent that answers to questions user asked.
- Agent can search on the Web. Answers only if it has enough information.
- If gathering information takes more than 3 minutes, agent stops thinking and generates answer immediately.

## How to start

Create a .env file in the root directory and set the API Key values.

```python
OPENAI_API_KEY=<YOUR_API_KEY>
TAVILY_API_KEY=<YOUR_API_KEY>
```

You can run it using Poetry.
```bash
poetry install
poetry run python assignment1/main.py
```
