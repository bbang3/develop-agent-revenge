import os
from typing import Any


class CodeReader:
    def __init__(self, dir="./") -> None:
        self.dir = dir
        self.func_name = "read_code"
        self.description = "Read existing code from a file to understand its details."
        self.parameters = {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to read. e.g. 'src/main.py'",
                },
            },
            "required": ["path"],
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

    def __call__(self, path: str) -> Any:
        # if path contains a directory, create it
        real_path = os.path.join(self.dir, path)

        print(f"Read file: {real_path}")
        try:
            with open(real_path, "r") as f:
                code = f.read()
        except FileNotFoundError:
            return f"File not found at path: {real_path}"

        observation = self._generate_observation(path, code)
        return observation

    def _generate_observation(self, path: str, code: str) -> str:
        return f"""You read a code file.\nFile path: \n{path}\nContents: \n{code}\n"""
