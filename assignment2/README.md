# Project 2
- Created an agent that develops a web page as requested by the user.
- The agent is able to execute CLI commands. Created a tool called Terminal to allow command execution and view the results.
- Developing across multiple files without a clear plan or understanding of the current state is very difficult. Added Planning phase to clearly identify the current state and what needs to be done next.
  
- Test set is as follows:
    1. Please develop a webpage that displays hello world. The port you can use is 8080. 
    2. Please develop a webpage that allows me to move a box with my mouse. The port you can use is 8080. 
    3. Develop a webpage that shows the total number of page views. Make sure to store this value because we need to show the total number of views when a new person joins. The port you can use is 8080.
    4. Please develop a simple todo webpage. The user should be able to add and delete todo and see all todos. Develop in a neumorphism style. The port you can use is 8080.
    5. Please develop a tetris game web page. Be sure to handle user inputs via keyboard. The port you can use is 8080.

## How to start
Please run the following commands:
```bash
poetry install
poetry run python assignment2/main.py
```

Request the webpage implementation through the prompt. The implemented code is located in the `sandbox` folder.

If it runs correctly, terminal commands to start the web server will appear

### Example output
```
Task completed. You can serve the app by running: cd sandbox && node server.js.
If you want to edit the code, Enter additional prompts (Enter to exit): 
```

Try running the server. If you need to make changes, provide additional requests in the prompt. If not, press Enter to exit the program.


## Results
### Task 1
![t1](../assets/Task%201.png)
### Task 2
![t1](../assets/Task%202.png)
### Task 3
![t1](../assets/Task%203.png)
### Taks 4
![t4](../assets/Task%204.png)

## Approach
Inspired by the **Reasoning-and-Acting** method, we implemented a similar iteration process.

The process for the agent to respond to user prompts is as follows:

1. **Reasoning phase**
   - The agent thinks about what needs to be done next and generates a single sentence in natural language to describe it.

2. **Acting phase**
   - Based on the thought generated in the Reasoning phase and previous acting history, the agent chooses a Tool to execute an action.
   - OpenAI Function calling is used to implement this.
   - The result of each Acting phase is recorded in history. The history format includes:
     - **Thought** / **Action** / **Observation** (Tool execution result)

### Tools
1. **Code Writer**
   - Writes code to a single file.
   - **Parameters**: `path`, `code`, `description`
     - *Description* focuses on explaining the code, especially noting any dependencies (e.g., API endpoints).
   - **Observation**: path, code, description (actual code is excluded)

2. **Terminal**
   - Executes a one-line terminal command.
   - **Parameters**: `command`
   - **Observation**: Result of terminal execution

3. **Code Reader**
   - Reads the entire code from an existing file.
   - **Parameters**: `path`
   - **Observation**: Complete code

4. **Code Appender**
   - Adds code to an existing file.
   - **Parameters**: Same as `Code Writer`
   - **Observation**: Same as `Code Writer`

## Limitations
- When creating multiple files, the agent doesn’t account for dependencies. (e.g., defining an element with ID todo in HTML while referencing a different ID in JS)
- The agent struggles with complex logic for games like Tetris (e.g., only adding comments inside functions).
  - A feature to partially modify code might be needed.
- Prompting the full history results in context issues.
- Although Appender and Reader tools are available, they are rarely used.

## Lessons learned
- Initially, it seemed advantageous to do fixed planning, but due to dependencies between steps, this was ineffective.
- Referring to ReAct, I realized that reflecting on previous steps which is similar to reinforcement learning approach was more advantageous.
- I found that GPT-4’s context capacity is larger than expected. Using an open-source model would likely reduce performance 😅
- Not everything can be solved with model capacity & prompting alone. If the architecture is flawed, no amount of prompt tweaking can improve it.
