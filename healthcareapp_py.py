import streamlit as st
import csv
from gtts import gTTS

# Speak text using gTTS
def speak_text(text):
    try:
        tts = gTTS(text, lang='en')
        tts.save("audio.mp3")
        st.audio("audio.mp3")
    except Exception as e:
        st.error(f"[Speech error: {e}]")

# Load resources from CSV file
def load_resources(filename):
    resources = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['Services'] = [s.strip().lower() for s in row['Services'].split(';')]
                row['WheelchairAccessible'] = row['WheelchairAccessible'].strip().lower() == "yes"
                resources.append(row)
        return resources
    except Exception as e:
        st.error(f"Error loading resources: {e}")
        return []

# Display resources with accessibility filter
def display_resources(resources, city, zip_code, state, service, accessible_required):
    filtered = []
    for res in resources:
        if not (city in res["City"].lower() or not city):
            continue
        if not (zip_code == res["ZIP"] or not zip_code):
            continue
        if not (state in res["State"].lower() or not state):
            continue
        if service and service not in res['Services']:
            continue
        if accessible_required is not None and res["WheelchairAccessible"] != accessible_required:
            continue
        filtered.append(res)

    if not filtered:
        st.warning("No resources found.")
        speak_text("No resources found.")
    else:
        for i, res in enumerate(filtered, start=1):
            accessible = "Yes" if res["WheelchairAccessible"] else "No"
            info = (
                f"**{i}. {res['Name']}**\n"
                f"- Address: {res['Address']}\n"
                f"- City: {res['City']}, State: {res['State']}, ZIP: {res['ZIP']}\n"
                f"- Phone: {res['Phone']}\n"
                f"- Wheelchair Accessible: {accessible}\n"
                f"- Services: {', '.join(res['Services'])}\n"
            )
            st.markdown(info)
            speak_text(f"Resource {i}: {res['Name']}, located at {res['Address']}, {res['City']}, {res['State']}.")

# Load resources
resources = load_resources("healthCare_test_dataset.csv")
reminders = []

# Streamlit UI
st.title("Accessible Health Resource Finder and Reminder")

# Accessibility settings
st.header("Accessibility Settings")
font_size_choice = st.radio("Choose font size:", ["Normal", "Large"])
color_blind_mode = st.checkbox("Enable color-blind friendly colors")

if font_size_choice == "Large":
    st.markdown("""
        <style>
        body, .stText, .stMarkdown {
            font-size: 18px !important;
        }
        </style>
        """, unsafe_allow_html=True)

if color_blind_mode:
    st.markdown("""
        <style>
        .css-18e3th9 { background-color: #fffde7 !important; }
        button { background-color: #0072B2 !important; color: white !important; }
        a, .stMarkdown, .stText { color: #D55E00 !important; }
        </style>
    """, unsafe_allow_html=True)

# Service dropdown list
services = [
    "general clinic", "vaccination", "health screenings", "primary care",
    "counseling", "mental health", "therapy", "psychological support",
    "urgent care", "emergency", "wellness", "nutrition", "immunization",
    "orthodontist"
]

# Search section
st.header("Search for Resources")
city = st.text_input("Enter city:").strip().lower()
zip_code = st.text_input("Enter ZIP code:").strip()
state = st.text_input("Enter state:").strip().lower()
service = st.selectbox("Select service:", [""] + services)

# New dropdown for accessibility
accessibility_filter = st.selectbox("Require wheelchair accessible resource?", ["No preference", "Yes", "No"])

if st.button("Search Resources"):
    if accessibility_filter == "Yes":
        accessible_required = True
    elif accessibility_filter == "No":
        accessible_required = False
    else:
        accessible_required = None  # No preference

    display_resources(resources, city, zip_code, state, service.lower(), accessible_required)

# Reminder section
st.header("Add Health Appointment Reminder")
date_time = st.text_input("Date and Time (YYYY-MM-DD HH:MM):").strip()
description = st.text_input("Reminder description:").strip()
location = st.text_input("Location:").strip()
phone = st.text_input("Phone number:").strip()

if st.button("Add Reminder"):
    reminders.append({
        "date_time": date_time,
        "description": description,
        "location": location,
        "phone": phone
    })
    st.success("Reminder added!")
    speak_text("Reminder added!")

# List reminders
st.header("Your Health Appointment Reminders")
for i, rem in enumerate(reminders, 1):
    st.markdown(f"**{i}. {rem['date_time']} - {rem['description']} at {rem['location']} (Phone: {rem['phone']})**")
    speak_text(f"Reminder {i}: {rem['description']} at {rem['location']} on {rem['date_time']}.")
