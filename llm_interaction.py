from groq import Groq
from typing import List, Dict, Any
from models import DirectToIndirectSpeechTask
import os
import json
from pydantic import ValidationError

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '') # Get the GROQ_API_KEY from the environment

groq = Groq(
    api_key=GROQ_API_KEY,
)

def llm_explain_task(messages: List[Dict[str, Any]]):
    chat_completion = groq.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
        temperature=1.2,
        # Streaming is not supported in JSON mode
        stream=False,
        # Enable JSON mode by setting the response format
        # response_format={"type": "json_object"},
    )
    return chat_completion.choices[0].message.content


def llm_check_answer(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    retries_left = 5
    while retries_left > 0:
        try:
            chat_completion = groq.chat.completions.create(
                messages=messages,
                model="llama3-70b-8192",
                temperature=1.2,
                stream=False,
            )
            print("Check answer completion:", chat_completion)
            result = json.loads(chat_completion.choices[0].message.content)
            return result
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error: {e}")
            retries_left -= 1
    return {"error": "Error after 5 retries"}


def llm_get_tasks(messages: List[Dict[str, Any]]) -> List[DirectToIndirectSpeechTask]:
    retries_left = 5
    while retries_left > 0:
        try:
            print("API Key:", GROQ_API_KEY)
            print("Messages:", messages)
            chat_completion = groq.chat.completions.create(
                messages=messages,
                model="llama3-70b-8192",
                temperature=1.2,
                stream=False,
            )
            print("Chat completion:", chat_completion)
            tasks_json = json.loads(chat_completion.choices[0].message.content)
            print("Parsed JSON:", tasks_json)

            tasks = []
            for task_data in tasks_json['tasks']:
                print("Current task data:", task_data)
                validated_task = DirectToIndirectSpeechTask(**task_data)
                tasks.append(validated_task)
            return tasks
        except (json.JSONDecodeError, ValidationError, Exception) as e:
            print(f"Error: {e}")
            retries_left -= 1
    return {"error": "Error after 5 retries"}

def llm_fetch_tasks(messages: List[Dict[str, Any]]):
    messages = messages
    print("API Key:", GROQ_API_KEY)
    print("Messages:", messages)
    chat_completion = groq.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
        temperature=1.2,
        stream=False,
    )
    print("Chat completion:", chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


