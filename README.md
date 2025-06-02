# 🧾 Automation of VTU Results

A Python automation project that extracts and analyzes student results from the VTU results website. It solves CAPTCHAs, fetches result data, calculates percentages, and displays/save the output.

---

## 🚀 Features

- 🔍 **Automated Result Fetching** from VTU results portal
- 🔐 **CAPTCHA Solver** using image preprocessing
- 📊 **Percentage Calculator** from raw marks
- 🖼️ **Snapshot Generator** of result section
- 💾 **Save Images and Data** locally for reference

---

## 🛠️ Tech Stack

- **Python 3.10+**
- `requests`, `beautifulsoup4` – Web scraping
- `Pillow`, `OpenCV` – Image processing
- `pytesseract` – OCR for CAPTCHA solving
- `matplotlib`, `numpy` – Data handling & plots (optional)
- `Flask` – Web interface (if used)

---

## 📂 Folder Structure

vtu_result_automation/
│
├── app.py # Main script
├── CalculatePercentage.py # Calculates percentage from marks
├── requirements.txt # Dependencies
├── temp/ # Stores CAPTCHA, snapshot images
│ ├── cap.png
│ ├── output_image.png
│ └── snapshot.png
└── pycache/ # Python cache (optional to track)


---

## 📸 Sample Output

- ✅ CAPTCHA Solved Automatically
- 📋 Result Snapshot Saved
- 📈 Percentage Calculated: **e.g., 72.85%**

---

## 📦 Installation

## 1. Clone the repository:
   ```bash
   git clone https://github.com/ananya0707/Automation-of-VTU-results.git
   cd Automation-of-VTU-results
   ```

## 2.Install dependencies:

 ```bash
pip install -r requirements.txt
```
## 3.Run the application:

```bash

python app.py
```

## 🧠 How It Works
Takes USN input.

Fetches result page from VTU server.

Solves CAPTCHA using OCR (easyocr).

Extracts marks and calculates percentage.

Saves result snapshot to temp/.

## ❗ Note
Accuracy of CAPTCHA solving may vary based on image clarity.

Designed for educational and personal use only.

## 🙌 Author
Made with ❤️ by Ananya M Rao

---
