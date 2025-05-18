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

# Load resources
resources = load_resources("healthCare_test_dataset.csv")
reminders = []

# Streamlit UI
st.title("Accessible Health Resource Finder and Reminder")

# Prompt for voice assistance
voice_assistance = st.radio("Do you want the website to be read to you?", ["No", "Yes"])

# Accessibility settings
st.header("Accessibility Settings")
font_size_choice = st.radio("Choose font size:", ["Normal", "Large"])
color_blind_mode = st.checkbox("Enable color-blind friendly colors")

# Adjust font size
if font_size_choice == "Large":
    st.markdown("""
        <style>
        body, .stText, .stMarkdown {
            font-size: 18px !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Apply color-blind friendly colors if enabled
if color_blind_mode:
    st.markdown("""
    <style>
    .css-18e3th9 {background-color: #fffde7 !important;}
    button {background-color: #0072B2 !important; color: white !important;}
    a, .stMarkdown, .stText {color: #D55E00 !important;}
    </style>
    """, unsafe_allow_html=True)

# Search section
st.header("Search for Resources")
city = st.text_input("Enter city:").strip().lower()
zip_code = st.text_input("Enter ZIP code:").strip()
state = st.text_input("Enter state:").strip().lower()
services = ["general clinic", "vaccination", "health screenings", "primary care", "counseling", "mental health", "therapy", "psychological support", "urgent care", "emergency", "wellness", "nutrition", "immunization", "orthodontist"]
service = st.selectbox("Select service:", [""] + services)

if st.button("Search Resources"):
    filtered = [res for res in resources if (city in res["City"].lower() or not city) and (zip_code == res["ZIP"] or not zip_code) and (state in res["State"].lower() or not state) and (service in res['Services'] or not service)]
    if not filtered:
        st.warning("No resources found.")
        if voice_assistance == "Yes":
            speak_text("No resources found.")
    else:
        for i, res in enumerate(filtered, start=1):
            accessible = "Yes" if res["WheelchairAccessible"] else "No"
            info = f"**{i}. {res['Name']}**\n- Address: {res['Address']}\n- City: {res['City']}, State: {res['State']}, ZIP: {res['ZIP']}\n- Phone: {res['Phone']}\n- Wheelchair Accessible: {accessible}\n- Services: {', '.join(res['Services'])}"
            st.markdown(info)
            if voice_assistance == "Yes":
                speak_text(f"Resource {i}: {res['Name']}, located at {res['Address']}, {res['City']}, {res['State']}.")

# Reminder section
st.header("Add Health Appointment Reminder")
date_time = st.text_input("Date and Time (YYYY-MM-DD HH:MM):").strip()
description = st.text_input("Reminder description:").strip()
location = st.text_input("Location:").strip()
phone = st.text_input("Phone number:").strip()

if st.button("Add Reminder"):
    reminders.append({"date_time": date_time, "description": description, "location": location, "phone": phone})
    st.success("Reminder added!")
    if voice_assistance == "Yes":
        speak_text("Reminder added!")

# List reminders
st.header("Your Health Appointment Reminders")
if reminders:
    for i, rem in enumerate(reminders, 1):
        st.markdown(f"**{i}. {rem['date_time']} - {rem['description']} at {rem['location']} (Phone: {rem['phone']})**")
        if voice_assistance == "Yes":
            speak_text(f"Reminder {i}: {rem['description']} at {rem['location']} on {rem['date_time']}. ")
else:
    st.warning("No reminders set.")
    if voice_assistance == "Yes":
        speak_text("No reminders set.")
