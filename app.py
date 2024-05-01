from flask import Flask, request, jsonify, render_template
from task_factory import TaskFactory
import markdown
from bs4 import BeautifulSoup

app = Flask(__name__)

tasks_store = {}


@app.route('/')
def index():
    print("Loading index page")
    task_handler = TaskFactory.get_task_handler('direct_to_indirect_speech')
    tasks = task_handler.fetch_tasks()
    print(f"Current tasks: {tasks}")

    # Pass the tasks to the template with proper formatting
    return render_template('index.html', tasks=[{'id': task.id, 'task': task.task, 'correct_answer': task.correct_answer} for task in tasks])


@app.route('/check/<task_type>', methods=['POST'])
def submit_task(task_type):
    task_handler = TaskFactory.get_task_handler(task_type)
    original_task = request.json.get('task')
    user_answer = request.json.get('answer')
    task_id = request.json.get('id')
    print(f"Checking task {original_task} with answer {user_answer} and id {task_id}")
    # if answer is empty return error
    if not user_answer:
        return jsonify({"error": "Answer is empty"}), 400
    result = task_handler.check_task(original_task, user_answer, task_id)
    return jsonify(result)


@app.route('/explain/<path:task_type>/<path:question_text>')
def explain(question_text, task_type):
    # print(f"Explaining task {question_text}")
    task_handler = TaskFactory.get_task_handler(task_type)
    explanation = task_handler.explain_task(question_text)
    # Your logic here to fetch or generate an explanation
    print(f"Explanation for task {question_text}: {explanation}")
    # apply markdown formatting
    explanation_html = markdown.markdown(explanation, extensions=['codehilite', 'fenced_code'])
    print(f"Explanation HTML: {explanation_html}")
    # Use BeautifulSoup to add Tailwind classes
    soup = BeautifulSoup(explanation_html, 'html.parser')

    # Add Tailwind classes to unordered lists
    for ul in soup.find_all('ul'):
        ul['class'] = ul.get('class', []) + ['list-disc', 'pl-5']

    # Add Tailwind classes to ordered lists
    for ol in soup.find_all('ol'):
        ol['class'] = ol.get('class', []) + ['list-decimal', 'pl-5']
    return jsonify({"explanation": str(soup)})


@app.route('/fetch_task/<task_type>', methods=['GET'])
def fetch_task(task_type):
    try:
        task_handler = TaskFactory.get_task_handler(task_type)
        task = task_handler.fetch_task()
        return jsonify(task), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(debug=True)



