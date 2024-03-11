import os
from typing import Any


class CodeAppender:
    def __init__(self, dir="./") -> None:
        self.dir = dir
        self.func_name = "append_code"
        self.description = "Append code to the existing file. You MUST call read_code before calling this function."
        self.parameters = {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to be written. e.g. 'src/main.py'",
                },
                "code": {"type": "string", "description": "The code to be appended"},
                "description": {
                    "type": "string",
                    "description": "A brief description of what your code does. Be sure to include any dependencies your code needs, such as file paths or variables.",
                },
            },
            "required": ["path", "code", "description"],
        }

    def as_dict(self):
        return {
            "type": "function",
            "function": {
                "name": self.func_name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __call__(self, path: str, code: str, description: str) -> Any:
        # if path contains a directory, create it
        real_path = os.path.join(self.dir, path)
        last_slash = real_path.rfind("/")
        if last_slash != -1:
            directory = real_path[:last_slash]
            print(f"Creating directory {directory}")
            os.makedirs(directory, exist_ok=True)

        print(f"Append code to: {real_path}")
        print(f"Code: {code}")
        with open(real_path, "a+") as f:
            f.write(code)

        observation = self._generate_observation(path, code, description)
        return observation

    def _generate_observation(self, path: str, code: str, description: str) -> str:
        return f"""You appended code to the existing file.\nFile path: \n{path}\nDescription: \n{description}\n"""
