from flask import Flask, render_template, request
from summarize import summarize

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        output = summarize()
        return render_template("index.html", summary=output["result"])
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
