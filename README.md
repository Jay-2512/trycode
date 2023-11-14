# tryCode - Test your code with ease

## Features

- **Code Compilation:** Upload C++ code, and the application will handle the compilation using g++.
- **Test Case Execution:** Execute compiled code against provided test cases and view detailed results.
- **Result Download:** Download a comprehensive result file containing execution times, expected output, and program output.

## Getting Started

### Prerequisites

- Python (version 3.8.1)
    ```bash
    sudo  apt install python3
    sudo  apt install python3.8-venv
- g++ compiler for C++ (version 12.3)

### Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd trycode
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Activate virtual enviroment:
    ```bash
   python -m venv venv
  
   source venv/bin/activate  # For Unix/Linux
   
   venv\Scripts\activate  # For Windows
### Usage

1. Run the Flask application:

    ```bash
    flask run
    ```

2. Access the application:

    Visit [http://localhost:6776/](http://localhost:6776/) in your web browser.

## How to Use

### Code Compilation

1. Navigate to the "Compile Code" or "Upload" section.
2. Provide your C++ code or upload a file.
3. Click the "Compile" or "Submit" button.

### Test Case Execution

1. Navigate to the "Compile" or "Type Code" section.
2. Upload your C++ code and test case files.
3. Click the "Compile" or "Run Tests" button.

### View Results

- Detailed results, including execution times and output, will be displayed on the web page.
- Download a comprehensive result file for further analysis.

## Security Considerations

- Validate and sanitize user inputs to prevent security vulnerabilities.
- Use session-specific or request-specific variables instead of global variables.

## File Structure

- **app.py:** Main Flask application file.
- **templates/:** HTML templates for different views.
- **static/:** Static files such as CSS or JavaScript.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request. Refer to the [contribution guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the [MIT License](LICENSE).
