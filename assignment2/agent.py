import json
import os
import shutil

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletionMessage
from prompt import (
    SYSTEM_PROMPT,
    ACT_PROMPT,
    REASONING_PROMPT,
    HISTORY_FORMAT,
)
from tools import CodeWriter, CodeReader, CodeAppender, Terminal


class Agent:
    def __init__(self, sandbox_path: str = "sandbox") -> None:
        _ = load_dotenv()
        self.sandbox_path = sandbox_path

        self.openai_client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = "gpt-4-turbo-preview"
        self.messages: list[ChatCompletionMessage] = []
        self.tools = [
            Terminal(sandbox_path),
            CodeWriter(sandbox_path),
            CodeReader(sandbox_path),
            CodeAppender(sandbox_path),
        ]
        self.history = ""

    def run(self) -> None:
        # Cleanup sandbox
        self.cleanup_sandbox()

        # Read Prompt
        user_prompt = input("Enter a prompt: ")

        # Reasoning-and-Acting iteration
        while True:
            thought = self.reason(user_prompt)
            if "DONE" in thought:
                # find the command to serve the app
                final_command = thought[6:]
                print(
                    f"Task completed. You can serve the app by running: cd {self.sandbox_path} && {final_command}"
                )
                # Ask for additional prompt
                additional_prompt = input(
                    "If you want to edit the code, Enter additional prompts (Enter to exit): "
                )
                if additional_prompt:
                    thought = additional_prompt
                else:
                    break

            current_history = self.implement(user_prompt, thought)
            print(current_history)
            self.history += current_history

    def reason(self, user_prompt: str) -> str:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": REASONING_PROMPT.format(
                    prompt=user_prompt,
                    history=self.history or "None",
                ),
            },
        ]
        response = self.call_api(messages, func_mode=False)
        return response.content

    def implement(
        self,
        user_prompt: str,
        thought: str,
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": ACT_PROMPT.format(
                    prompt=user_prompt,
                    history=self.history or "None",
                    thought=thought,
                ),
            },
        ]
        history = ""
        response_message = self.call_api(messages, func_mode=True)
        tool_calls = response_message.tool_calls
        action_taken = False
        if tool_calls:
            tools_dict = {tool.func_name: tool for tool in self.tools}
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func = tools_dict.get(func_name)
                if func is None:
                    print("Tool not found: ", tool_call.function.name)
                    continue

                func_args = json.loads(tool_call.function.arguments)
                func_response = func(**func_args)

                history += HISTORY_FORMAT.format(
                    thought=thought,
                    action=func_name,
                    observation=func_response,
                )
                action_taken = True

        if not action_taken:  # handling no tool calls
            history += HISTORY_FORMAT.format(
                thought=thought,
                action="None",
                observation="No action taken.",
            )

        return history

    def call_api(
        self, messages: list[ChatCompletionMessage], func_mode: bool = False
    ) -> ChatCompletionMessage:
        if func_mode:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=[tool.as_dict() for tool in self.tools],
                tool_choice="auto",
            )
        else:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )

        return response.choices[0].message

    def cleanup_sandbox(self) -> None:
        shutil.rmtree(self.sandbox_path, ignore_errors=True)
