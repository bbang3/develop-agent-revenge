import os
import subprocess


class Terminal:
    """
    A tool that runs terminal commands and returns the output.
    Output is returned as a tuple of (stdout, stderr).
    """

    func_name = "run_terminal"
    description = "Run a single line of terminal command."
    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to run",
            },
        },
        "required": ["command"],
    }

    def __init__(self, dir="./") -> None:
        self.dir = dir  # The directory to run the command in

    def as_dict(self):
        return {
            "type": "function",
            "function": {
                "name": self.func_name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def __call__(self, command: str) -> tuple[str, str]:
        print(f"Running command: {command}")

        real_command = command
        if self.dir:
            if not os.path.exists(self.dir):
                os.system(f"mkdir {self.dir}")
            real_command = f"cd {self.dir} && {real_command}"
        popen = subprocess.Popen(
            real_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            encoding="utf-8",
        )
        (stdout, stderr) = popen.communicate()

        observation = self._generate_observation(command, stdout, stderr)
        return observation

    def _generate_observation(self, command: str, stdout: str, stderr: str) -> str:
        observation = f"""You ran a terminal command.\nCommand: {command}\n"""
        if stdout:
            observation += (
                f"""The command was executed successfully.\nOutput: \n{stdout}\n"""
            )

        else:
            observation += f"""The command failed to execute. \nError: {stderr}\n"""

        return observation


# Test
if __name__ == "__main__":
    terminal = Terminal()
    stdout, stderr = terminal({"command": "ls -l"})
    print("stdout: ", stdout)
    print("stderr: ", stderr)
