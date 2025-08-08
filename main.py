from flask import Flask, request, jsonify
import subprocess
import sys

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    """
    Executes Python code received in a POST request.
    The code is run in a separate process for security and isolation.
    """
    code = request.json.get('code', '')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        # We use subprocess to run the code in a new python interpreter instance.
        # This is safer than using exec() because it isolates the execution.
        process = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=15  # Add a timeout to prevent long-running code
        )
        stdout = process.stdout
        stderr = process.stderr

        if stderr:
            # If there's an error during execution, return it as output
            return jsonify({'output': stderr})
        else:
            # Otherwise, return the standard output
            return jsonify({'output': stdout})

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/interpreter', methods=['POST'])
def interpreter():
    """
    Executes Python code received in a POST request.
    This route is an alias for /execute.
    The code is run in a separate process for security and isolation.
    """
    code = request.json.get('code', '')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        # This uses the same safe execution method as the /execute route.
        process = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=15  # A timeout prevents infinitely running scripts.
        )
        stdout = process.stdout
        stderr = process.stderr

        if stderr:
            # Return any errors from the script execution.
            return jsonify({'output': stderr})
        else:
            # Return the script's standard output.
            return jsonify({'output': stdout})

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 408
    except Exception as e:
        # Catch any other server-side exceptions.
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # --- IMPORTANT CHANGE ---
    # Running on '0.0.0.0' makes the server accessible from other devices
    # on your local network, like your phone.
    app.run(host='0.0.0.0', port=5000)
