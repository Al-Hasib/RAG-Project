from flask import Flask, render_template, request, redirect, url_for
import os
from src.chat import rag_chain
from src import create_vector

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

if __name__ == "__main__":
    app.run(debug=True, port=5000)