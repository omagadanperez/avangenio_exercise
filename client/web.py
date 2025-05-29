from flask import Flask, request, render_template, flash, redirect, url_for, get_flashed_messages, send_from_directory
import asyncio
import client
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num_strings = int(request.form['num_strings'])

            output_path = "data/chains.txt"
            response_path = "data/responses.txt"

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            os.makedirs(os.path.dirname(response_path), exist_ok=True)

            asyncio.run(client.main_from_web(num_strings, output_path, response_path))

            flash(f"Success:Processing completed for {num_strings} strings.", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")

        # REDIRECT after POST
        return redirect(url_for('index'))

    # Separate GET route for clean render after redirect
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/download/<filename>')
def download_file(filename):
    directory = os.path.join(app.root_path, 'data')
    if filename not in ('chains.txt', 'responses.txt'):
        return "Invalid file", 404
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
