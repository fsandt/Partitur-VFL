# Partitur Generator

## Overview
The Partitur Generator is an application designed to create musical scores for various instruments based on a given description text. This can include descriptions such as company profiles, moods, or any other narrative that can be translated into music.

## Features
- **Text Processing**: Extracts mood and mentioned instruments from the description using a simple keyword based parser.
- **Score Generation**: Creates a short melody for each requested instrument. If
  the `music21` library is available a separate MusicXML file is written for
  each instrument; otherwise the note names are printed to the console.
- **Modular Design**: Organized into distinct modules for easy maintenance and scalability.
- **Web Interface**: Simple Flask application for entering descriptions and viewing the generated score in the browser.

## Project Structure
```
partitur-generator
├── src
│   ├── main.py          # Entry point of the application
│   ├── instruments      # Module for instrument definitions
│   │   └── __init__.py
│   ├── score            # Module for score generation
│   │   └── generator.py
│   └── utils           # Module for utility functions
│       └── text_parser.py
├── requirements.txt     # List of dependencies
├── README.md            # Project documentation
└── .gitignore           # Files to ignore in version control
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/partitur-generator.git
   ```
2. Navigate to the project directory:
   ```
   cd partitur-generator
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
 ulp6o9-codex/create-application-for-automated-score-generation
Run the command line application with a description text. Example:

 main
```
python src/main.py "A happy company with piano and drums"
```
This command prints a summary. When `music21` is installed it also writes one
MusicXML file per instrument (e.g. `piano.musicxml`).
 ulp6o9-codex/create-application-for-automated-score-generation

### Web Interface

To use the browser-based interface start the Flask app:

```
python src/web.py
```

Then open `http://127.0.0.1:5000` in your browser and enter a description.