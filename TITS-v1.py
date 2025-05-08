import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set page config for a wider layout
st.set_page_config(page_title="TITS Curriculum", layout="wide")

# Initialize session state for selected courses
if 'selected_courses' not in st.session_state:
    st.session_state.selected_courses = []

# Title and header
st.title("Texas Institute of Technology and Science (TITS)")
st.subheader("Curriculum Explorer - Austin, Texas")
st.write("Conquer the cosmos with unapologetic STEM excellence, rooted in merit, truth, and relentless innovation—no woke nonsense tolerated.")

# Define curriculum with 26 departments, 14 courses each (364 total)
departments = [
    ("Aerospace Engineering", "AE"),
    ("Artificial Intelligence", "AI"),
    ("Psychology for STEM", "PSY"),
    ("Sociology for STEM", "SOC"),
    ("Bioinformatics", "BI"),
    ("Space Law and Policy", "SL"),
    ("Sustainable Energy", "SE"),
    ("Physics and Space Science", "PS"),
    ("Entrepreneurial Engineering", "EE"),
    ("Materials Science", "MS"),
    ("Biotechnology", "BT"),
    ("Computer Science", "CS"),
    ("Civil and Planetary Engineering", "CE"),
    ("Neuroscience and Cybernetics", "NC"),
    ("Mathematics and Theoretical Sciences", "MT"),
    ("Robotics and Automation", "RA"),
    ("Environmental Systems", "ES"),
    ("Astrophysics and Cosmology", "AC"),
    ("Quantum Technologies", "QT"),
    ("Interdisciplinary Futures", "IF"),
    ("Mechanical Engineering", "ME"),
    ("Electrical and Electronic Engineering", "EE"),
    ("Chemical Engineering", "CH"),
    ("Philosophy of Science and Technology", "PT"),
    ("Data Science and Analytics", "DS"),
    ("Nanoengineering", "NE")  # Added to reach 26 departments
]

# Generate curriculum dynamically
curriculum = {}
course_levels = [101, 202, 303, 404, 505, 606, 707, 808, 909, 1010, 1111, 1212, 1313, 1414]
for dept_name, dept_code in departments:
    courses = []
    for i, level in enumerate(course_levels):
        course = {
            "code": f"{dept_code}{level}",
            "name": f"{dept_name} Course {level}",
            "desc": f"Master {dept_name.lower()} with merit-driven rigor at level {level}.",
            "credits": 4 if level > 101 else 3,
            "prereq": "None" if level == 101 else f"{dept_code}{course_levels[i-1]}"
        }
        # Customize specific courses for key departments
        if dept_name == "Aerospace Engineering":
            course["name"] = [
                "Intro to Rocket Design", "Orbital Mechanics", "Mars Colonization Engineering", "Hypersonic Flight",
                "Spacecraft Systems Integration", "Interplanetary Mission Design", "Asteroid Mining Tech",
                "Starship Architecture", "Interstellar Propulsion", "Galactic Navigation", "Space Combat Engineering",
                "Cosmic Mega-Transports", "Anti-Woke Space Logistics", "Universal Expansion Tech"
            ][i]
            course["desc"] = [
                "Master propulsion with raw engineering prowess.", "Navigate space with cold, hard math.",
                "Build habitats with unyielding logic.", "Push speed limits with fearless innovation.",
                "Engineer ships that deliver, no fluff.", "Plan missions with ruthless precision.",
                "Extract resources with relentless grit.", "Design vessels for the bold, not the timid.",
                "Chase FTL with unfiltered science.", "Map the galaxy with iron will.",
                "Defend humanity with ruthless efficiency.", "Move civilizations with no handouts.",
                "Optimize fleets, reject mediocrity.", "Conquer the cosmos with merit-driven mastery."
            ][i]
        elif dept_name == "Psychology for STEM":
            course["name"] = [
                "Intro to Scientific Psychology", "Cognitive Science Basics", "Behavioral Analysis for Engineers",
                "Decision-Making Models", "Team Dynamics in STEM", "Stress and Resilience Tech", "Space Psychology",
                "Anti-Woke Psych Ethics", "Neural Data Analysis", "Galactic Crew Optimization",
                "Cognitive Enhancement Tech", "Cosmic Psych Resilience", "Anti-Woke Behavioral Engineering",
                "Universal Psych Mastery"
            ][i]
            course["desc"] = [
                "Study minds with data, not feelings.", "Decode thought with rigorous science.",
                "Optimize humans with empirical facts.", "Predict choices with unyielding logic.",
                "Build elite crews with merit, no fluff.", "Forge unbreakable minds with science.",
                "Master isolation with relentless focus.", "Reason behavior, reject feelings-first dogma.",
                "Crunch brain data with cold precision.", "Maximize team performance across stars.",
                "Boost minds with no apologies.", "Forge minds for the cosmic frontier.",
                "Engineer behavior with merit-driven science.", "Dominate cognition across galaxies."
            ][i]
        elif dept_name == "Sociology for STEM":
            course["name"] = [
                "Intro to Systems Sociology", "Social Structures for Engineers", "Quantitative Social Analysis",
                "Merit-Based Social Dynamics", "Space Colony Sociology", "Anti-Woke Social Theory",
                "Tech-Driven Social Systems", "Galactic Social Networks", "Social Optimization Models",
                "Cosmic Social Resilience", "Anti-Woke Governance", "Universal Social Engineering",
                "Merit-Driven Social Optimization", "Merit-Based Social Mastery"
            ][i]
            course["desc"] = [
                "Study society with data, not narratives.", "Analyze groups with scientific rigor.",
                "Crunch social data, no woke fluff.", "Optimize societies with hard results.",
                "Build communities with unyielding logic.", "Reject collectivism with fierce reason.",
                "Engineer societies with proven outcomes.", "Link societies across stars with efficiency.",
                "Maximize groups with data-driven science.", "Forge societies for the cosmic frontier.",
                "Rule with strength, no collectivist traps.", "Design societies with no excuses.",
                "Peak social performance with science.", "Dominate social systems across galaxies."
            ][i]
        courses.append(course)
    curriculum[dept_name] = courses

