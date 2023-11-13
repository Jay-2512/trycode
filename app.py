from flask import Flask, render_template, request
import subprocess
import zipfile
import os
import time
import uuid
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/typeCode')
def typeCode():
    return render_template('typeCode.html')

@app.route('/upload')
def upload_files():
    return render_template('upload.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.files['code']
    testcase = request.files['testcase']
    code_filename = str(uuid.uuid4()) + '.cpp'
    testcase_filename = str(uuid.uuid4()) + '.zip'
    code.save(code_filename)
    testcase.save(testcase_filename)

    testcase_folder = str(uuid.uuid4())
    os.mkdir(testcase_folder)

    with zipfile.ZipFile(testcase_filename, 'r') as zip_ref:
        zip_ref.extractall(testcase_folder)

    input_files = sorted([f for f in os.listdir(testcase_folder) if f.startswith('input')])
    output_files = sorted([f for f in os.listdir(testcase_folder) if f.startswith('output')])

    execution_times = {}

    for input_file, output_file in zip(input_files, output_files):
        input_path = os.path.join(testcase_folder, input_file)
        output_path = os.path.join(testcase_folder, output_file)

        with open(input_path, 'r') as f:
            input_data = f.readlines()  

        with open(output_path, 'r') as f:
            expected_output = f.read().strip()

        compile_command = f'g++ -o program {code_filename}'
        compile_output = subprocess.getoutput(f'time -f "Compilation Time: %E" {compile_command}')

        start_time = time.time()
        process = subprocess.run(['./program'], input='\n'.join(input_data), capture_output=True, text=True)
        program_output = process.stdout.strip()

        end_time = time.time()
        execution_time = end_time - start_time

        if program_output == expected_output:
            execution_times[input_file] = {
                'execution_time': execution_time,
                'status': 'Passed'
            }
        else:
            execution_times[input_file] = {
                'execution_time': execution_time,
                'status': 'Failed'
            }

    os.remove(code_filename)
    os.remove(testcase_filename)
    os.remove('program')
    shutil.rmtree(testcase_folder)

    return render_template('result.html', execution_times=execution_times)

@app.route('/compileCode', methods=['POST'])
def compileCode():
    code = request.form['code']
    code_filename = str(uuid.uuid4()) + '.cpp'
    with open(code_filename, 'w') as file:
        file.write(code)

    compile_command = f'g++ -o program {code_filename}'
    compile_output = subprocess.getoutput(f'time -f "Compilation Time: %E" {compile_command}')

    os.remove(code_filename)
    os.remove('program')

    return compile_output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6776)
