from flask import Flask, render_template, request, jsonify
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SLOT_ORDER = ["morning", "afternoon", "night"]

def classify_time_slot(hour: int) -> str:
    if 5 <= hour < 12: return "morning"
    elif 12 <= hour < 17: return "afternoon"
    else: return "night"

def enforce_slots(itinerary, days, arrival, departure):
    try:
        arr_hour = int(arrival.split(":")[0])
        dep_hour = int(departure.split(":")[0])
        arr_idx = SLOT_ORDER.index(classify_time_slot(arr_hour))
        dep_idx = SLOT_ORDER.index(classify_time_slot(dep_hour))

        for day_data in itinerary:
            day_num = int(day_data.get("day", 1))
            for idx, slot in enumerate(SLOT_ORDER):
                if (day_num == 1 and idx < arr_idx) or (day_num == days and idx > dep_idx):
                    day_data[slot] = "--- (In Transit) ---"
        return itinerary
    except:
        return itinerary

def get_itinerary_data(from_city, to_city, budget, days, arrival, departure):
    days_int = int(days)
    budget_int = int(budget)

    # 1. DYNAMIC BUDGET CHECK (Real-world minimums excluding flights)
    min_check_prompt = f"Estimate the absolute minimum land budget (excluding flights) in INR for a {days_int}-day trip to {to_city} for basic survival. Return ONLY the numeric value."
    
    try:
        min_res = client.chat.completions.create(
            messages=[{"role": "user", "content": min_check_prompt}],
            model="llama-3.3-70b-versatile"
        )
        real_min_str = min_res.choices[0].message.content.strip().replace(',', '')
        real_min = int(''.join(filter(str.isdigit, real_min_str)))
        
        if budget_int < real_min:
            return {"error": "insufficient", "suggested_min": real_min}
    except:
        if budget_int < (1500 * days_int): 
            return {"error": "insufficient", "suggested_min": 1500 * days_int}

    # 2. GENERATE FULL ITINERARY WITH 3 HOTELS
    prompt = f"""
    Create a {days_int}-day travel itinerary for {to_city} from {from_city}.
    Land Budget (excluding flights): ₹{budget_int} INR.
    Return JSON only with this exact structure:
    {{
      "hotels": [
        {{ "name": "Hotel 1", "price": "₹...", "desc": "..." }},
        {{ "name": "Hotel 2", "price": "₹...", "desc": "..." }},
        {{ "name": "Hotel 3", "price": "₹...", "desc": "..." }}
      ],
      "breakdown": {{"Stay": "₹...", "Food": "₹...", "Activities": "₹..."}},
      "itinerary": [
        {{ "day": 1, "morning": "...", "afternoon": "...", "night": "..." }}
      ]
    }}
    Note: All currency MUST be in INR. Ensure exactly 3 hotel options are provided.
    """
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": "You are a travel agent. Output JSON only. All prices in INR."}, 
                  {"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    result["itinerary"] = enforce_slots(result.get("itinerary", []), days_int, arrival, departure)
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form
    result = get_itinerary_data(
        data.get('from_city', 'Mumbai'), data.get('to_city', 'Goa'), 
        data.get('budget', '0'), data.get('days', '1'), 
        data.get('arrival', '10:00'), data.get('departure', '18:00')
    )
    
    if isinstance(result, dict) and result.get("error") == "insufficient":
        return render_template('index.html', error_msg=True, min_val=result['suggested_min'], 
                               city=data['to_city'], days=data['days'], user_budget=data['budget'])

    return render_template('itinerary.html', result=result, city=data['to_city'], 
                           from_city=data['from_city'], budget=data['budget'], days=data['days'])

@app.route('/get_flights', methods=['POST'])
def get_flights():
    try:
        data = request.json
        prompt = f"""
        Provide a round-trip flight price range in INR for one person from {data['from_city']} to {data['to_city']} in {data['month']}.
        Instructions:
        - Use REALISTIC budget carrier rates (e.g., IndiGo, Air India Express).
        - Price must be strictly in INR.
        Return JSON: {{"range": "₹XX,XXX - ₹XX,XXX", "tip": "..."}}
        """
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a travel expert. Use only INR currency."},
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(response.choices[0].message.content))
    except:
        return jsonify({"range": "Rate unavailable", "tip": "Check Google Flights for INR rates."})

if __name__ == '__main__':
    app.run(debug=True)