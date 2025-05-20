# Constelations_pygame

Pygame game packaged for the web with Pygbag.

## Description

Constelations is a small Pygame demo that draws moving dots and connects those within a certain distance, with an interactive control panel to adjust speed, number of points, and connection distance. With Pygbag, it can run in modern browsers as a WebAssembly application.

**Important Note**  
The original idea for this animation is not mine. I do not claim it as my own nor am I the rightful owner of its intellectual property. It is an attempt to replicate an animation I saw while browsing the internet. I have been unable to locate the original animation again and therefore cannot credit the creator.

## Requirements

- **Python** working on ≥ 3.8.x and < 3.12.x - [3.8.x, 3.12)
- **pygame-ce** (community edition of Pygame)
- **pygbag** ≥ 0.8.1 (recommended 0.9.2)

## Installation

1. Clone or download this repository.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```
3. Install the dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running Locally

1. Package the current folder with Pygbag:
   ```bash
   python -m pygbag .
   ```
2. Open in your browser:
   ```
   http://localhost:8000
   ```
3. For debug mode (interactive REPL):
   ```
   http://localhost:8000?-i
   ```

## File Structure

```
Constelations/
├── main.py           # Game source code (async)
├── assets/           # Images, sounds, and fonts
├── requirements.txt  # Python dependencies
└── README.md         # This document
```

## Customization

- Adjust `main.py` if you add new assets or dependencies.
- You can create a ZIP ready for itch.io with:
  ```bash
  python -m pygbag . --archive
  ```

## License

This project is licensed under the MIT License.
