# 🌍 TripMate | AI-Powered Travel Planner

**TripMate** is an intelligent travel itinerary generator that creates personalized journeys based on your budget, timing, and destination. Developed using **Vibe Coding**—a high-level orchestration of Gemini and Claude—this project bridges complex Flask backend logic with a high-end "glassmorphism" UI.

---

## ✨ Features

* **AI Itinerary Generation:** Uses **Llama 3.3 70B** (via Groq) to build detailed daily schedules.
* **Dynamic Budget Validation:** Includes a "Budget Guard" that checks if your funds are realistic for the chosen destination.
* **Interactive 3D UI:** Features a custom-coded, rotating SVG globe and floating state cards.
* **Flight Price Estimator:** Provides round-trip flight price ranges in INR based on your selected travel month.
* **Transit Logic:** Automatically adjusts schedules based on your specific arrival and departure times.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **LLM Engine:** Groq API (Llama 3)
* **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript
* **Development Method:** Vibe Coding (AI-pair programming with Gemini & Claude)

---

## 🚀 Setup and Installation

To run this project locally, you need the following:

### 1. Prerequisites

* **Python 3.10+**: Ensure Python is installed on your system.
* **Groq API Key**: Obtain a key from the Groq Cloud Console.

### 2. Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/TripMate-AI-Planner.git
cd TripMate-AI-Planner
```

#### 2. Install Dependencies

Ensure your `requirements.txt` file contains:

* flask
* groq
* python-dotenv

Then run:

```bash
pip install -r requirements.txt
```

#### 3. Set Up Environment Variables

Create a file named `.env` in the root directory and add your key:

```text
GROQ_API_KEY=your_actual_key_here
```

#### 4. Run the Application

```bash
python app.py
```

#### 5. View the Project

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```text
TripMate-AI-Planner/
├── app.py              # Flask backend & AI logic
├── templates/          # Frontend HTML files
│   ├── index.html      # Landing page & UI
│   └── itinerary.html  # Results page
├── .env                # API Keys (Local only)
├── .gitignore          # Files to exclude from Git
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 👨‍💻 Author

**Jeevika Hunnurkar**
*Computer Engineering Student at Sinhgad Institute*

---

## 🧠 Development Note

This project was built using **Vibe Coding**, leveraging iterative prompting, system design guidance, and debugging support through AI tools like Gemini and Claude. It demonstrates an AI-augmented development workflow focused on rapid prototyping and high-quality output.
