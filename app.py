from flask import Flask, render_template
from utils import system_info as sys

app = Flask(__name__)

@app.route('/')
def index():
    uname, boot_time = sys.get_system_info()
    context = {
        "uname": uname,
        "boot_time": boot_time,
        "cpu_info": sys.get_cpu_info(),
        "memory": sys.get_memory_info(),
        "battery": sys.get_battery_info(),
        "processes": sys.get_process_list()
    }
    return render_template('index.html', **context)

@app.route('/process/<int:pid>')
def process_detail(pid):
    try:
        info = sys.get_process_detail(pid)
        return render_template('process_detail.html', pid=pid, info=info)
    except Exception:
        return f"Processo com PID {pid} não encontrado ou não acessível.", 404

if __name__ == '__main__':
    app.run(debug=True)
