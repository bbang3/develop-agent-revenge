# Assignment 1
- 유저가 질문하면 답해주는 에이전트를 만듭니다.
- 에이전트는 인터넷에서 검색할 수 있습니다. 답변하기 위한 충분한 정보가 쌓였다면 답변합니다.
- 유저는 인내심이 없어서 3분까지만 기다려줍니다. 만약 그 때까지 답변하지 않았다면 그 때까지의 정보를 토대로 답변합니다.

## How to start

루트 디렉토리에 `.env` 파일을 생성한 후 API Key 값을 설정해주세요.
```python
OPENAI_API_KEY=<YOUR_API_KEY>
TAVILY_API_KEY=<YOUR_API_KEY>
```

Poetry를 이용해 실행할 수 있습니다.
```bash
poetry install
poetry run python assignment1/main.py
```