# Create a list of all courses for the multiselect
all_courses = []
for dept, courses in curriculum.items():
    for course in courses:
        all_courses.append(f"{course['code']}: {course['name']} ({dept})")

# Sidebar for navigation
st.sidebar.header("Navigation")
department = st.sidebar.selectbox("Select Department", list(curriculum.keys()))
search_term = st.sidebar.text_input("Search Courses", "")
level_filter = st.sidebar.multiselect("Filter by Course Level", ["100-200", "300-400", "500-600", "700-800", "900-1000", "1100-1200", "1300-1400"], default=["100-200", "300-400", "500-600", "700-800", "900-1000", "1100-1200", "1300-1400"])
sort_by = st.sidebar.selectbox("Sort By", ["Code (Ascending)", "Code (Descending)", "Name (A-Z)", "Name (Z-A)"], index=0)
show_all = st.sidebar.checkbox("Show All Courses in Department", value=False)

# Course picker section
st.header("Course Picker")
selected_course_names = st.multiselect("Choose Your Courses", all_courses, default=[f"{course['code']}: {course['name']} ({dept})" for dept, course in st.session_state.selected_courses])
if selected_course_names:
    # Update session state with selected courses
    st.session_state.selected_courses = []
    for course_name in selected_course_names:
        code = course_name.split(":")[0]
        for dept, courses in curriculum.items():
            for course in courses:
                if course["code"] == code:
                    st.session_state.selected_courses.append((dept, course))
                    break

# Display selected courses
if st.session_state.selected_courses:
    st.subheader("Your Selected Courses")
    selected_data = []
    for dept, course in st.session_state.selected_courses:
        selected_data.append({
            "Department": dept,
            "Code": course["code"],
            "Name": course["name"],
            "Description": course["desc"],
            "Credits": course["credits"],
            "Prerequisites": course["prereq"]
        })
    selected_df = pd.DataFrame(selected_data)
    st.dataframe(selected_df)

    # Download selected courses as CSV
    csv_buffer = BytesIO()
    selected_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label="Download Selected Courses as CSV",
        data=csv_buffer,
        file_name="TITS_Selected_Courses.csv",
        mime="text/csv"
    )

