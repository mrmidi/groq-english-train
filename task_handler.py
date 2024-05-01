from models import DirectToIndirectSpeechTask, DirectToInderectSpeechCheck
from typing import List
from pydantic import BaseModel
import json
from llm_interaction import llm_get_tasks, llm_explain_task, llm_check_answer

class TaskHandler:
    def fetch_task(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def submit_task(self, answer):
        raise NotImplementedError("Subclasses must implement this method.")

    def validate_answer(self, user_answer, correct_answer):
        return user_answer.strip() == correct_answer.strip()

    @property
    def jsonschema(self):
        raise NotImplementedError("Subclasses must implement this property to return schema.")

class DirectToIndirectSpeechTaskHandler(TaskHandler):
    def __init__(self):
        self.tasks: List[DirectToIndirectSpeechTask] = [
            DirectToIndirectSpeechTask(id=1, task="You are working really well, he told me.", correct_answer="He told me that I was working really well."),
            DirectToIndirectSpeechTask(id=2, task="We will meet here tomorrow, they said.", correct_answer="They said that they would meet here the next day."),
            # Add more tasks as needed
        ]
        self.current_task_index = 0

    @property
    def jsonschema(self):
        return json.dumps(DirectToIndirectSpeechTask.schema(), indent=2)

    def fetch_tasks(self):
        messages = [  # Ensure this is an assignment to a variable
            {
                "role": "system",
                "content": f"You are an English teacher that creates tasks and outputs them in JSON.\n"
                           f"Example of a tasks that should be created:\n"
                           f"“You are working really well,” he told me.\n"
                           f"They said, “We will meet here tomorrow.”\n"
                           f"She asked me: “Have you been to Berlin?”\n"
                           f"“Why do I need protective gear?” he asked.\n"
                           f"“Insert the gauge into the hole,” they said.\n"
                           # f"IDENTIFY LISTENER EXPLICITLY in each task (in parenthesis).\n"
                           # f"Avoid scenarios where listener is not defined: \"Don't be late!\" she said. She said to whom?\n"
                           # f"Another example that should be avoided: \"What is your name?\" he asked. - He asked her? me?\n"
                           f"You will create similar tasks and provide correct answers for each.\n"
                           "You output will be only JSON object starting with { and ending with }.\n"
                           f"No other content should be present in the output.\n"
                           f"The JSON object must use the schema: {self.jsonschema}",
            },
            {
                "role": "user",
                "content": "Please create 5 tasks for converting direct to indirect speech.",
            },
        ]
        return llm_get_tasks(messages)


    def explain_task(self, task_question):
        # Fetch the explanation for the task
        messages = [
            {
                "role": "system",
                "content": f"You are EXPERINCED in English teaching and you are asked to explain a task.\n"
                           f"Your student don't know how to convert direct speech to indirect.\n"
                           f"You will carefully explain how to transform his question to indirect speech.\n"
            },
            {
                "role": "user",
                "content": task_question,
            },
        ]
        return llm_explain_task(messages)


    def check_task(self, task_question, task_answer, task_id):
        # Check the task answer
        print(f"Checking task: {task_question} with answer: {task_answer}")
        task_question = task_question.strip()
        task_answer = task_answer.strip()
        messages = [
            {
                "role": "system",
                "content": f"You are an English teacher that checks student's tasks.\n"
                           f"The topic you are working on is direct to indirect speech.\n"
                           f"User will provide a sentence in direct form and his answer.\n"
                           f"As a language expert you need to check if the answer is correct.\n"
                           f"As a language expert you will grade as good answer multiple possible variants\n"
                           f"For task \"You will fail!\" he said. both varians is correct:\n"
                           f"He said that I would fail and He told him that he would fail.\n"
                           f"Another valid example: \"I will help you,\" he said. - >He said that he would help me.< or >He said that he would help him< or >he said that he would help them< are correct! \n"
                           f"As output you should provide a JSON object with the schema: {json.dumps(DirectToInderectSpeechCheck.schema(), indent=2)}"
                           "Your output will contain only JSON starting from { and ending with }. WITH NO OTHER DATA\n"
            },
            {
                "role": "user",
                "content": f"I've converted the following sentence to indirect speech: {task_question}. My answer is: {task_answer}. The id of task was {task_id} so please return the same id in the response."
            },
        ]
        return llm_check_answer(messages)

    def fetch_task(self):
        # Return the current task and increment the index
        task = self.tasks[self.current_task_index]
        self.current_task_index = (self.current_task_index + 1) % len(self.tasks)
        return task

    def submit_task(self, answer):
        # Validate the answer for the current task
        correct_answer = self.tasks[self.current_task_index - 1].correct_answer  # -1 because index has been incremented after fetch
        return self.validate_answer(answer, correct_answer)
