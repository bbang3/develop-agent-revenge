# Assignment 2
- 유저가 요청한 웹페이지를 개발해주는 에이전트를 만듭니다.
- 에이전트는 cli를 실행할 수 있습니다. cli 실행 결과를 확인할 수 있습니다. `Terminal` 이라는 도구를 만들어주세요.
- 계획 없이, 현재 상태에 대한 이해 없이 여러 파일로 나눠져야 하는 개발을 하기는 매우 어렵습니다. 현재 상태와 앞으로 해야 하는 일을 명확히 파악할 수 있도록 가벼운 `Planning`을 해봅시다.

- 테스트셋은 다음과 같습니다.
    1. Please develop a webpage that displays hello world. The port you can use is 8080. 
    2. Please develop a webpage that allows me to move a box with my mouse. The port you can use is 8080. 
    3. Develop a webpage that shows the total number of page views. Make sure to store this value because we need to show the total number of views when a new person joins. The port you can use is 8080.
    4. Please develop a simple todo webpage. The user should be able to add and delete todo and see all todos. Develop in a neumorphism style. The port you can use is 8080.
    5. Please develop a tetris game web page. Be sure to handle user inputs via keyboard. The port you can use is 8080.

## How to start
다음 명령어를 실행해주세요.
```bash
poetry install
poetry run python assignment2/main.py
```

프롬프트로 웹페이지 구현을 요청하세요. 구현한 코드는 `sandbox` 폴더에 있습니다.

정상적으로 실행되었다면, 웹서버를 구동할 수 있는 터미널 명령어가 노출됩니다.
### Example output
```
Task completed. You can serve the app by running: cd sandbox && node server.js.
If you want to edit the code, Enter additional prompts (Enter to exit): 
```

서버를 실행해본 뒤 수정할 부분이 있다면 추가 요청을 프롬프트로 다시 제공해주세요. 없다면 엔터를 눌러 프로그램을 종료해주시면 됩니다.

## Approach
Reasoning-and-Acting 방법에서 영감을 받아, 그와 유사한 Iteration 과정을 구현하였습니다.

에이전트가 유저 프롬프트에 대응하는 과정은 다음과 같습니다.

1. Reasoning phase
- 다음으로 해야 할 일을 생각합니다. "자연어로 된 한 줄의 문장"을 생성하도록 지시하였습니다.
2. Acting phase
- Reasoning phase에서 생성한 thought과, 이전의 acting history를 주고 Tool들 중 하나를 골라 행동하도록 합니다.
- OpenAI Function calling을 사용하였습니다.
- Acting의 결과는 history에 누적해서 기록됩니다. History의 형태는 다음과 같습니다.
  - Thought / Action / **Observation** (Tool 실행 결과)



### Tools
1. Code Writer
- 단일 파일로 된 코드를 작성합니다.
- Parameter: `path`,`code`,`description`
  - description은 작성한 코드에 대한 설명입니다. API endpoint 등 다른 파일과 dependency가 있을만한 내용을 중점적으로 서술하도록 했습니다.
- Observation: path, code, description (실제 작성 코드는 제외)

2. Terminal
- 한 줄로 된 터미널 명령을 실행합니다.
- Parameter: `command`
- Observation: 터미널 실행 결과

3. Code Reader
- 기존 파일에 적힌 코드 전체를 읽어옵니다.
- Parameter: `path`
- Observation: 코드 전체

4. Code Appender
- 기존 파일에 코드를 추가합니다.
- Parameter: `Code writer`와 동일
- Observation: `Code writer`와 동일

## Limitations
- 여러 파일을 작성해야 할 때, 종속성을 반영하지 않고 코드를 작성합니다. (e.g. HTML에 ID가 `todo` element를 선언해놓고 js에서 다른 ID를 참조하는 문제)
- 테트리스와 같은 복잡한 로직을 작성해야 하는 경우 온전한 코드를 작성하지 않습니다. (e.g. 함수 내에 주석만 작성하는 등)
  - 코드를 부분 수정하는 기능이 필요할 것으로 보입니다.
- 모든 히스토리를 concat하여 프롬프팅하기 때문에 컨텍스트 문제가 있습니다.
- Appender, Reader 툴을 제공하긴 하나 거의 사용되지 않습니다.

## Lessons learned
- 처음에는 고정된 Planning을 하는 것이 유리할 것이라 생각했는데, 코딩 작업의 특성상 앞선 step에 종속적인 작업들이 많아 효과적이지 않았습니다.
- ReAct를 참고하여 강화학습과 유사한 느낌으로 이전 step의 결과를 반영하여 작성해 나가도록 하는 것이 유리하다는 것을 알았습니다.
- GPT-4의 컨텍스트가 생각보다 매우 크다는 것을 알게 되었습니다. 오픈 소스 모델을 사용하면 성능이 하락할 것으로 추측됩니다 😅
- 모든 것을 모델 capacity & 프롬프팅으로 해결할 수만은 없는 것 같습니다. 아키텍처가 잘못되어 있으면 프롬프팅을 아무리 깎아도 개선되지 않습니다.