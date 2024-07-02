import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_script():
    # 运行脚本
    result = subprocess.run(['python3', '/content/leto.py'], capture_output=True, text=True)
    
    # 返回结果
    return {
        'stdout': result.stdout,
        'stderr': result.stderr,
        'returncode': result.returncode
    }
if __name__ == '__main__':
    app.run(debug=True)