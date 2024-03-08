import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletionMessage
from prompt import (
    PLAN_PROMPT,
    SYSTEM_PROMPT,
    ACT_PROMPT,
    REASONING_PROMPT,
    OBSERVATION_FORMAT,
)
from tools import CodeWriter, Terminal


class Agent:
    def __init__(self, sandbox_path: str = "sandbox") -> None:
        load_dotenv()
        self.sandbox_path = sandbox_path
        if not os.path.isdir(sandbox_path):
            os.mkdir(sandbox_path)

        self.openai_client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = "gpt-4-turbo-preview"
        self.messages: list[ChatCompletionMessage] = []
        self.tools = [Terminal(sandbox_path), CodeWriter(sandbox_path)]
        self.history = ""

    def run(self) -> None:
        # Read Prompt
        user_prompt = input("Enter a prompt: ")

        thought = self.reason(user_prompt)
        while thought != "Done":
            print("<History>: ", self.history)
            self.history += self.implement(user_prompt, thought)
            thought = self.reason(user_prompt)

    def plan(self, prompt: str):
        self.messages += [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": PLAN_PROMPT.format(task=prompt)},
        ]

        response = self.call_api(self.messages)
        self.messages.append(response)
        print("Plan: \n", response.content)
        steps = response.content.split("\n")
        return steps

    def reason(self, user_prompt: str) -> None:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": REASONING_PROMPT.format(
                    prompt=user_prompt,
                    history=self.history if self.history else "None",
                ),
            },
        ]
        response = self.call_api(messages, func_mode=False)
        print("Thought: \n", response.content)
        return response.content

    def implement(
        self,
        user_prompt: str,
        thought: str,
    ) -> None:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": ACT_PROMPT.format(
                    prompt=user_prompt,
                    history=self.history if self.history else "None",
                    thought=thought,
                ),
            },
        ]
        observation = ""
        func_response = self.call_api(messages, func_mode=True)
        tool_calls = func_response.tool_calls
        if tool_calls:
            avilable_funcs = {tool.func_name: tool for tool in self.tools}
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                print(f"Tool call: {tool_call.function.name}")
                func = avilable_funcs.get(func_name)
                if func is None:
                    print("Tool not found: ", tool_call.function.name)
                    continue

                func_args = json.loads(tool_call.function.arguments)
                func_response = func(**func_args)
                print("Tool response: ", func_response)
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": func_response,
                    }
                )

                observation += OBSERVATION_FORMAT.format(
                    thought=thought,
                    action=func_name,
                    observation=func_response,
                )

        return observation

    def call_api(
        self, messages: list[ChatCompletionMessage], func_mode: bool = False
    ) -> ChatCompletionMessage:
        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=[tool.as_dict() for tool in self.tools] if func_mode else None,
        )
        return response.choices[0].message
