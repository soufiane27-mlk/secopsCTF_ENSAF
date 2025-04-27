from flask import Flask, request, render_template
import yaml

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        config = request.form.get("config", "")
        try:
            data = yaml.load(config, Loader=yaml.Loader)
            output = str(data)
        except Exception as e:
            output = f"Error parsing YAML: {e}"
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
