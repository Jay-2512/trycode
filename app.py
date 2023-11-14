from flask import Flask, render_template, request, send_file
import subprocess
import zipfile
import os
import time
import uuid
import shutil
import pandas as pd

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
    global result_path

    code = request.files['code']
    testcase = request.files['testcase']
    code_filename = str(uuid.uuid4()) + '.cpp'
    compiled_program_filename = str(uuid.uuid4())
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
    result_text = ''

    result_data = {
        'Input File': [],
        'Execution Time': [],
        'Status': [],
        'Expected Output': [],
        'Program Output': []
    }

    for input_file, output_file in zip(input_files, output_files):
        input_path = os.path.join(testcase_folder, input_file)
        output_path = os.path.join(testcase_folder, output_file)

        with open(input_path, 'r') as f:
            input_data = f.readlines()

        with open(output_path, 'r') as f:
            expected_output = f.read().strip()

        compile_command = f'g++ -o {compiled_program_filename} {code_filename}'
        compile_output = subprocess.getoutput(f'time -f "Compilation Time: %E" {compile_command}')

        start_time = time.time()
        process = subprocess.run([f'./{compiled_program_filename}'], input='\n'.join(input_data), capture_output=True, text=True)
        program_output = process.stdout.strip()

        end_time = time.time()
        execution_time = end_time - start_time

        if program_output == expected_output:
            status = 'Passed'
        else:
            status = 'Failed'

        execution_times[input_file] = {
            'execution_time': execution_time,
            'status': status,
            'expected_output': expected_output,
            'program_output': program_output
        }

        result_text += f'Input File: {input_file}\n'
        result_text += f'Execution Time: {execution_time} seconds\n'
        result_text += f'Status: {status}\n'
        result_text += f'Expected Output:\n{expected_output}\n'
        result_text += f'Program Output:\n{program_output}\n\n'

        result_data['Input File'].append(input_file)
        result_data['Execution Time'].append(execution_time)
        result_data['Status'].append(status)
        result_data['Expected Output'].append(expected_output)
        result_data['Program Output'].append(program_output)

    os.remove(code_filename)
    os.remove(testcase_filename)
    os.remove(compiled_program_filename)


    result_filename = str(uuid.uuid4()) + '.xlsx'
    result_path = os.path.join(testcase_folder, result_filename)
    pd.DataFrame(result_data).to_excel(result_path, index=False)

    return render_template('result.html', execution_times=execution_times, result_filename=result_filename)

@app.route('/download/<result_filename>')
def download_result(result_filename):
    return send_file(result_path, as_attachment=True)

@app.route('/compile-code')
def code_compiler():
    return render_template('compiler.html')

@app.route('/compileCode', methods=['POST'])
def compileCode():
    code = request.form['code']
    code_filename = str(uuid.uuid4()) + '.cpp'
    compiled_program_filename = str(uuid.uuid4())
    
    with open(code_filename, 'w') as file:
        file.write(code)

    compile_command = f'g++ -o {compiled_program_filename} {code_filename}'
    compile_output = subprocess.getoutput(f'time -f "Compilation Time: %E" {compile_command}')

    os.remove(code_filename)
    os.remove(compiled_program_filename)

    return compile_output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1818)
