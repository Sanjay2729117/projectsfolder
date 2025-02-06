from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app)

# College Data with detailed information
colleges = [
    {
        "name": "PSG College of Arts & Science",
        "address": "Peelamedu, Coimbatore - 641004",
        "contact": "+91-422-4303300",
        "website": "https://www.psgcas.ac.in",
        "admission": "Admissions are based on merit and online applications are available on the college website.",
        "courses": ["B.Sc Computer Science", "B.Com", "BBA", "BA English", "M.Sc IT"]
    },
    {
        "name": "Government Arts College",
        "address": "Dr. Nanjappa Road, Coimbatore - 641018",
        "contact": "+91-422-2215212",
        "website": "https://www.gaccoon.com",
        "admission": "Admissions are done through Tamil Nadu Government online counseling.",
        "courses": ["B.Sc Mathematics", "B.Com", "BA History", "M.Sc Physics", "MA Economics"]
    },
    {
        "name": "Sri Krishna Arts and Science College",
        "address": "Kuniamuthur, Coimbatore - 641008",
        "contact": "+91-422-2678400",
        "website": "https://www.skasc.ac.in",
        "admission": "Apply online through the official website. Selection is based on merit.",
        "courses": ["B.Sc Computer Science", "BCA", "B.Com Professional Accounting", "MBA", "M.Sc AI & Data Science"]
    },
    {
        "name": "Hindusthan College of Arts and Science",
        "address": "Avinashi Road, Coimbatore - 641028",
        "contact": "+91-422-2930219",
        "website": "https://www.hindusthan.net/hcas",
        "admission": "Direct admissions based on eligibility criteria. Applications available online and offline.",
        "courses": ["BBA", "B.Sc Visual Communication", "B.Com Banking & Insurance", "M.Sc Biotechnology", "MA Journalism"]
    },
    {
        "name": "Dr. NGP Arts and Science College",
        "address": "Kalapatti, Coimbatore - 641048",
        "contact": "+91-422-2369202",
        "website": "https://www.drngpasc.ac.in",
        "admission": "Online applications open from May. Selection is based on merit.",
        "courses": ["B.Sc Microbiology", "B.Com IT", "BBA Logistics", "M.Sc Biotechnology", "M.Com"]
    }
]

# API to fetch all colleges
@app.route("/colleges", methods=["GET"])
def get_colleges():
    return jsonify({"success": True, "data": colleges})

# Chatbot API for queries
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    message = data.get("message", "").lower()

    if not message:
        return jsonify({"success": False, "error": "Message is required"})

    response_text = "I can help you with information about Arts & Science colleges in Coimbatore."

    for college in colleges:
        if college["name"].lower() in message:
            if "admission" in message:
                response_text = f"{college['name']} Admission Process: {college['admission']}"
            elif "courses" in message:
                response_text = f"{college['name']} offers the following courses: {', '.join(college['courses'])}."
            elif "contact" in message or "address" in message:
                response_text = f"{college['name']} Address: {college['address']}. Contact: {college['contact']}."
            else:
                response_text = f"{college['name']} - Visit: {college['website']} for more details."
            break

    return jsonify({"success": True, "reply": response_text})

if _name_ == "_main_":
    app.run(debug=True, port=5000)