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
curriculum = {
    "Aerospace Engineering": [
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
    "Artificial Intelligence": [
        {"code": "AI101", "name": "Fundamentals of Machine Learning", "desc": "Code algorithms that dominate, no excuses.", "credits": 3, "prereq": "None"},
        {"code": "AI202", "name": "AI for Autonomous Systems", "desc": "Program machines with unrelenting logic.", "credits": 4, "prereq": "AI101"},
        {"code": "AI303", "name": "Ethics in AI: Truth Over Trash", "desc": "Reason AI’s impact, shred woke lies.", "credits": 4, "prereq": "AI202"},
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
    "Psychology for STEM": [
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
    "Sociology for STEM": [
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
    "Bioinformatics": [
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
    "Space Law and Policy": [
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
    "Sustainable Energy": [
        {"code": "SE101", "name": "Solar Power Systems", "desc": "Harness sun with unrelenting skill.", "credits": 3, "prereq": "None"},
        {"code": "SE202", "name": "Battery Technology", "desc": "Store energy with proven science.", "credits": 4, "prereq": "SE101"},
        {"code": "SE303", "name": "Terraforming Technologies", "desc": "Engineer planets with fearless grit.", "credits": 4, "prereq": "SE202"},
        {"code": "SE404", "name": "Fusion Energy Principles", "desc": "Master fusion with cold reason.", "credits": 4, "prereq": "SE202"},
        {"code": "SE505", "name": "Wind and Hydro Dynamics", "desc": "Tap nature with raw ingenuity.", "credits": 4, "prereq": "SE303"},
        {"code": "SE606", "name": "Energy Grid Optimization", "desc": "Build grids with no fluff.", "credits": 4, "prereq": "SE404"},
        {"code": "SE707", "name": "Geothermal Engineering", "desc": "Drill deep with unyielding focus.", "credits": 4, "prereq": "SE505"},
        {"code": "SE808", "name": "Space-Based Solar Power", "desc": "Capture solar in orbit, no excuses.", "credits": 4, "prereq": "SE606"},
        {"code": "SE909", "name": "Antimatter Energy", "desc": "Unlock power with relentless pursuit.", "credits": 4, "prereq": "SE808"},
        {"code": "SE1010", "name": "Stellar Energy Harvesting", "desc": "Steal from stars with efficiency.", "credits": 4, "prereq": "SE909"},
        {"code": "SE1111", "name": "Planetary Core Energy", "desc": "Tap cores with fearless tech.", "credits": 4, "prereq": "SE1010"},
        {"code": "SE1212", "name": "Cosmic Energy Networks", "desc": "Link stars with bold ambition.", "credits": 4, "prereq": "SE1111"},
        {"code": "SE1313", "name": "Anti-Woke Energy Policy", "desc": "Power reality, reject green dogma.", "credits": 4, "prereq": "SE1212"},
        {"code": "SE1414", "name": "Universal Energy Mastery", "desc": "Dominate energy across cosmos.", "credits": 4, "prereq": "SE1313"}
    ],
    "Physics and Space Science": [
        {"code": "PS101", "name": "Quantum Mechanics", "desc": "Grasp reality with unfiltered truth.", "credits": 3, "prereq": "None"},
        {"code": "PS202", "name": "Astrophysics", "desc": "Study cosmos with relentless precision.", "credits": 4, "prereq": "PS101"},
        {"code": "PS303", "name": "Space Exploration Physics", "desc": "Conquer space with hard facts.", "credits": 4, "prereq": "PS202"},
        {"code": "PS404", "name": "Relativity and Gravitation", "desc": "Master Einstein with no compromises.", "credits": 4, "prereq": "PS202"},
        {"code": "PS505", "name": "Particle Physics", "desc": "Probe the core with fierce reason.", "credits": 4, "prereq": "PS303"},
        {"code": "PS606", "name": "Cosmic Radiation Studies", "desc": "Face dangers with bold science.", "credits": 4, "prereq": "PS404"},
        {"code": "PS707", "name": "Dark Matter and Energy", "desc": "Unveil truths, no dogma allowed.", "credits": 4, "prereq": "PS505"},
        {"code": "PS808", "name": "Wormhole Theory", "desc": "Explore shortcuts with fearless logic.", "credits": 4, "prereq": "PS606"},
        {"code": "PS909", "name": "Quantum Gravity", "desc": "Unify physics with unyielding focus.", "credits": 4, "prereq": "PS707"},
        {"code": "PS1010", "name": "Cosmic Engineering", "desc": "Bend spacetime with raw intellect.", "credits": 4, "prereq": "PS808"},
        {"code": "PS1111", "name": "Parallel Universe Physics", "desc": "Seek realities with no fantasies.", "credits": 4, "prereq": "PS909"},
        {"code": "PS1212", "name": "Universal Constants Redefined", "desc": "Challenge limits with merit.", "credits": 4, "prereq": "PS1010"},
        {"code": "PS1313", "name": "Anti-Woke Physics Inquiry", "desc": "Pursue truth, reject relativism.", "credits": 4, "prereq": "PS1212"},
        {"code": "PS1414", "name": "Galactic Physics Mastery", "desc": "Rule the cosmos with unfiltered science.", "credits": 4, "prereq": "PS1313"}
    ],
    "Entrepreneurial Engineering": [
        {"code": "EE101", "name": "Startup Fundamentals", "desc": "Build empires with raw ambition.", "credits": 3, "prereq": "None"},
        {"code": "EE202", "name": "Disruptive Innovation", "desc": "Break molds with fearless ingenuity.", "credits": 4, "prereq": "EE101"},
        {"code": "EE303", "name": "Space Economy", "desc": "Profit in space with merit-driven strategy.", "credits": 4, "prereq": "EE202"},
        {"code": "EE404", "name": "Venture Capital Strategies", "desc": "Raise funds with proven results.", "credits": 4, "prereq": "EE202"},
        {"code": "EE505", "name": "Product Development Cycles", "desc": "Deliver winners, no excuses.", "credits": 4, "prereq": "EE303"},
        {"code": "EE606", "name": "Global Tech Leadership", "desc": "Lead with strength, not sentiment.", "credits": 4, "prereq": "EE404"},
        {"code": "EE707", "name": "Tech Policy: Freedom First", "desc": "Fight rules with fierce logic.", "credits": 4, "prereq": "EE505"},
        {"code": "EE808", "name": "Interstellar Commerce", "desc": "Trade across stars with bold ambition.", "credits": 4, "prereq": "EE606"},
        {"code": "EE909", "name": "Mega-Corp Strategy", "desc": "Run trillions with iron will.", "credits": 4, "prereq": "EE707"},
        {"code": "EE1010", "name": "Galactic Trade Systems", "desc": "Dominate markets with no handouts.", "credits": 4, "prereq": "EE808"},
        {"code": "EE1111", "name": "Anti-Woke Business Models", "desc": "Thrive without collectivist traps.", "credits": 4, "prereq": "EE909"},
        {"code": "EE1212", "name": "Cosmic Monopoly Theory", "desc": "Own the universe with merit.", "credits": 4, "prereq": "EE1010"},
        {"code": "EE1313", "name": "Freedom-Driven Ventures", "desc": "Build free markets, reject woke dogma.", "credits": 4, "prereq": "EE1212"},
        {"code": "EE1414", "name": "Universal Enterprise Design", "desc": "Rule commerce across cosmos.", "credits": 4, "prereq": "EE1313"}
    ],
    "Materials Science": [
        {"code": "MS101", "name": "Intro to Materials Engineering", "desc": "Forge materials with cold precision.", "credits": 3, "prereq": "None"},
        {"code": "MS202", "name": "Nanotechnology", "desc": "Manipulate atoms with unyielding skill.", "credits": 4, "prereq": "MS101"},
        {"code": "MS303", "name": "Composites for Aerospace", "desc": "Build tough with no compromises.", "credits": 4, "prereq": "MS202"},
        {"code": "MS404", "name": "Smart Materials", "desc": "Engineer adaptability with hard science.", "credits": 4, "prereq": "MS202"},
        {"code": "MS505", "name": "Materials for Energy Storage", "desc": "Power the future with proven tech.", "credits": 4, "prereq": "MS303"},
        {"code": "MS606", "name": "Space-Grade Materials", "desc": "Craft for extremes, no fluff.", "credits": 4, "prereq": "MS404"},
        {"code": "MS707", "name": "Self-Healing Materials", "desc": "Innovate resilience with relentless focus.", "credits": 4, "prereq": "MS505"},
        {"code": "MS808", "name": "Metamaterials", "desc": "Defy limits with bold engineering.", "credits": 4, "prereq": "MS606"},
        {"code": "MS909", "name": "Quantum Materials", "desc": "Harness quanta with unyielding pursuit.", "credits": 4, "prereq": "MS707"},
        {"code": "MS1010", "name": "Exotic Matter Engineering", "desc": "Create the impossible with science.", "credits": 4, "prereq": "MS808"},
        {"code": "MS1111", "name": "Anti-Fragile Materials", "desc": "Thrive under stress, no cságáling.", "credits": 4, "prereq": "MS909"},
        {"code": "MS1212", "name": "Cosmic Fabrication", "desc": "Build for galaxies with fierce drive.", "credits": 4, "prereq": "MS1010"},
        {"code": "MS1313", "name": "Anti-Woke Material Design", "desc": "Forge reality, reject nonsense.", "credits": 4, "prereq": "MS1212"},
        {"code": "MS1414", "name": "Universal Material Mastery", "desc": "Dominate matter across cosmos.", "credits": 4, "prereq": "MS1313"}
    ],
    "Biotechnology": [
        {"code": "BT101", "name": "Intro to Genetic Engineering", "desc": "Edit DNA with merit-driven science.", "credits": 3, "prereq": "None"},
        {"code": "BT202", "name": "Synthetic Biology", "desc": "Design life with unfiltered reason.", "credits": 4, "prereq": "BT101"},
        {"code": "BT303", "name": "Bioengineering for Space", "desc": "Support humans off-world, no fluff.", "credits": 4, "prereq": "BT202"},
        {"code": "BT404", "name": "CRISPR Applications", "desc": "Perfect genes with cold precision.", "credits": 4, "prereq": "BT202"},
        {"code": "BT505", "name": "Regenerative Medicine", "desc": "Heal with science, not sanctimony.", "credits": 4, "prereq": "BT303"},
        {"code": "BT606", "name": "Biotech for Sustainability", "desc": "Feed worlds with hard results.", "credits": 4, "prereq": "BT404"},
        {"code": "BT707", "name": "Neural Enhancement", "desc": "Boost brains with fearless innovation.", "credits": 4, "prereq": "BT505"},
        {"code": "BT808", "name": "Xeno-Biology", "desc": "Study alien life with unyielding curiosity.", "credits": 4, "prereq": "BT606"},
        {"code": "BT909", "name": "Immortality Research", "desc": "Defy death with relentless science.", "credits": 4, "prereq": "BT707"},
        {"code": "BT1010", "name": "Post-Biological Evolution", "desc": "Evolve beyond flesh with raw intellect.", "credits": 4, "prereq": "BT808"},
        {"code": "BT1111", "name": "Anti-Woke Bioethics", "desc": "Challenge nonsense with fierce truth.", "credits": 4, "prereq": "BT909"},
        {"code": "BT1212", "name": "Galactic Lifeforms", "desc": "Engineer life for stars, no limits.", "credits": 4, "prereq": "BT1010"},
        {"code": "BT1313", "name": "Bio-Optimization Tech", "desc": "Maximize life with merit-driven science.", "credits": 4, "prereq": "BT1212"},
        {"code": "BT1414", "name": "Cosmic Bio-Dominance", "desc": "Rule life across cosmos.", "credits": 4, "prereq": "BT1313"}
    ],
    "Computer Science": [
        {"code": "CS101", "name": "Programming Foundations", "desc": "Code with unrelenting skill.", "credits": 3, "prereq": "None"},
        {"code": "CS202", "name": "Data Structures and Algorithms", "desc": "Solve problems with cold efficiency.", "credits": 4, "prereq": "CS101"},
        {"code": "CS303", "name": "Distributed Systems", "desc": "Scale networks with proven results.", "credits": 4, "prereq": "CS202"},
        {"code": "CS404", "name": "Cybersecurity Essentials", "desc": "Defend with logic, not lectures.", "credits": 4, "prereq": "CS202"},
        {"code": "CS505", "name": "Quantum Computing", "desc": "Compute beyond with hard science.", "credits": 4, "prereq": "CS303"},
        {"code": "CS606", "name": "Software for Space Missions", "desc": "Code for stars, no fluff.", "credits": 4, "prereq": "CS404"},
        {"code": "CS707", "name": "Blockchain Technologies", "desc": "Decentralize with fearless innovation.", "credits": 4, "prereq": "CS505"},
        {"code": "CS808", "name": "Exascale Computing", "desc": "Push performance with raw power.", "credits": 4, "prereq": "CS606"},
        {"code": "CS909", "name": "Holographic Computing", "desc": "Build 3D systems with bold vision.", "credits": 4, "prereq": "CS707"},
        {"code": "CS1010", "name": "Universal Simulation", "desc": "Code reality with unyielding ambition.", "credits": 4, "prereq": "CS808"},
        {"code": "CS1111", "name": "Anti-Censorship Tech", "desc": "Protect freedom with unfiltered code.", "credits": 4, "prereq": "CS909"},
        {"code": "CS1212", "name": "Galactic Computing Grids", "desc": "Link stars with fierce logic.", "credits": 4, "prereq": "CS1010"},
        {"code": "CS1313", "name": "Anti-Woke Software Design", "desc": "Build truth-driven systems.", "credits": 4, "prereq": "CS1212"},
        {"code": "CS1414", "name": "Cosmic Code Mastery", "desc": "Dominate computation across cosmos.", "credits": 4, "prereq": "CS1313"}
    ],
    "Civil and Planetary Engineering": [
        {"code": "CE101", "name": "Structural Engineering Basics", "desc": "Build strong with fearless logic.", "credits": 3, "prereq": "None"},
        {"code": "CE202", "name": "Planetary Infrastructure", "desc": "Engineer Mars with unyielding grit.", "credits": 4, "prereq": "CE101"},
        {"code": "CE303", "name": "Sustainable Urban Design", "desc": "Plan cities with proven results.", "credits": 4, "prereq": "CE202"},
        {"code": "CE404", "name": "Seismic Engineering", "desc": "Defy quakes with hard science.", "credits": 4, "prereq": "CE202"},
        {"code": "CE505", "name": "Space Habitat Construction", "desc": "Build in orbit with bold ingenuity.", "credits": 4, "prereq": "CE303"},
        {"code": "CE606", "name": "Megastructure Engineering", "desc": "Erect giants with cold precision.", "credits": 4, "prereq": "CE404"},
        {"code": "CE707", "name": "Atmospheric Engineering", "desc": "Shape climates with unfiltered facts.", "credits": 4, "prereq": "CE505"},
        {"code": "CE808", "name": "Dyson Sphere Concepts", "desc": "Engineer stars with relentless vision.", "credits": 4, "prereq": "CE606"},
        {"code": "CE909", "name": "Orbital Ring Systems", "desc": "Link planets with fierce scale.", "credits": 4, "prereq": "CE707"},
        {"code": "CE1010", "name": "Galactic Habitats", "desc": "House humanity with no handouts.", "credits": 4, "prereq": "CE808"},
        {"code": "CE1111", "name": "Anti-Woke Urbanism", "desc": "Design for merit, not madness.", "credits": 4, "prereq": "CE909"},
        {"code": "CE1212", "name": "Cosmic Civil Mastery", "desc": "Rule infrastructure with iron will.", "credits": 4, "prereq": "CE1010"},
        {"code": "CE1313", "name": "Planetary Defense Systems", "desc": "Protect with ruthless efficiency.", "credits": 4, "prereq": "CE1212"},
        {"code": "CE1414", "name": "Universal Habitat Design", "desc": "Dominate living across cosmos.", "credits": 4, "prereq": "CE1313"}
    ],
    "Neuroscience and Cybernetics": [
        {"code": "NC101", "name": "Intro to Neuroscience", "desc": "Decode brains with raw reason.", "credits": 3, "prereq": "None"},
        {"code": "NC202", "name": "Brain-Computer Interfaces", "desc": "Link minds with unyielding skill.", "credits": 4, "prereq": "NC101"},
        {"code": "NC303", "name": "Cybernetic Enhancements", "desc": "Augment with fearless science.", "credits": 4, "prereq": "NC202"},
        {"code": "NC404", "name": "Cognitive Modeling", "desc": "Simulate thought with cold truth.", "credits": 4, "prereq": "NC202"},
        {"code": "NC505", "name": "Neural Repair Tech", "desc": "Fix brains with proven results.", "credits": 4, "prereq": "NC303"},
        {"code": "NC606", "name": "Consciousness Studies", "desc": "Probe minds with unfiltered logic.", "credits": 4, "prereq": "NC404"},
        {"code": "NC707", "name": "AI-Human Symbiosis", "desc": "Merge with AI with bold ambition.", "credits": 4, "prereq": "NC505"},
        {"code": "NC808", "name": "Telepathic Interfaces", "desc": "Connect brains with relentless tech.", "credits": 4, "prereq": "NC606"},
        {"code": "NC909", "name": "Mind Uploading", "desc": "Digitize minds with no apologies.", "credits": 4, "prereq": "NC707"},
        {"code": "NC1010", "name": "Collective Consciousness", "desc": "Link minds with fierce innovation.", "credits": 4, "prereq": "NC808"},
        {"code": "NC1111", "name": "Anti-Woke Cognition", "desc": "Enhance thought, reject nonsense.", "credits": 4, "prereq": "NC909"},
        {"code": "NC1212", "name": "Galactic Neural Networks", "desc": "Unite minds across stars with merit.", "credits": 4, "prereq": "NC1010"},
        {"code": "NC1313", "name": "Neural Optimization", "desc": "Maximize brains with unfiltered science.", "credits": 4, "prereq": "NC1212"},
        {"code": "NC1414", "name": "Cosmic Mind Mastery", "desc": "Dominate consciousness across galaxies.", "credits": 4, "prereq": "NC1313"}
    ],
    "Mathematics and Theoretical Sciences": [
        {"code": "MT101", "name": "Advanced Calculus", "desc": "Master math with unapologetic rigor.", "credits": 3, "prereq": "None"},
        {"code": "MT202", "name": "Linear Algebra", "desc": "Solve systems with cold precision.", "credits": 4, "prereq": "MT101"},
        {"code": "MT303", "name": "Probability and Statistics", "desc": "Analyze data with unfiltered facts.", "credits": 4, "prereq": "MT202"},
        {"code": "MT404", "name": "Number Theory", "desc": "Unlock primes with fierce logic.", "credits": 4, "prereq": "MT202"},
        {"code": "MT505", "name": "Topology", "desc": "Shape spaces with relentless math.", "credits": 4, "prereq": "MT303"},
        {"code": "MT606", "name": "Chaos and Dynamical Systems", "desc": "Tame chaos with raw intellect.", "credits": 4, "prereq": "MT404"},
        {"code": "MT707", "name": "String Theory Math", "desc": "Probe dimensions with unyielding reason.", "credits": 4, "prereq": "MT505"},
        {"code": "MT808", "name": "Multiverse Modeling", "desc": "Map realities with bold math.", "credits": 4, "prereq": "MT606"},
        {"code": "MT909", "name": "Infinite Set Theory", "desc": "Grasp infinity with fierce focus.", "credits": 4, "prereq": "MT707"},
        {"code": "MT1010", "name": "Cosmic Algorithmics", "desc": "Code the universe with iron will.", "credits": 4, "prereq": "MT808"},
        {"code": "MT1111", "name": "Anti-Woke Math Logic", "desc": "Prove truth, reject relativism.", "credits": 4, "prereq": "MT909"},
        {"code": "MT1212", "name": "Galactic Math Frameworks", "desc": "Structure cosmos with merit.", "credits": 4, "prereq": "MT1010"},
        {"code": "MT1313", "name": "Universal Math Optimization", "desc": "Maximize math with unfiltered science.", "credits": 4, "prereq": "MT1212"},
        {"code": "MT1414", "name": "Cosmic Math Dominance", "desc": "Rule numbers across galaxies.", "credits": 4, "prereq": "MT1313"}
    ],
    "Robotics and Automation": [
        {"code": "RA101", "name": "Intro to Robotics", "desc": "Build bots with cold efficiency.", "credits": 3, "prereq": "None"},
        {"code": "RA202", "name": "Robotic Kinematics", "desc": "Control motion with unyielding precision.", "credits": 4, "prereq": "RA101"},
        {"code": "RA303", "name": "Automation in Industry", "desc": "Automate with proven results.", "credits": 4, "prereq": "RA202"},
        {"code": "RA404", "name": "Swarm Robotics", "desc": "Coordinate bots with fierce efficiency.", "credits": 4, "prereq": "RA202"},
        {"code": "RA505", "name": "Robots for Space", "desc": "Deploy off-world with hard science.", "credits": 4, "prereq": "RA303"},
        {"code": "RA606", "name": "Human-Robot Interaction", "desc": "Design interfaces with unfiltered pragmatism.", "credits": 4, "prereq": "RA404"},
        {"code": "RA707", "name": "Soft Robotics", "desc": "Craft flexible bots with relentless focus.", "credits": 4, "prereq": "RA505"},
        {"code": "RA808", "name": "Planetary Rover Design", "desc": "Roam worlds with bold tech.", "credits": 4, "prereq": "RA606"},
        {"code": "RA909", "name": "Nano-Robotics", "desc": "Engineer microscale with no excuses.", "credits": 4, "prereq": "RA707"},
        {"code": "RA1010", "name": "Self-Replicating Machines", "desc": "Create bots that build themselves.", "credits": 4, "prereq": "RA808"},
        {"code": "RA1111", "name": "Anti-Woke Automation", "desc": "Automate merit, reject mediocrity.", "credits": 4, "prereq": "RA909"},
        {"code": "RA1212", "name": "Galactic Robotic Colonies", "desc": "Rule stars with machines.", "credits": 4, "prereq": "RA1010"},
        {"code": "RA1313", "name": "Robotic Optimization", "desc": "Maximize bots with unfiltered science.", "credits": 4, "prereq": "RA1212"},
        {"code": "RA1414", "name": "Cosmic Automation Mastery", "desc": "Dominate robotics across galaxies.", "credits": 4, "prereq": "RA1313"}
    ],
    "Environmental Systems": [
        {"code": "ES101", "name": "Earth Systems Science", "desc": "Study Earth with unfiltered data.", "credits": 3, "prereq": "None"},
        {"code": "ES202", "name": "Climate Modeling", "desc": "Predict climates with cold data.", "credits": 4, "prereq": "ES101"},
        {"code": "ES303", "name": "Eco-Engineering", "desc": "Fix Earth with proven results.", "credits": 4, "prereq": "ES202"},
        {"code": "ES404", "name": "Oceanic Technologies", "desc": "Tap oceans with fearless ingenuity.", "credits": 4, "prereq": "ES202"},
        {"code": "ES505", "name": "Planetary Restoration", "desc": "Restore worlds with hard science.", "credits": 4, "prereq": "ES303"},
        {"code": "ES606", "name": "Exo-Environmental Design", "desc": "Build ecosystems, no fluff.", "credits": 4, "prereq": "ES404"},
        {"code": "ES707", "name": "Carbon Capture Systems", "desc": "Cut CO2 with ruthless efficiency.", "credits": 4, "prereq": "ES505"},
        {"code": "ES808", "name": "Bio-Mimetic Engineering", "desc": "Copy nature with unfiltered logic.", "credits": 4, "prereq": "ES606"},
        {"code": "ES909", "name": "Interstellar Ecology", "desc": "Design for stars, no excuses.", "credits": 4, "prereq": "ES707"},
        {"code": "ES1010", "name": "Universal Terraforming", "desc": "Shape planets with bold ambition.", "credits": 4, "prereq": "ES808"},
        {"code": "ES1111", "name": "Anti-Woke Eco-Solutions", "desc": "Solve crises with merit, no dogma.", "credits": 4, "prereq": "ES909"},
        {"code": "ES1212", "name": "Cosmic Eco-Dominance", "desc": "Rule nature across galaxies.", "credits": 4, "prereq": "ES1010"},
        {"code": "ES1313", "name": "Eco-Optimization Tech", "desc": "Maximize ecosystems with unfiltered science.", "credits": 4, "prereq": "ES1212"},
        {"code": "ES1414", "name": "Universal Eco-Mastery", "desc": "Dominate environments across cosmos.", "credits": 4, "prereq": "ES1313"}
    ],
    "Astrophysics and Cosmology": [
        {"code": "AC101", "name": "Intro to Astronomy", "desc": "Observe stars with relentless truth.", "credits": 3, "prereq": "None"},
        {"code": "AC202", "name": "Stellar Dynamics", "desc": "Study stars with cold precision.", "credits": 4, "prereq": "AC101"},
        {"code": "AC303", "name": "Galactic Structures", "desc": "Map galaxies with unfiltered facts.", "credits": 4, "prereq": "AC202"},
        {"code": "AC404", "name": "Cosmological Models", "desc": "Model universe with fierce reason.", "credits": 4, "prereq": "AC202"},
        {"code": "AC505", "name": "Exoplanet Studies", "desc": "Find worlds with hard science.", "credits": 4, "prereq": "AC303"},
        {"code": "AC606", "name": "Gravitational Waves", "desc": "Detect spacetime with relentless focus.", "credits": 4, "prereq": "AC404"},
        {"code": "AC707", "name": "Black Hole Physics", "desc": "Probe singularities with raw intellect.", "credits": 4, "prereq": "AC505"},
        {"code": "AC808", "name": "Dark Universe Exploration", "desc": "Unveil unseen with no apologies.", "credits": 4, "prereq": "AC606"},
        {"code": "AC909", "name": "Intergalactic Travel Theory", "desc": "Cross galaxies with bold math.", "credits": 4, "prereq": "AC707"},
        {"code": "AC1010", "name": "Cosmic Origins", "desc": "Trace the bang with unfiltered logic.", "credits": 4, "prereq": "AC808"},
        {"code": "AC1111", "name": "Anti-Woke Cosmology", "desc": "Seek truth, reject myths.", "credits": 4, "prereq": "AC909"},
        {"code": "AC1212", "name": "Galactic Dominion Physics", "desc": "Rule cosmos with merit.", "credits": 4, "prereq": "AC1010"},
        {"code": "AC1313", "name": "Cosmic Optimization", "desc": "Maximize universe with unfiltered science.", "credits": 4, "prereq": "AC1212"},
        {"code": "AC1414", "name": "Universal Cosmic Mastery", "desc": "Dominate stars across galaxies.", "credits": 4, "prereq": "AC1313"}
    ],
    "Quantum Technologies": [
        {"code": "QT101", "name": "Quantum Fundamentals", "desc": "Master quantum with fierce rigor.", "credits": 3, "prereq": "None"},
        {"code": "QT202", "name": "Quantum Information", "desc": "Encode with cold precision.", "credits": 4, "prereq": "QT101"},
        {"code": "QT303", "name": "Quantum Cryptography", "desc": "Secure with unfiltered science.", "credits": 4, "prereq": "QT202"},
        {"code": "QT404", "name": "Quantum Computing Basics", "desc": "Build quantum with no fluff.", "credits": 4, "prereq": "QT202"},
        {"code": "QT505", "name": "Quantum Sensors", "desc": "Measure with relentless accuracy.", "credits": 4, "prereq": "QT303"},
        {"code": "QT606", "name": "Quantum Networking", "desc": "Link quantum with bold innovation.", "credits": 4, "prereq": "QT404"},
        {"code": "QT707", "name": "Quantum Teleportation", "desc": "Move states with fearless tech.", "credits": 4, "prereq": "QT505"},
        {"code": "QT808", "name": "Quantum Materials Tech", "desc": "Engineer quanta with unyielding skill.", "credits": 4, "prereq": "QT606"},
        {"code": "QT909", "name": "Quantum Field Applications", "desc": "Apply fields with fierce logic.", "credits": 4, "prereq": "QT707"},
        {"code": "QT1010", "name": "Quantum Reality Engineering", "desc": "Shape reality with raw ambition.", "credits": 4, "prereq": "QT808"},
        {"code": "QT1111", "name": "Anti-Woke Quantum Ethics", "desc": "Reason use, reject dogma.", "credits": 4, "prereq": "QT909"},
        {"code": "QT1212", "name": "Galactic Quantum Systems", "desc": "Rule quantum with merit.", "credits": 4, "prereq": "QT1010"},
        {"code": "QT1313", "name": "Quantum Optimization", "desc": "Maximize quanta with unfiltered science.", "credits": 4, "prereq": "QT1212"},
        {"code": "QT1414", "name": "Cosmic Quantum Mastery", "desc": "Dominate quantum across galaxies.", "credits": 4, "prereq": "QT1313"}
    ],
    "Interdisciplinary Futures": [
        {"code": "IF101", "name": "Futures Thinking", "desc": "Predict progress with unfiltered reason.", "credits": 3, "prereq": "None"},
        {"code": "IF202", "name": "Systems Integration", "desc": "Merge tech with cold efficiency.", "credits": 4, "prereq": "IF101"},
        {"code": "IF303", "name": "Space-Human Synergy", "desc": "Unite man and machine with hard science.", "credits": 4, "prereq": "IF202"},
        {"code": "IF404", "name": "Ethics of Progress: Truth First", "desc": "Reason right, no woke lies.", "credits": 4, "prereq": "IF202"},
        {"code": "IF505", "name": "Tech and Society", "desc": "Shape culture with proven results.", "credits": 4, "prereq": "IF303"},
        {"code": "IF606", "name": "Multi-Planetary Governance", "desc": "Rule planets with fierce strength.", "credits": 4, "prereq": "IF404"},
        {"code": "IF707", "name": "Synthetic Ecosystems", "desc": "Design nature with unfiltered logic.", "credits": 4, "prereq": "IF505"},
        {"code": "IF808", "name": "Post-Scarcity Economics", "desc": "Master wealth with merit.", "credits": 4, "prereq": "IF606"},
        {"code": "IF909", "name": "Cosmic Civilization Design", "desc": "Build societies with bold vision.", "credits": 4, "prereq": "IF707"},
        {"code": "IF1010", "name": "Transhuman Evolution", "desc": "Evolve humanity with raw ambition.", "credits": 4, "prereq": "IF808"},
        {"code": "IF1111", "name": "Anti-Woke Futures", "desc": "Plan ahead, reject collectivist traps.", "credits": 4, "prereq": "IF909"},
        {"code": "IF1212", "name": "Galactic Meritocracy", "desc": "Rule cosmos with excellence.", "credits": 4, "prereq": "IF1010"},
        {"code": "IF1313", "name": "Future Optimization", "desc": "Maximize futures with unfiltered science.", "credits": 4, "prereq": "IF1212"},
        {"code": "IF1414", "name": "Cosmic Future Mastery", "desc": "Dominate destiny across galaxies.", "credits": 4, "prereq": "IF1313"}
    ],
    "Mechanical Engineering": [
        {"code": "ME101", "name": "Mechanics Basics", "desc": "Master forces with raw skill.", "credits": 3, "prereq": "None"},
        {"code": "ME202", "name": "Thermodynamics", "desc": "Harness heat with cold precision.", "credits": 4, "prereq": "ME101"},
        {"code": "ME303", "name": "Fluid Dynamics", "desc": "Control fluids with unfiltered science.", "credits": 4, "prereq": "ME202"},
        {"code": "ME404", "name": "Machine Design", "desc": "Build machines with fearless ingenuity.", "credits": 4, "prereq": "ME202"},
        {"code": "ME505", "name": "Robotic Mechanisms", "desc": "Engineer motion with proven results.", "credits": 4, "prereq": "ME303"},
        {"code": "ME606", "name": "Space Propulsion Systems", "desc": "Power ships with bold innovation.", "credits": 4, "prereq": "ME404"},
        {"code": "ME707", "name": "Hyperloop Engineering", "desc": "Move fast with relentless tech.", "credits": 4, "prereq": "ME505"},
        {"code": "ME808", "name": "Planetary Drills", "desc": "Bore worlds with fierce efficiency.", "credits": 4, "prereq": "ME606"},
        {"code": "ME909", "name": "Zero-Point Energy Tech", "desc": "Tap infinite power with raw ambition.", "credits": 4, "prereq": "ME707"},
        {"code": "ME1010", "name": "Galactic Machinery", "desc": "Build for stars with unyielding focus.", "credits": 4, "prereq": "ME808"},
        {"code": "ME1111", "name": "Anti-Woke Mechanics", "desc": "Engineer reality, no fluff.", "credits": 4, "prereq": "ME909"},
        {"code": "ME1212", "name": "Cosmic Engine Design", "desc": "Power universe with merit.", "credits": 4, "prereq": "ME1010"},
        {"code": "ME1313", "name": "Mech Optimization", "desc": "Maximize machines with unfiltered science.", "credits": 4, "prereq": "ME1212"},
        {"code": "ME1414", "name": "Universal Mech Mastery", "desc": "Dominate mechanics across cosmos.", "credits": 4, "prereq": "ME1313"}
    ],
    "Electrical and Electronic Engineering": [
        {"code": "EE101", "name": "Circuit Fundamentals", "desc": "Wire power with cold precision.", "credits": 3, "prereq": "None"},
        {"code": "EE202", "name": "Electromagnetism", "desc": "Master fields with unyielding skill.", "credits": 4, "prereq": "EE101"},
        {"code": "EE303", "name": "Power Systems", "desc": "Deliver energy with proven science.", "credits": 4, "prereq": "EE202"},
        {"code": "EE404", "name": "Microelectronics", "desc": "Shrink tech with fearless ingenuity.", "credits": 4, "prereq": "EE202"},
        {"code": "EE505", "name": "Signal Processing", "desc": "Decode signals with hard results.", "credits": 4, "prereq": "EE303"},
        {"code": "EE606", "name": "Space Communication Systems", "desc": "Link stars with bold tech.", "credits": 4, "prereq": "EE404"},
        {"code": "EE707", "name": "Neural Interface Electronics", "desc": "Wire brains with relentless innovation.", "credits": 4, "prereq": "EE505"},
        {"code": "EE808", "name": "Quantum Electronics", "desc": "Harness quanta with fierce focus.", "credits": 4, "prereq": "EE606"},
        {"code": "EE909", "name": "Galactic Power Grids", "desc": "Electrify stars with raw ambition.", "credits": 4, "prereq": "EE707"},
        {"code": "EE1010", "name": "Anti-Matter Circuits", "desc": "Power impossible with no excuses.", "credits": 4, "prereq": "EE808"},
        {"code": "EE1111", "name": "Anti-Woke Electronics", "desc": "Build for truth, not trends.", "credits": 4, "prereq": "EE909"},
        {"code": "EE1212", "name": "Cosmic Signal Mastery", "desc": "Rule waves with merit.", "credits": 4, "prereq": "EE1010"},
        {"code": "EE1313", "name": "Electro-Optimization", "desc": "Maximize power with unfiltered science.", "credits": 4, "prereq": "EE1212"},
        {"code": "EE1414", "name": "Universal Electro-Mastery", "desc": "Dominate electricity across cosmos.", "credits": 4, "prereq": "EE1313"}
    ],
    "Chemical Engineering": [
        {"code": "CH101", "name": "Chemical Principles", "desc": "Master reactions with fearless science.", "credits": 3, "prereq": "None"},
        {"code": "CH202", "name": "Process Engineering", "desc": "Refine with cold precision.", "credits": 4, "prereq": "CH101"},
        {"code": "CH303", "name": "Materials Synthesis", "desc": "Craft substances with unfiltered science.", "credits": 4, "prereq": "CH202"},
        {"code": "CH404", "name": "Catalysis Tech", "desc": "Boost reactions with bold ingenuity.", "credits": 4, "prereq": "CH202"},
        {"code": "CH505", "name": "Fuel Cell Engineering", "desc": "Power up with proven results.", "credits": 4, "prereq": "CH303"},
        {"code": "CH606", "name": "Space Chemistry", "desc": "Synthesize in orbit with relentless tech.", "credits": 4, "prereq": "CH404"},
        {"code": "CH707", "name": "Nano-Chemistry", "desc": "Engineer atoms with fierce innovation.", "credits": 4, "prereq": "CH505"},
        {"code": "CH808", "name": "Planetary Atmosphere Chem", "desc": "Shape air with unyielding focus.", "credits": 4, "prereq": "CH606"},
        {"code": "CH909", "name": "Exo-Chemical Engineering", "desc": "Forge alien compounds with raw ambition.", "credits": 4, "prereq": "CH707"},
        {"code": "CH1010", "name": "Galactic Resource Chem", "desc": "Extract wealth with no excuses.", "credits": 4, "prereq": "CH808"},
        {"code": "CH1111", "name": "Anti-Woke Chem Ethics", "desc": "Reason use, reject dogma.", "credits": 4, "prereq": "CH909"},
        {"code": "CH1212", "name": "Cosmic Alchemy", "desc": "Transform matter with merit.", "credits": 4, "prereq": "CH1010"},
        {"code": "CH1313", "name": "Chem Optimization", "desc": "Maximize chemistry with unfiltered science.", "credits": 4, "prereq": "CH1212"},
        {"code": "CH1414", "name": "Universal Chem Mastery", "desc": "Dominate chemicals across cosmos.", "credits": 4, "prereq": "CH1313"}
    ],
    "Philosophy of Science and Technology": [
        {"code": "PT101", "name": "Logic and Reason", "desc": "Think straight, no woke distortions.", "credits": 3, "prereq": "None"},
        {"code": "PT202", "name": "History of Science", "desc": "Learn from giants, not ideologues.", "credits": 4, "prereq": "PT101"},
        {"code": "PT303", "name": "Tech Progress Philosophy", "desc": "Advance with truth, not trends.", "credits": 4, "prereq": "PT202"},
        {"code": "PT404", "name": "Ethics of Innovation", "desc": "Reason right, reject relativism.", "credits": 4, "prereq": "PT202"},
        {"code": "PT505", "name": "Science vs. Dogma", "desc": "Fight nonsense with fierce logic.", "credits": 4, "prereq": "PT303"},
        {"code": "PT606", "name": "Space Exploration Philosophy", "desc": "Justify stars with unfiltered thought.", "credits": 4, "prereq": "PT404"},
        {"code": "PT707", "name": "AI and Human Destiny", "desc": "Debate futures with cold reason.", "credits": 4, "prereq": "PT505"},
        {"code": "PT808", "name": "Anti-Woke Epistemology", "desc": "Know truth, shred lies.", "credits": 4, "prereq": "PT606"},
        {"code": "PT909", "name": "Cosmic Purpose Theory", "desc": "Seek meaning with relentless inquiry.", "credits": 4, "prereq": "PT707"},
        {"code": "PT1010", "name": "Galactic Ethics", "desc": "Rule stars with merit-based morals.", "credits": 4, "prereq": "PT808"},
        {"code": "PT1111", "name": "Freedom in Science", "desc": "Defend inquiry with iron will.", "credits": 4, "prereq": "PT909"},
        {"code": "PT1212", "name": "Universal Truth Pursuit", "desc": "Chase absolutes with no fluff.", "credits": 4, "prereq": "PT1010"},
        {"code": "PT1313", "name": "Anti-Woke Thought Optimization", "desc": "Maximize reason with unfiltered science.", "credits": 4, "prereq": "PT1212"},
        {"code": "PT1414", "name": "Cosmic Philosophical Mastery", "desc": "Dominate thought across galaxies.", "credits": 4, "prereq": "PT1313"}
    ],
    "Data Science and Analytics": [
        {"code": "DS101", "name": "Intro to Data Science", "desc": "Analyze with unrelenting skill.", "credits": 3, "prereq": "None"},
        {"code": "DS202", "name": "Statistical Modeling", "desc": "Predict with cold precision.", "credits": 4, "prereq": "DS101"},
        {"code": "DS303", "name": "Big Data Systems", "desc": "Handle data with unfiltered science.", "credits": 4, "prereq": "DS202"},
        {"code": "DS404", "name": "Machine Learning for Analytics", "desc": "Optimize with fearless ingenuity.", "credits": 4, "prereq": "DS202"},
        {"code": "DS505", "name": "Space Data Analysis", "desc": "Crunch cosmic data with proven results.", "credits": 4, "prereq": "DS303"},
        {"code": "DS606", "name": "Real-Time Analytics", "desc": "Analyze live with bold tech.", "credits": 4, "prereq": "DS404"},
        {"code": "DS707", "name": "Anti-Woke Data Ethics", "desc": "Reason data use, reject dogma.", "credits": 4, "prereq": "DS505"},
        {"code": "DS808", "name": "Galactic Data Networks", "desc": "Link data across stars with efficiency.", "credits": 4, "prereq": "DS606"},
        {"code": "DS909", "name": "Predictive Cosmic Models", "desc": "Forecast with no apologies.", "credits": 4, "prereq": "DS707"},
        {"code": "DS1010", "name": "Universal Data Optimization", "desc": "Maximize data with raw ambition.", "credits": 4, "prereq": "DS808"},
        {"code": "DS1111", "name": "Data-Driven Truth Engines", "desc": "Seek facts with unfiltered code.", "credits": 4, "prereq": "DS909"},
        {"code": "DS1212", "name": "Cosmic Analytics Mastery", "desc": "Rule data across cosmos.", "credits": 4, "prereq": "DS1010"},
        {"code": "DS1313", "name": "Anti-Woke Data Systems", "desc": "Build truth-driven analytics.", "credits": 4, "prereq": "DS1212"},
        {"code": "DS1414", "name": "Universal Data Dominance", "desc": "Dominate data across galaxies.", "credits": 4, "prereq": "DS1313"}
    ],
    "Nanoengineering": [
        {"code": "NE101", "name": "Intro to Nanoengineering", "desc": "Engineer the nanoscale with raw skill.", "credits": 3, "prereq": "None"},
        {"code": "NE202", "name": "Nanomaterials", "desc": "Craft materials with cold precision.", "credits": 4, "prereq": "NE101"},
        {"code": "NE303", "name": "Nanoelectronics", "desc": "Build circuits with unfiltered science.", "credits": 4, "prereq": "NE202"},
        {"code": "NE404", "name": "Nanobiotechnology", "desc": "Engineer life at nanoscale with bold ingenuity.", "credits": 4, "prereq": "NE202"},
        {"code": "NE505", "name": "Nanoscale Fabrication", "desc": "Create with proven results.", "credits": 4, "prereq": "NE303"},
        {"code": "NE606", "name": "Space Nanotech Applications", "desc": "Apply nano in orbit with relentless tech.", "credits": 4, "prereq": "NE404"},
        {"code": "NE707", "name": "Nanomedicine", "desc": "Heal with nanoscale innovation.", "credits": 4, "prereq": "NE505"},
        {"code": "NE808", "name": "Nanoenergy Systems", "desc": "Power with fierce efficiency.", "credits": 4, "prereq": "NE606"},
        {"code": "NE909", "name": "Quantum Nanotechnology", "desc": "Harness quanta with unyielding focus.", "credits": 4, "prereq": "NE707"},
        {"code": "NE1010", "name": "Galactic Nanoengineering", "desc": "Engineer stars with raw ambition.", "credits": 4, "prereq": "NE808"},
        {"code": "NE1111", "name": "Anti-Woke Nano Ethics", "desc": "Reason nano use, reject dogma.", "credits": 4, "prereq": "NE909"},
        {"code": "NE1212", "name": "Cosmic Nano Fabrication", "desc": "Build nanoscale across cosmos.", "credits": 4, "prereq": "NE1010"},
        {"code": "NE1313", "name": "Nano Optimization", "desc": "Maximize nanoscale with unfiltered science.", "credits": 4, "prereq": "NE1212"},
        {"code": "NE1414", "name": "Universal Nano Mastery", "desc": "Dominate nanoscale across galaxies.", "credits": 4, "prereq": "NE1313"}
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
