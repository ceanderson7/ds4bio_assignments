import streamlit as st

st.title("BMI Calculator")

height_unit = st.radio("Height unit", ["meters", "feet and inches"])

if height_unit == "meters":
    height_m = st.number_input("Height (meters)", value=1.75)
else:
    feet = st.number_input("Feet", value=5)
    inches = st.number_input("Inches", value=9)
    total_inches = feet * 12 + inches
    height_m = total_inches * 0.0254

weight_unit = st.radio("Weight unit", ["kilograms", "pounds"])

if weight_unit == "kilograms":
    weight_kg = st.number_input("Weight (kg)", value=70.0)
else:
    weight_lb = st.number_input("Weight (lb)", value=154.0)
    weight_kg = weight_lb * 0.4535

if height_m <= 0 or weight_kg <= 0:
    st.warning("Height and weight must be greater than zero.")
else:
    bmi = weight_kg / (height_m * height_m)
    st.write("Your BMI is", round(bmi, 1))

    if bmi < 18.5:
        st.write("Category: Underweight")
    elif bmi < 25:
        st.write("Category: Healthy weight")
    elif bmi < 30:
        st.write("Category: Overweight")
    else:
        st.write("Category: Obesity")