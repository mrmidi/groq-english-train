from models import DirectToIndirectSpeechTask, DirectToInderectSpeechCheck, VerbTenseTask, VerbTenseCheck
from typing import List
from pydantic import BaseModel
import json
from llm_interaction import llm_get_tasks, llm_explain_task, llm_check_answer, llm_fetch_tasks

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


class VerbTenseTaskHandler(TaskHandler):
    def __init__(self):
        super().__init__()
        self.tasks = [
            VerbTenseTask(
                id=1,
                sentence="They are buying a new printer because the old one ________ (break) down.",
                blanks=["has broken"],
                hints=["Use the present perfect form."]
            ),
            VerbTenseTask(
                id=2,
                sentence="She ________ (study) for her exams since last week.",
                blanks=["has been studying"],
                hints=["Use the present perfect continuous form."]
            ),
            VerbTenseTask(
                id=3,
                sentence="When I ________ (join) the company in 1999, they ________ (market) three  three versions of the model by then.",
                blanks=["joined", "had been marketing"],
                hints=["Use the simple past tense because the action (joining) happened at a specific time in the past.", "Use the past perfect continuous tense to describe an action that had been ongoing until a certain point in the past."]
            )
        ]

    def fetch_task(self):
        print("Fetching tasks")
        retries_left = 5
        while retries_left > 0:
            try:
        # Logic to fetch and return tasks
                messages = [
                    {
                        "role": "system",
                        "content": f"You are an English teacher that creates tasks and outputs them in JSON.\n"
                                   "You will create exercises for students to practice verb tenses.\n"
                                   "You will create ONLY verb tenses that student has asked for.\n"
                                   f"Example of a tasks that should be created:\n"
                                   f"They are buying a new printer because the old one ________ (break) down.\n"
                                   f"She ________ (study) for her exams since last week.\n"
                                   f"When I ________ (join) the company in 1999, they ________ (market) three  three versions of the model by then.\n"
                                   f"Can you see the square? It ________ (change).\n"
                                   f"They (demolish) the old office block and ________ (build) a fountain.\n"
                                   f"But the same trees (grow) at the lower end since we were children.\n"
                                   f"Thomas thought that Mark (tell) me about the email.\n"
                                   f"Great example of hints: Use the simple past tense because the action (joining) happened at a specific time in the past.\n"
                                   "Use the past perfect continuous tense to describe an action that had been ongoing until a certain point in the past.\n"
                                   "If answers contains already, just or similar word - ADD IT TO HINTS!\n"
                                   "Every blank should have a hint.\n"
                                   "Answer SHOULD be stored in the BLANKS field.\n"
                                   "There CAN be MULTIPLE blank in one sentence!\n"
                                   "DO NOT SHORTEN CORRECT ANSWERS: \"I have been studying\" is correct, \"I've been studying\" is not.\n"
                                   f"You will create similar tasks and provide correct answers for each blank.\n"
                                   "You output will be only JSON object starting with { and ending with }.\n"
                                   f"No other content should be present in the output.\n"
                                   f"The JSON object must use the schema: {self.jsonschema}",
                    },
                    {
                        "role": "user",
                        "content": "Please create 10 tasks for forms of present perfect, past, or past perfect tenses. ONLY FOR THIS TENSES PLEASE!!!!!"
                    }
                ]
                print("Messages:", messages)
                tasks_text = llm_fetch_tasks(messages)
                # serialize the tasks
                tasks = []
                data = json.loads(tasks_text)
                # check if data is VerbTenseTask object
                if isinstance(data, VerbTenseTask):
                    return [data]
                print("Parsed JSON:", data)
                for task_data in data['tasks']:
                    print("Current task data:", task_data)
                    validated_task = VerbTenseTask(**task_data)
                    tasks.append(validated_task)
                print(self.tasks)
                print(tasks)
                return tasks
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error: {e}")
                retries_left -= 1
        return {"error": "Error after 5 retries"}

    def submit_task(self, answer):
        # Logic to check the answers
        pass

    def validate_answer(self, user_answer, correct_answer):
        return [ans.strip() == cor_ans.strip() for ans, cor_ans in zip(user_answer, correct_answer)]

    @property
    def jsonschema(self):
        return json.dumps(VerbTenseTask.schema(), indent=2)
