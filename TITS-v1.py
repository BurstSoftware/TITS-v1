import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

# Set page config for a wider layout
st.set_page_config(page_title="TITS Curriculum", layout="wide")

# Initialize session state for selected courses
if 'selected_courses' not in st.session_state:
    st.session_state.selected_courses = []

# Title and header
st.title("Texas Institute of Technology and Science (TITS)")
st.subheader("Curriculum Explorer - Austin, Texas")
st.write("Conquer the cosmos with unapologetic STEM excellence, rooted in merit, truth, and relentless innovation—no woke nonsense tolerated.")

# Updated curriculum with 26 departments, 364 courses
curriculum = {
    "Department of Aerospace Engineering": [
        {"code": "AE101", "name": "Intro to Rocket Design", "desc": "Master propulsion with raw engineering prowess.", "credits": 3, "prereq": "None"},
        {"code": "AE202", "name": "Orbital Mechanics", "desc": "Navigate space with cold, hard math.", "credits": 4, "prereq": "AE101"},
        {"code": "AE303", "name": "Mars Colonization Engineering", "desc": "Build habitats with unyielding logic.", "credits": 4, "prereq": "AE202"},
        {"code": "AE404", "name": "Hypersonic Flight", "desc": "Push speed limits with fearless innovation.", "credits": 4, "prereq": "AE202"},
        {"code": "AE505", "name": "Spacecraft Systems Integration", "desc": "Engineer ships that deliver, no fluff.", "credits": 4, "prereq": "AE303"},
        {"code": "AE606", "name": "Interplanetary Mission Design", "desc": "Plan missions with ruthless precision.", "credits": 4, "prereq": "AE404"},
        {"code": "AE707", "name": "Asteroid Mining Tech", "desc": "Extract resources with relentless grit.", "credits": 4, "prereq": "AE505"},
        {"code": "AE808", "name": "Starship Architecture", "desc": "Design vessels for the bold, not the timid.", "credits": 4, "prereq": "AE606"},
        {"code": "AE909", "name": "Interstellar Propulsion", "desc": "Chase FTL with unfiltered science.", "credits": 4, "prereq": "AE707"},
        {"code": "AE1010", "name": "Galactic Navigation", "desc": "Map the galaxy with iron will.", "credits": 4, "prereq": "AE808"},
        {"code": "AE1111", "name": "Space Combat Engineering", "desc": "Defend humanity with ruthless efficiency.", "credits": 4, "prereq": "AE909"},
        {"code": "AE1212", "name": "Cosmic Mega-Transports", "desc": "Move civilizations with no handouts.", "credits": 4, "prereq": "AE1010"},
        {"code": "AE1313", "name": "Anti-Woke Space Logistics", "desc": "Optimize fleets, reject mediocrity.", "credits": 4, "prereq": "AE1212"},
        {"code": "AE1414", "name": "Universal Expansion Tech", "desc": "Conquer the cosmos with merit-driven mastery.", "credits": 4, "prereq": "AE1313"}
    ],
    "Department of Artificial Intelligence": [
        {"code": "AI101", "name": "Fundamentals of Machine Learning", "desc": "Code algorithms that dominate, no excuses.", "credits": 3, "prereq": "None"},
        {"code": "AI202", "name": "AI for Autonomous Systems", "desc": "Program machines with unrelenting logic.", "credits": 4, "prereq": "AI101"},
        {"code": "AI303", "name": "Ethics in AI: Truth Over Trash", "desc": "Reason AI’s impact, shred woke lies.", "credits": 3, "prereq": "AI202"},
        {"code": "AI404", "name": "Deep Learning Architectures", "desc": "Build networks with cold precision.", "credits": 4, "prereq": "AI202"},
        {"code": "AI505", "name": "AI in Robotics", "desc": "Merge AI and bots with hard results.", "credits": 4, "prereq": "AI404"},
        {"code": "AI606", "name": "Generative AI Systems", "desc": "Create with AI, no coddling allowed.", "credits": 4, "prereq": "AI505"},
        {"code": "AI707", "name": "AI for Space Exploration", "desc": "Navigate stars with unfiltered intelligence.", "credits": 4, "prereq": "AI606"},
        {"code": "AI808", "name": "Artificial General Intelligence", "desc": "Pursue AGI with merit-driven focus.", "credits": 4, "prereq": "AI707"},
        {"code": "AI909", "name": "AI Swarm Intelligence", "desc": "Coordinate AI with ruthless efficiency.", "credits": 4, "prereq": "AI808"},
        {"code": "AI1010", "name": "Post-Human AI", "desc": "Forge AI beyond limits, no apologies.", "credits": 4, "prereq": "AI909"},
        {"code": "AI1111", "name": "AI Truth Engines", "desc": "Seek facts with unyielding code.", "credits": 4, "prereq": "AI1010"},
        {"code": "AI1212", "name": "Galactic AI Governance", "desc": "Rule AI systems with strength.", "credits": 4, "prereq": "AI1111"},
        {"code": "AI1313", "name": "Anti-Woke AI Design", "desc": "Build AI free of collectivist nonsense.", "credits": 4, "prereq": "AI1212"},
        {"code": "AI1414", "name": "Cosmic AI Optimization", "desc": "Maximize AI across stars with merit.", "credits": 4, "prereq": "AI1313"}
    ],
    "Department of Psychology for STEM": [
        {"code": "PSY101", "name": "Intro to Scientific Psychology", "desc": "Study minds with data, not feelings.", "credits": 3, "prereq": "None"},
        {"code": "PSY202", "name": "Cognitive Science Basics", "desc": "Decode thought with rigorous science.", "credits": 4, "prereq": "PSY101"},
        {"code": "PSY303", "name": "Behavioral Analysis for Engineers", "desc": "Optimize humans with empirical facts.", "credits": 4, "prereq": "PSY202"},
        {"code": "PSY404", "name": "Decision-Making Models", "desc": "Predict choices with unyielding logic.", "credits": 4, "prereq": "PSY202"},
        {"code": "PSY505", "name": "Team Dynamics in STEM", "desc": "Build elite crews with merit, no fluff.", "credits": 4, "prereq": "PSY303"},
        {"code": "PSY606", "name": "Stress and Resilience Tech", "desc": "Forge unbreakable minds with science.", "credits": 4, "prereq": "PSY404"},
        {"code": "PSY707", "name": "Space Psychology", "desc": "Master isolation with relentless focus.", "credits": 4, "prereq": "PSY505"},
        {"code": "PSY808", "name": "Anti-Woke Psych Ethics", "desc": "Reason behavior, reject feelings-first dogma.", "credits": 4, "prereq": "PSY606"},
        {"code": "PSY909", "name": "Neural Data Analysis", "desc": "Crunch brain data with cold precision.", "credits": 4, "prereq": "PSY707"},
        {"code": "PSY1010", "name": "Galactic Crew Optimization", "desc": "Maximize team performance across stars.", "credits": 4, "prereq": "PSY808"},
        {"code": "PSY1111", "name": "Cognitive Enhancement Tech", "desc": "Boost minds with no apologies.", "credits": 4, "prereq": "PSY909"},
        {"code": "PSY1212", "name": "Cosmic Psych Resilience", "desc": "Forge minds for the cosmic frontier.", "credits": 4, "prereq": "PSY1010"},
        {"code": "PSY1313", "name": "Anti-Woke Behavioral Engineering", "desc": "Engineer behavior with merit-driven science.", "credits": 4, "prereq": "PSY1212"},
        {"code": "PSY1414", "name": "Universal Psych Mastery", "desc": "Dominate cognition across galaxies.", "credits": 4, "prereq": "PSY1313"}
    ],
    "Department of Sociology for STEM": [
        {"code": "SOC101", "name": "Intro to Systems Sociology", "desc": "Study society with data, not narratives.", "credits": 3, "prereq": "None"},
        {"code": "SOC202", "name": "Social Structures for Engineers", "desc": "Analyze groups with scientific rigor.", "credits": 4, "prereq": "SOC101"},
        {"code": "SOC303", "name": "Quantitative Social Analysis", "desc": "Crunch social data, no woke fluff.", "credits": 4, "prereq": "SOC202"},
        {"code": "SOC404", "name": "Merit-Based Social Dynamics", "desc": "Optimize societies with hard results.", "credits": 4, "prereq": "SOC202"},
        {"code": "SOC505", "name": "Space Colony Sociology", "desc": "Build communities with unyielding logic.", "credits": 4, "prereq": "SOC303"},
        {"code": "SOC606", "name": "Anti-Woke Social Theory", "desc": "Reject collectivism with fierce reason.", "credits": 4, "prereq": "SOC404"},
        {"code": "SOC707", "name": "Tech-Driven Social Systems", "desc": "Engineer societies with proven outcomes.", "credits": 4, "prereq": "SOC505"},
        {"code": "SOC808", "name": "Galactic Social Networks", "desc": "Link societies across stars with efficiency.", "credits": 4, "prereq": "SOC606"},
        {"code": "SOC909", "name": "Social Optimization Models", "desc": "Maximize groups with data-driven science.", "credits": 4, "prereq": "SOC707"},
        {"code": "SOC1010", "name": "Cosmic Social Resilience", "desc": "Forge societies for the cosmic frontier.", "credits": 4, "prereq": "SOC808"},
        {"code": "SOC1111", "name": "Anti-Woke Governance", "desc": "Rule with strength, no collectivist traps.", "credits": 4, "prereq": "SOC909"},
        {"code": "SOC1212", "name": "Universal Social Engineering", "desc": "Design societies with no excuses.", "credits": 4, "prereq": "SOC1010"},
        {"code": "SOC1313", "name": "Merit-Driven Social Optimization", "desc": "Peak social performance with science.", "credits": 4, "prereq": "SOC1212"},
        {"code": "SOC1414", "name": "Merit-Based Social Mastery", "desc": "Dominate social systems across galaxies.", "credits": 4, "prereq": "SOC1313"}
    ],
    "Department of Bioinformatics": [
        {"code": "BI101", "name": "Intro to Bioinformatics", "desc": "Analyze genomes with raw data skill.", "credits": 3, "prereq": "None"},
        {"code": "BI202", "name": "Genomic Data Analysis", "desc": "Decode DNA with unyielding precision.", "credits": 4, "prereq": "BI101"},
        {"code": "BI303", "name": "Proteomics for Engineers", "desc": "Engineer proteins with hard science.", "credits": 4, "prereq": "BI202"},
        {"code": "BI404", "name": "Computational Biology", "desc": "Model life with cold logic.", "credits": 4, "prereq": "BI202"},
        {"code": "BI505", "name": "Space Biotech Informatics", "desc": "Analyze life off-world with results.", "credits": 4, "prereq": "BI303"},
        {"code": "BI606", "name": "Anti-Woke Bio-Data Ethics", "desc": "Reason data use, reject dogma.", "credits": 4, "prereq": "BI404"},
        {"code": "BI707", "name": "Synthetic Genome Design", "desc": "Craft genomes with fearless innovation.", "credits": 4, "prereq": "BI505"},
        {"code": "BI808", "name": "Galactic Bio-Databases", "desc": "Store life data across stars.", "credits": 4, "prereq": "BI606"},
        {"code": "BI909", "name": "Exo-Bioinformatics", "desc": "Analyze alien life with merit.", "credits": 4, "prereq": "BI707"},
        {"code": "BI1010", "name": "Cosmic Life Optimization", "desc": "Optimize biology with no apologies.", "credits": 4, "prereq": "BI808"},
        {"code": "BI1111", "name": "Anti-Woke Genomic Policy", "desc": "Govern bio-data with strength.", "credits": 4, "prereq": "BI1010"},
        {"code": "BI1212", "name": "Universal Bio-Data Systems", "desc": "Rule bio-data across cosmos.", "credits": 4, "prereq": "BI1111"},
        {"code": "BI1313", "name": "Bioinformatics Optimization", "desc": "Maximize bio-data with science.", "credits": 4, "prereq": "BI1212"},
        {"code": "BI1414", "name": "Cosmic Bioinfo Mastery", "desc": "Dominate life data across galaxies.", "credits": 4, "prereq": "BI1313"}
    ],
    "Department of Space Law and Policy": [
        {"code": "SL101", "name": "Intro to Space Law", "desc": "Master cosmic law with merit.", "credits": 3, "prereq": "None"},
        {"code": "SL202", "name": "Planetary Governance", "desc": "Rule planets with unyielding logic.", "credits": 4, "prereq": "SL101"},
        {"code": "SL303", "name": "Interstellar Trade Law", "desc": "Govern trade with cold reason.", "credits": 4, "prereq": "SL202"},
        {"code": "SL404", "name": "Anti-Woke Policy Frameworks", "desc": "Reject collectivism in space governance.", "credits": 4, "prereq": "SL202"},
        {"code": "SL505", "name": "Space Property Rights", "desc": "Secure assets with fierce logic.", "credits": 4, "prereq": "SL303"},
        {"code": "SL606", "name": "Cosmic Conflict Resolution", "desc": "Resolve disputes with results.", "credits": 4, "prereq": "SL404"},
        {"code": "SL707", "name": "Galactic Legal Systems", "desc": "Design laws for stars with strength.", "credits": 4, "prereq": "SL505"},
        {"code": "SL808", "name": "Anti-Woke Space Ethics", "desc": "Reason right, no woke nonsense.", "credits": 4, "prereq": "SL606"},
        {"code": "SL909", "name": "Universal Jurisdiction Models", "desc": "Govern cosmos with no apologies.", "credits": 4, "prereq": "SL707"},
        {"code": "SL1010", "name": "Cosmic Policy Optimization", "desc": "Maximize governance with science.", "credits": 4, "prereq": "SL808"},
        {"code": "SL1111", "name": "Merit-Based Cosmic Law", "desc": "Rule with merit, no fluff.", "credits": 4, "prereq": "SL909"},
        {"code": "SL1212", "name": "Galactic Policy Mastery", "desc": "Dominate law across stars.", "credits": 4, "prereq": "SL1010"},
        {"code": "SL1313", "name": "Anti-Woke Legal Optimization", "desc": "Peak law with unfiltered reason.", "credits": 4, "prereq": "SL1212"},
        {"code": "SL1414", "name": "Universal Legal Dominance", "desc": "Govern galaxies with iron will.", "credits": 4, "prereq": "SL1313"}
    ],
    # Remaining 20 departments (abbreviated for brevity, same structure as before with updated descriptions)
    "Department of Sustainable Energy": [
        {"code": "SE101", "name": "Solar Power Systems", "desc": "Harness sun with unrelenting skill.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to SE1414
    ],
    "Department of Physics and Space Science": [
        {"code": "PS101", "name": "Quantum Mechanics", "desc": "Grasp reality with unfiltered truth.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to PS1414
    ],
    "Department of Entrepreneurial Engineering": [
        {"code": "EE101", "name": "Startup Fundamentals", "desc": "Build empires with raw ambition.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to EE1414
    ],
    "Department of Materials Science": [
        {"code": "MS101", "name": "Intro to Materials Engineering", "desc": "Forge materials with cold precision.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to MS1414
    ],
    "Department of Biotechnology": [
        {"code": "BT101", "name": "Intro to Genetic Engineering", "desc": "Edit DNA with merit-driven science.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to BT1414
    ],
    "Department of Computer Science": [
        {"code": "CS101", "name": "Programming Foundations", "desc": "Code with unrelenting skill.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to CS1414
    ],
    "Department of Civil and Planetary Engineering": [
        {"code": "CE101", "name": "Structural Engineering Basics", "desc": "Build strong with fearless logic.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to CE1414
    ],
    "Department of Neuroscience and Cybernetics": [
        {"code": "NC101", "name": "Intro to Neuroscience", "desc": "Decode brains with raw reason.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to NC1414
    ],
    "Department of Mathematics and Theoretical Sciences": [
        {"code": "MT101", "name": "Advanced Calculus", "desc": "Master math with unapologetic rigor.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to MT1414
    ],
    "Department of Robotics and Automation": [
        {"code": "RA101", "name": "Intro to Robotics", "desc": "Build bots with cold efficiency.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to RA1414
    ],
    "Department of Environmental Systems": [
        {"code": "ES101", "name": "Earth Systems Science", "desc": "Study Earth with unfiltered data.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to ES1414
    ],
    "Department of Astrophysics and Cosmology": [
        {"code": "AC101", "name": "Intro to Astronomy", "desc": "Observe stars with relentless truth.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to AC1414
    ],
    "Department of Quantum Technologies": [
        {"code": "QT101", "name": "Quantum Fundamentals", "desc": "Master quantum with fierce rigor.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to QT1414
    ],
    "Department of Interdisciplinary Futures": [
        {"code": "IF101", "name": "Futures Thinking", "desc": "Predict progress with unfiltered reason.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to IF1414
    ],
    "Department of Mechanical Engineering": [
        {"code": "ME101", "name": "Mechanics Basics", "desc": "Master forces with raw skill.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to ME1414
    ],
    "Department of Electrical and Electronic Engineering": [
        {"code": "EE101", "name": "Circuit Fundamentals", "desc": "Wire power with cold precision.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to EE1414
    ],
    "Department of Chemical Engineering": [
        {"code": "CH101", "name": "Chemical Principles", "desc": "Master reactions with fearless science.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to CH1414
    ],
    "Department of Philosophy of Science and Technology": [
        {"code": "PT101", "name": "Logic and Reason", "desc": "Think straight, no woke distortions.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to PT1414
    ],
    "Department of Data Science and Analytics": [
        {"code": "DS101", "name": "Intro to Data Science", "desc": "Analyze with unrelenting skill.", "credits": 3, "prereq": "None"},
        # ... 13 more courses, up to DS1414
    ]
}

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
        course_level = int(course["code"][2:5])
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
