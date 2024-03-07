import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT
from tavily import TavilyClient
from tools.websurfer import WebSurfer


class Agent:
    def __init__(self):
        load_dotenv()
        self.tavily_client = TavilyClient(os.environ.get("TAVILY_API_KEY"))
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        self.tools = [WebSurfer()]
        self.TIMEOUT = 180

    def run(self):
        query = input("Ask me anything: ")

        answer = self.answer(query)
        print(answer)

    def answer(self, query: str) -> str:
        begin_time = time.time()
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]

        # Keep asking the API for a response until it contains an answer or the timeout is reached
        last_message = ""
        while (
            "답변: " not in last_message
            and (elapsed_time := time.time() - begin_time) < self.TIMEOUT
        ):
            response_message = self.call_api(messages, func_mode=True)

            # If the response contains tool calls, process them
            if response_message.tool_calls:
                tool_calls = response_message.tool_calls
                if tool_calls:
                    messages.append(response_message)
                    available_funcs = {tool.func_name: tool for tool in self.tools}
                    for tool_call in tool_calls:
                        func_name = tool_call.function.name
                        func = available_funcs[func_name]
                        func_args = json.loads(tool_call.function.arguments)
                        func_response = func(**func_args)

                        print(f"Tool call: {tool_call.function.name}")
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": func_name,
                                "content": func_response,
                            }
                        )

            last_message = response_message.content if response_message.content else ""

        # If the last message does not contains an answer(e.g. Timeout), call the API once more
        if "답변: " not in last_message:
            last_message = self.call_api(messages, func_mode=False).content

        return last_message

    def call_api(self, messages, func_mode=False):
        response = self.openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            tools=[tool.as_dict() for tool in self.tools] if func_mode else None,
        )
        return response.choices[0].message


if __name__ == "__main__":
    agent = Agent()
    agent.run()
