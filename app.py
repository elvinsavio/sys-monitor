from flask import Flask, render_template

from sys_calls.proc import SystemStats, get_system_stats

app = Flask(__name__)


@app.get("/")
def index():
    system_info: SystemStats = get_system_stats()

    return render_template("index.html", system_info=system_info)