# Filter and sort courses for main display
filtered_courses = []
for dept, courses in curriculum.items():
    for course in courses:
        try:
            course_level = int(course["code"][2:5])
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid course code format: {course.get('code', 'Unknown')} in {dept}. Error: {e}")
            continue
        level_range = [(100, 200), (300, 400), (500, 600), (700, 800), (900, 1000), (1100, 1200), (1300, 1400)]
        matches_level = any(start <= course_level <= end for start, end in level_range if f"{start}-{end}" in level_filter)
        if matches_level and (not search_term or 
                              search_term.lower() in course["name"].lower() or 
                              search_term.lower() in course["code"].lower() or 
                              search_term.lower() in course["desc"].lower()):
            filtered_courses.append((dept, course))

# Sorting logic
if sort_by == "Code (Ascending)":
    filtered_courses.sort(key=lambda x: x[1]["code"])
elif sort_by == "Code (Descending)":
    filtered_courses.sort(key=lambda x: x[1]["code"], reverse=True)
elif sort_by == "Name (A-Z)":
    filtered_courses.sort(key=lambda x: x[1]["name"])
elif sort_by == "Name (Z-A)":
    filtered_courses.sort(key=lambda x: x[1]["name"], reverse=True)

# Main content
col1, col2 = st.columns([3, 1])
with col1:
    if search_term or not show_all:
        st.header("Filtered Results" if search_term else f"{department} - Filtered Courses")
        if filtered_courses:
            for dept, course in filtered_courses:
                if search_term or dept == department:
                    with st.expander(f"{course['code']}: {course['name']}"):
                        st.write(f"**Department:** {dept}")
                        st.write(f"**Description:** {course['desc']}")
                        st.write(f"**Credits:** {course['credits']}")
                        st.write(f"**Prerequisites:** {course['prereq']}")
        else:
            st.write("No courses match your filters.")
    else:
        st.header(department)
        for course in curriculum[department]:
            with st.expander(f"{course['code']}: {course['name']}"):
                st.write(f"**Description:** {course['desc']}")
                st.write(f"**Credits:** {course['credits']}")
                st.write(f"**Prerequisites:** {course['prereq']}")

# PDF Download functionality
def create_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("TITS Curriculum", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Anti-Woke Mission: Merit, Truth, Freedom", styles['Heading2']))
    elements.append(Spacer(1, 12))

    for dept, courses in curriculum.items():
        elements.append(Paragraph(dept, styles['Heading2']))
        data = [["Code", "Name", "Credits", "Prerequisites"]]
        for course in courses:
            data.append([course['code'], course['name'], course['credits'], course['prereq']])
        table = Table(data)
        table.setStyle([('GRID', (0, 0), (-1, -1), 1, 'black'), ('FONTSIZE', (0, 0), (-1, -1), 5)])
        elements.append(table)
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer

with col2:
    st.subheader("Download Options")
    if st.button("Download Full Curriculum as PDF"):
        pdf_buffer = create_pdf()
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="TITS_Curriculum_AntiWoke_364.pdf",
            mime="application/pdf"
        )

# Sidebar additional info
st.sidebar.header("About TITS")
if st.sidebar.checkbox("Mission Statement"):
    st.write("""
    **Mission:**  
    TITS is a fortress of meritocracy, forging STEM pioneers to dominate the cosmos through unfiltered science, 
    raw innovation, and rejection of woke ideology. With data-driven psychology, sociology, and new frontiers 
    like bioinformatics and space law, we prepare students to optimize humanity for a multi-galactic future.
    """)

# Styling
st.markdown("""
    <style>
    .stExpander {
        background-color: #f0f8ff;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #ff4500;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    .stSelectbox, .stTextInput, .stMultiSelect {
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.write("---")
st.write("Powered by xAI | Forging a future of merit, might, and mind.")
