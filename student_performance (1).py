# -*- coding: utf-8 -*-
"""Student performance.ipynb


Student performance visualization
"""

"""Installing the libraries necessary for the code"""

import os
os.system('python -m pip install jupyter-dash')
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

"""Loading the dataset"""

df = pd.read_excel('student1.xlsx')

"""Exploratory data analysis"""

df.info()

df.describe()

df.head()

"""Visualization of the dataset"""

subjects = ["Maths", "English", "ss", "HE", "Bstudies", "BST", "Computer", "Agric", "IRS"]

# Define student_data before using it
student_data = df[df["Name"] == "Bashir Abdulmumin"]  # Assuming you want data for 'Bashir Abdulmumin'

scores = [student_data[subject].values[0] for subject in subjects]  # Now student_data is defined

fig = px.bar(
    x=subjects,
    y=scores,
    title="Test Chart",
    labels={"x": "Subjects", "y": "Scores"},
    color=scores,
    color_continuous_scale="Viridis",
)

fig.show()

"""Checking for highest score, punctuality, attendance and average"""

student_data = df[df["Name"] == "Bashir Abdulmumin"]
subjects = ["Maths", "English", "ss", "HE", "Bstudies", "BST", "Computer", "Agric", "IRS"]
scores = [student_data[subject].values[0] for subject in subjects]
highest_scores = {subject: df[subject].max() for subject in subjects}
average_score = sum(scores) / len(scores)
print(highest_scores)
print(average_score)

student_data["Punctuality"].values[0]

student_data["Attendance(%)"].values[0]

"""Loading the plotly app"""

app = dash.Dash(__name__)

"""Setting the layout"""

app.layout = html.Div([
    html.H1("Student Performance Dashboard",style={"textAlign":"center"}),
    html.Label("Select Student:"),
    dcc.Dropdown(
        id="student-dropdown",
        options=[{"label":name,  "value":name} for name in df["Name"]],
        value="Bashir Abdulmumin",
        style={"width":"50%"}
),

     dcc.Graph(id="subject-score-graph"),
     html.H3("Student Performance Table"),
     html.Div(id="data-table")
])

"""Calling the app"""

@app.callback(
    [Output("subject-score-graph", "figure"),
     Output("data-table", "children")],
    [Input("student-dropdown", "value")]
)
def update_dashboard(selected_student):
    # Debugging: Print selected student
    print(f"Selected student: {selected_student}")
# Filter data for selected student
    student_data = df[df["Name"] == selected_student]

    if student_data.empty:
        print("No data found for the selected student.")
        return {}, html.Div("No data available")

    # Subjects and scores
    subjects = ["Maths", "English", "ss", "HE", "Bstudies", "BST", "Computer", "Agric", "IRS"]
    scores = [student_data[subject].values[0] for subject in subjects]
    highest_scores = {subject: df[subject].max() for subject in subjects}
    average_score = sum(scores) / len(scores)
 # Bar chart
    fig = px.bar(
        x=subjects,
        y=scores,
        title=f"{selected_student}'s Subject Scores",
        labels={"x": "Subjects", "y": "Scores"},
        color=scores,
        color_continuous_scale="Viridis"
    )

    # Table
    table = html.Table([
        html.Thead(html.Tr([html.Th("Subject"), html.Th("Student Score"), html.Th("Highest Score")])),
        html.Tbody([
            html.Tr([html.Td(subject),
                     html.Td(student_data[subject].values[0]),
                     html.Td(highest_scores[subject])])
            for subject in subjects
        ]),
        html.Tbody([
            html.Tr([html.Td("Average Score"), html.Td(average_score)]),
            html.Tr([html.Td("Punctuality"), html.Td(student_data["Punctuality"].values[0])]),
            html.Tr([html.Td("Attendance"), html.Td(student_data["Attendance(%)"].values[0])])
        ])
    ], style={"width": "50%", "margin": "auto", "border": "1px solid black", "textAlign": "center"})

    return fig, table

if __name__ == "__main__":
     app.run_server(debug=True)

import os
os.system('python -m pip install streamlit') # Installing the streamlit library

import streamlit as st # Now you can import and use streamlit

# Create a Streamlit component to display the Dash app
st.components.v1.iframe("http://localhost:8051", height=800)  # Adjust height as needed




