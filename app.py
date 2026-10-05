import streamlit as st
import pandas as pd

# Project title
st.title("Student Attendance Analyzer")

# Load attendance dataset
df = pd.read_csv("data/attendance.csv")

# Display original data
st.dataframe(df)

# -------------------------------
# Overall Project Statistics
# -------------------------------

total_students = df["Student_ID"].nunique()

total_subjects = df["Subject"].nunique()

average_attendance = (
    df["Classes_Attended"].sum()
    / df["Classes_Held"].sum()
) * 100

average_attendance = round(average_attendance, 2)

# Student-wise total attendance
student_totals = (
    df.groupby(["Student_ID", "Student_Name"])[
        ["Classes_Held", "Classes_Attended"]
    ]
    .sum()
)

student_totals["Attendance_Percentage"] = (
    student_totals["Classes_Attended"]
    / student_totals["Classes_Held"]
) * 100

student_totals["Attendance_Percentage"] = (
    student_totals["Attendance_Percentage"].round(2)
)

# Count students below 75%
low_attendance_students = (
    student_totals["Attendance_Percentage"] < 75
).sum()

# -------------------------------
# Dashboard Statistics
# -------------------------------

st.subheader("📊 Overall Statistics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("Total Subjects", total_subjects)
col3.metric("Average Attendance", f"{average_attendance}%")
col4.metric("Low Attendance Students", low_attendance_students)

# -------------------------------
# Select a Student
# -------------------------------

st.subheader("👤 Student Details")
student_names = df["Student_Name"].unique()

selected_student = st.selectbox(
    "Select Student",
    student_names
)

student_data = df[
    df["Student_Name"] == selected_student
]

# -------------------------------
# Selected Student Attendance
# -------------------------------

classes_held = student_data["Classes_Held"].sum()

classes_attended = student_data["Classes_Attended"].sum()

student_percentage = (
    classes_attended / classes_held
) * 100

student_percentage = round(student_percentage, 2)

st.write(
    f"{selected_student}'s Overall Attendance: "
    f"{classes_attended} out of {classes_held} classes "
    f"({student_percentage}%)"
)

st.progress(student_percentage / 100)

if student_percentage < 75:
    st.warning("Low Attendance")
else:
    st.success("Good Attendance")

# -------------------------------
# Subject-wise Attendance
# -------------------------------

st.subheader("📚 Subject Analysis")
subject_data = student_data.copy()

subject_data["Attendance_Percentage"] = (
    subject_data["Classes_Attended"]
    / subject_data["Classes_Held"]
) * 100

subject_data["Attendance_Percentage"] = (
    subject_data["Attendance_Percentage"].round(2)
)

st.subheader("Subject-wise Attendance")

display_data = subject_data[
    [
        "Subject",
        "Classes_Held",
        "Classes_Attended",
        "Attendance_Percentage"
    ]
].copy()

display_data["Attendance_Percentage"] = (
    display_data["Attendance_Percentage"].map(
        lambda x: f"{x:.2f}%"
    )
)

st.dataframe(display_data)
# -------------------------------
# Subject-wise Chart
# -------------------------------

st.subheader("Subject-wise Attendance Chart")

st.bar_chart(
    subject_data.set_index("Subject")[
        "Attendance_Percentage"
    ]
)

# -------------------------------
# Lowest and Highest Subject
# -------------------------------

lowest_subject = subject_data.loc[
    subject_data["Attendance_Percentage"].idxmin(),
    "Subject"
]

highest_subject = subject_data.loc[
    subject_data["Attendance_Percentage"].idxmax(),
    "Subject"
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Overall Attendance",
    f"{student_percentage}%"
)

col2.metric(
    "Lowest Subject",
    lowest_subject
)

col3.metric(
    "Highest Subject",
    highest_subject
)

# -------------------------------
# Attendance Requirement
# -------------------------------

attendance_requirement = 75

st.info(
    f"Minimum Attendance Requirement: {attendance_requirement}%"
)

# -------------------------------
# Download Student Attendance
# -------------------------------

csv_data = subject_data[
    [
        "Subject",
        "Classes_Held",
        "Classes_Attended",
        "Attendance_Percentage"
    ]
].to_csv(index=False)

st.download_button(
    "Download Student Attendance",
    csv_data,
    file_name=f"{selected_student}_attendance.csv",
    mime="text/csv"
)

# -------------------------------
# Student-wise Attendance Comparison
# -------------------------------

st.subheader("📈 Student Performance Comparison")

student_comparison = student_totals.reset_index()

student_comparison["Status"] = student_comparison[
    "Attendance_Percentage"
].apply(
    lambda x: "Low Attendance" if x < 75 else "Good Attendance"
)

st.dataframe(
    student_comparison[
        [
            "Student_ID",
            "Student_Name",
            "Classes_Held",
            "Classes_Attended",
            "Attendance_Percentage",
            "Status"
        ]
    ].style.format(
        {"Attendance_Percentage": "{:.2f}%"}
    )
) 

st.bar_chart(
    student_comparison.set_index("Student_Name")[
        "Attendance_Percentage"
    ]
)# -------------------------------
# Low Attendance Students
# -------------------------------
st.subheader("⚠️ Students Below 75% Attendance")

low_students = student_comparison[
    student_comparison["Attendance_Percentage"] < 75
]

if len(low_students) > 0:
    st.dataframe(
    low_students[
        [
            "Student_ID",
            "Student_Name",
            "Classes_Held",
            "Classes_Attended",
            "Attendance_Percentage"
        ]
    ]
)
else:
    st.success("No students are below 75% attendance.")