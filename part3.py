from crypt import methods
import part1 as mn
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='Templates')

@app.route("/")
def home():
    # webapp homepage containing the request list
    return render_template("home.html")

@app.route("/selector", methods=['POST'])
def answer():
    question = eval(request.form["request"])
    text = request.form["txt"]
    result = mn.OperationManager.manager(registry, question, text)
    if question[0]=="rqc":
        return render_template("quotes.html", data=result[0], title= result[1], val = result[2])
    elif question[0]=="mtd" or question[0]=="sm":
        return render_template("metadata.html", collection=result[0], title=result[1])
    else:
        return render_template("answers.html", data=result[0], title=result[1], val = result[2])

if __name__ == '__main__':
    registry = mn.read()
    app.run()