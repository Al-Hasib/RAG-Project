from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from src.chat import rag_chain
from src import create_vector
import json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Path to the prompt.json file
PROMPT_FILE = "prompt.json"

# Initialize the prompt.json file if it doesn't exist
def init_prompt_file():
    if not os.path.exists(PROMPT_FILE):
        data = {
            "defaultSystemPrompt": """You are an assistant. You are given a question, a context and a chat history(optional). You need to answer based on the context & chat history.\
     If the context is not relevant to the question, then give me answer from your knowledge.""",
            "currentSystemPrompt": """You are an assistant. You are given a question, a context and a chat history(optional). You need to answer based on the context & chat history.\
     If the context is not relevant to the question, then give me answer from your knowledge.""",
        }
        with open(PROMPT_FILE, 'w') as f:
            json.dump(data, f, indent=4)

# Get prompts from the JSON file
def get_prompts():
    init_prompt_file()
    with open(PROMPT_FILE, 'r') as f:
        return json.load(f)

# Update the current prompts
def update_prompts(system_prompt=None):
    prompts = get_prompts()
    if system_prompt is not None:
        prompts["currentSystemPrompt"] = system_prompt
    with open(PROMPT_FILE, 'w') as f:
        json.dump(prompts, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload_file", methods=['GET', "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename=="":
            return "No selected file"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        message = create_vector.create_knowledgebase(file_path)
        # return f"File uploaded successfully: {file.filename}"
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("upload.html", files = files)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    message = request.form['msg']
    result = rag_chain.invoke({"chat_history":[], "question":message})
    return result

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    message = create_vector.delete_data_from_knowledgebase(filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for("upload_file"))


@app.route('/reset_to_default')
def reset_to_default():
    prompts = get_prompts()
    # Reset the current system prompt to match the default
    prompts["currentSystemPrompt"] = prompts["defaultSystemPrompt"]
    with open(PROMPT_FILE, 'w') as f:
        json.dump(prompts, f, indent=4)
    return redirect(url_for('index_prompt', message="System prompt has been reset to default."))

# Update the index_prompt route to handle the message parameter
@app.route('/maintain_prompt')
def index_prompt():
    prompts = get_prompts()
    message = request.args.get('message')
    return render_template('index_prompt.html', prompts=prompts, message=message)

@app.route('/update_system_prompt', methods=['POST'])
def update_system_prompt():
    system_prompt = request.form.get('system_prompt', '')
    update_prompts(system_prompt=system_prompt)
    return redirect(url_for('index_prompt'))


@app.route('/api/prompts', methods=['GET'])
def api_get_prompts():
    return jsonify(get_prompts())

@app.route('/api/prompts', methods=['POST'])
def api_update_prompts():
    data = request.json
    system_prompt = data.get('systemPrompt')
    update_prompts(system_prompt)
    return jsonify({"success": True})

if __name__ == "__main__":
    init_prompt_file()
    app.run(debug=False, port=5000)