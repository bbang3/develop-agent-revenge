import os
from typing import Any


class CodeWriter:
    func_name = "write_code"
    description = "Write code that implements the given task."
    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the file to be written. e.g. 'src/main.py'",
            },
            "code": {"type": "string", "description": "The code you generated"},
            "description": {
                "type": "string",
                "description": "A brief description of what your code does. Be sure to specify any dependencies your code needs, such as file paths, Element identifiers, API endpoints, etc.",
            },
        },
        "required": ["path", "code", "description"],
    }

    def __init__(self, dir="./") -> None:
        self.dir = dir

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

        print(f"Saving file to {real_path}")
        with open(real_path, "w") as f:
            f.write(code)

        observation = self._generate_observation(path, code, description)
        return observation

    def _generate_observation(self, path: str, code: str, description: str) -> str:
        return f"""You write a code file.\nFile path: \n{path}\nDescription: \n{description}\n"""
