# api_looter

## Overview
api_looter is a web application that provides users with a curated list of free APIs. Users can search through the available APIs, select one, and fill out a form to make API calls and view the results.

## Features
- List of free APIs with search functionality.
- Detailed view of each API with a form for making calls.
- User-friendly interface with a clean layout.

## Project Structure
```
api_looter
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── models.py
│   ├── forms.py
│   ├── templates
│   │   ├── index.html
│   │   ├── api_detail.html
│   │   └── layout.html
│   └── static
│       └── style.css
├── requirements.txt
├── run.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/api_looter.git
   ```
2. Navigate to the project directory:
   ```
   cd api_looter
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python run.py
   ```
2. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.