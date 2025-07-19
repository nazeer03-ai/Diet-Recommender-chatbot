
import streamlit as st
import base64
import re

# Set background image
def set_background_local(image_file):
    with open(image_file, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background_local("delicious-healthy-lettuce-salad.jpg")

st.title("💬 Diet Recommendation ChatBot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Save and display chat messages
def display_chat():
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["message"])

display_chat()

# Define chatbot response logic
def chatbot_response(message):
    response = ""

    # Name
    if "my name is" in message.lower():
        name = message.split("is")[-1].strip().title()
        st.session_state.name = name
        response = f"Hi {name}! 👋 What's your age?"

    # Age
    elif "i'm" in message.lower() or "i am" in message.lower():
        match = re.search(r'\b(?:i\'m|i am)\s+(\d{1,2})', message.lower())
        if match:
            age = int(match.group(1))
            st.session_state.age = age
            response = f"Great! You're {age} years old. What's your weight and height?"

    # Weight & Height
    elif "weight" in message.lower() and "height" in message.lower():
        try:
            weight = float(re.search(r'weight\s*is\s*(\d+)', message.lower()).group(1))
            height = float(re.search(r'height\s*is\s*(\d+)', message.lower()).group(1))
            st.session_state.weight = weight
            st.session_state.height = height
            response = f"Thanks! You're {weight}kg and {height}cm tall. Do you have diabetes?"
        except:
            response = "❗ Please say: 'My weight is 65 and height is 170'."

    # Diabetes
    elif "diabet" in message.lower():
        if "no" in message.lower():
            st.session_state.diabetic = False
            response = "Noted. How many hours do you sleep daily?"
        else:
            st.session_state.diabetic = True
            response = "Got it. How many hours do you sleep daily?"

    # Sleep
    elif "sleep" in message.lower():
        try:
            hours = int(re.search(r'(\d+)', message).group(1))
            st.session_state.sleep = hours
            response = "Thank you! Do you follow a vegetarian or non-vegetarian diet?"
        except:
            response = "❗ Please tell how many hours you sleep, e.g., 'I sleep 7 hours'."

    # Diet Type
    elif "vegetarian" in message.lower() or "non-vegetarian" in message.lower() or "vegan" in message.lower():
        st.session_state.diet = message.title()
        response = "Last question! How many meals do you eat daily?"

    # Meals
    elif "meal" in message.lower():
        try:
            meals = int(re.search(r'(\d+)', message).group(1))
            st.session_state.meals = meals

            bmi = st.session_state.weight / ((st.session_state.height / 100) ** 2)
            bmi = round(bmi, 2)
            st.session_state.bmi = bmi

            # Diet recommendation
            if bmi < 18.5:
                diet_note = "You're underweight. Eat more protein and healthy fats."
            elif bmi < 25:
                diet_note = "You're healthy! 🥗 Keep it up."
            elif bmi < 30:
                diet_note = "You're overweight. Watch your carbs and walk daily."
            else:
                diet_note = "You're obese. Consider a low-carb diet and daily exercise."

            response = f"""### ✅ Summary for {st.session_state.name}  
🎂 Age: {st.session_state.age}  
⚖️ Weight: {st.session_state.weight} kg  
📏 Height: {st.session_state.height} cm  
🧮 BMI: **{bmi}**  
💊 Diabetic: {"Yes" if st.session_state.diabetic else "No"}  
🍽️ Meals/day: {st.session_state.meals}  
🥦 Diet: {st.session_state.diet}  
🛌 Sleep: {st.session_state.sleep} hrs  

📝 **Diet Tip:** {diet_note}  
"""

            # Try to show diet chart image
            try:
                st.image("diet-chart.png", use_column_width=True)
            except:
                st.warning("⚠️ 'diet-chart.png' not found.")
        except:
            response = "❗ Please tell how many meals you eat daily."

    else:
        response = "👋 Hi! You can say: 'My name is Nazeer', 'I'm 24', 'My weight is 70 and height is 170', etc."

    return response

# Chat input box
user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    bot_reply = chatbot_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "message": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply, unsafe_allow_html=True)
