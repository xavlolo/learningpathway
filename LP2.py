import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="AI Learning Pathway",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .pathway-legend {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .legend-dot {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 2px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AI Learning Pathway Network")
st.markdown("### Interactive Learning Pathways: Choose Your Journey")

# Define pathways with colors
pathways = {
    "Research": {"color": "#E74C3C", "symbol": "circle"},  # Red
    "Admin": {"color": "#3498DB", "symbol": "circle"},     # Blue
    "Education": {"color": "#2ECC71", "symbol": "circle"}, # Green
    "General": {"color": "#9B59B6", "symbol": "circle"}    # Purple
}

# Define grid positions (x: Specificity, y: Exposure)
# Specificity: 0=Ideas, 1=Hands-on, 2=Issue Specific
# Exposure: 0=Never, 1=Sometimes, 2=Daily
grid_positions = {
    "Ideas": 0,
    "Hands-on": 1,
    "Issue Specific": 2,
    "Never": 0,
    "Sometimes": 1,
    "Daily": 2
}

# Define courses with their positions and pathways
# Adding offsets to prevent overlapping
courses = {
    # Research Pathway (Red)
    "R1": {"name": "AI Fundamentals", "x": -0.3, "y": -0.2, "pathway": "Research", "spec": "Ideas", "exp": "Never"},
    "R2": {"name": "ML Theory", "x": -0.3, "y": 0.7, "pathway": "Research", "spec": "Ideas", "exp": "Sometimes"},
    "R3": {"name": "Deep Learning Concepts", "x": 0.7, "y": 1.3, "pathway": "Research", "spec": "Hands-on", "exp": "Sometimes"},
    "R4": {"name": "Research Methods", "x": 0.7, "y": 2.3, "pathway": "Research", "spec": "Hands-on", "exp": "Daily"},
    "R5": {"name": "Advanced Research", "x": 1.7, "y": 2.3, "pathway": "Research", "spec": "Issue Specific", "exp": "Daily"},
    "R6": {"name": "Neural Networks", "x": 0.3, "y": 1.7, "pathway": "Research", "spec": "Ideas", "exp": "Daily"},
    "R7": {"name": "Statistics for AI", "x": 0.0, "y": -0.3, "pathway": "Research", "spec": "Ideas", "exp": "Never"},
    "R8": {"name": "Computer Vision", "x": 1.3, "y": 0.7, "pathway": "Research", "spec": "Hands-on", "exp": "Sometimes"},
    "R9": {"name": "NLP Research", "x": 1.3, "y": 2.3, "pathway": "Research", "spec": "Hands-on", "exp": "Daily"},
    "R10": {"name": "Paper Writing", "x": 2.3, "y": 1.7, "pathway": "Research", "spec": "Issue Specific", "exp": "Daily"},
    "R11": {"name": "Math for ML", "x": -0.1, "y": 0.1, "pathway": "Research", "spec": "Ideas", "exp": "Never"},
    "R12": {"name": "Reinforcement Learning", "x": 0.9, "y": 1.1, "pathway": "Research", "spec": "Hands-on", "exp": "Sometimes"},
    
    # Admin Pathway (Blue)
    "A1": {"name": "AI for Management", "x": 0.3, "y": 0.3, "pathway": "Admin", "spec": "Ideas", "exp": "Never"},
    "A2": {"name": "Data Governance", "x": 1.3, "y": -0.3, "pathway": "Admin", "spec": "Hands-on", "exp": "Never"},
    "A3": {"name": "AI Strategy", "x": 1.3, "y": 0.7, "pathway": "Admin", "spec": "Hands-on", "exp": "Sometimes"},
    "A4": {"name": "Implementation Planning", "x": 2.3, "y": 0.7, "pathway": "Admin", "spec": "Issue Specific", "exp": "Sometimes"},
    "A5": {"name": "AI Leadership", "x": 2.3, "y": 2.3, "pathway": "Admin", "spec": "Issue Specific", "exp": "Daily"},
    "A6": {"name": "Budget & ROI", "x": 2.3, "y": 0.3, "pathway": "Admin", "spec": "Issue Specific", "exp": "Never"},
    "A7": {"name": "AI Ethics Policy", "x": -0.3, "y": 1.3, "pathway": "Admin", "spec": "Ideas", "exp": "Sometimes"},
    "A8": {"name": "Team Building", "x": 0.7, "y": 0.3, "pathway": "Admin", "spec": "Hands-on", "exp": "Never"},
    "A9": {"name": "Change Management", "x": 1.7, "y": 1.3, "pathway": "Admin", "spec": "Issue Specific", "exp": "Sometimes"},
    "A10": {"name": "Risk Assessment", "x": 0.7, "y": 1.7, "pathway": "Admin", "spec": "Hands-on", "exp": "Daily"},
    "A11": {"name": "AI Compliance", "x": 1.1, "y": -0.1, "pathway": "Admin", "spec": "Hands-on", "exp": "Never"},
    "A12": {"name": "Performance Metrics", "x": 1.9, "y": 0.9, "pathway": "Admin", "spec": "Issue Specific", "exp": "Sometimes"},
    
    # Education Pathway (Green)
    "E1": {"name": "Teaching AI Basics", "x": 0.3, "y": 1.3, "pathway": "Education", "spec": "Ideas", "exp": "Sometimes"},
    "E2": {"name": "Curriculum Design", "x": 1.0, "y": 1.3, "pathway": "Education", "spec": "Hands-on", "exp": "Sometimes"},
    "E3": {"name": "Hands-on Workshops", "x": 1.0, "y": 1.7, "pathway": "Education", "spec": "Hands-on", "exp": "Daily"},
    "E4": {"name": "Advanced Pedagogy", "x": 2.0, "y": 1.7, "pathway": "Education", "spec": "Issue Specific", "exp": "Daily"},
    "E5": {"name": "AI Ethics Teaching", "x": -0.3, "y": 2.3, "pathway": "Education", "spec": "Ideas", "exp": "Daily"},
    "E6": {"name": "Learning Assessment", "x": 2.0, "y": 1.3, "pathway": "Education", "spec": "Issue Specific", "exp": "Sometimes"},
    "E7": {"name": "Educational Tools", "x": 1.0, "y": 0.3, "pathway": "Education", "spec": "Hands-on", "exp": "Never"},
    "E8": {"name": "Student Projects", "x": 1.7, "y": 0.7, "pathway": "Education", "spec": "Issue Specific", "exp": "Sometimes"},
    "E9": {"name": "Online Teaching", "x": 0.7, "y": -0.1, "pathway": "Education", "spec": "Hands-on", "exp": "Never"},
    "E10": {"name": "AI Lab Setup", "x": 1.3, "y": 1.9, "pathway": "Education", "spec": "Hands-on", "exp": "Daily"},
    
    # General Pathway (Purple)
    "G1": {"name": "AI Overview", "x": -0.1, "y": 0.3, "pathway": "General", "spec": "Ideas", "exp": "Never"},
    "G2": {"name": "Basic Python", "x": 1.0, "y": 0.1, "pathway": "General", "spec": "Hands-on", "exp": "Never"},
    "G3": {"name": "Applied AI", "x": 2.0, "y": -0.3, "pathway": "General", "spec": "Issue Specific", "exp": "Never"},
    "G4": {"name": "AI Tools", "x": 1.0, "y": 0.9, "pathway": "General", "spec": "Hands-on", "exp": "Sometimes"},
    "G5": {"name": "Problem Solving", "x": 2.0, "y": 1.1, "pathway": "General", "spec": "Issue Specific", "exp": "Sometimes"},
    "G6": {"name": "AI Applications", "x": 2.0, "y": 2.1, "pathway": "General", "spec": "Issue Specific", "exp": "Daily"},
    "G7": {"name": "Data Basics", "x": 0.3, "y": 0.0, "pathway": "General", "spec": "Ideas", "exp": "Never"},
    "G8": {"name": "ML Concepts", "x": -0.1, "y": 1.1, "pathway": "General", "spec": "Ideas", "exp": "Sometimes"},
    "G9": {"name": "AI in Business", "x": 0.3, "y": 2.1, "pathway": "General", "spec": "Ideas", "exp": "Daily"},
    "G10": {"name": "Practical Projects", "x": 1.3, "y": 2.1, "pathway": "General", "spec": "Hands-on", "exp": "Daily"},
    "G11": {"name": "AI Tools Basics", "x": 0.7, "y": -0.3, "pathway": "General", "spec": "Hands-on", "exp": "Never"},
    "G12": {"name": "Industry Cases", "x": 1.7, "y": 0.1, "pathway": "General", "spec": "Issue Specific", "exp": "Never"},
}

# Define connections for each pathway
connections = {
    "Research": [
        ("R1", "R2"), ("R1", "R7"), ("R7", "R2"), ("R2", "R3"), 
        ("R3", "R4"), ("R3", "R8"), ("R8", "R9"), ("R4", "R5"), 
        ("R2", "R6"), ("R6", "R4"), ("R4", "R9"), ("R9", "R5"), 
        ("R5", "R10"), ("R8", "R10"), ("R11", "R1"), ("R11", "R2"),
        ("R12", "R3"), ("R12", "R8"), ("R1", "R11")
    ],
    "Admin": [
        ("A1", "A2"), ("A1", "A8"), ("A8", "A2"), ("A2", "A3"), 
        ("A3", "A4"), ("A4", "A5"), ("A2", "A6"), ("A6", "A4"), 
        ("A7", "A3"), ("A7", "A10"), ("A10", "A5"), ("A3", "A9"), 
        ("A9", "A5"), ("A8", "A3"), ("A11", "A2"), ("A11", "A3"),
        ("A12", "A4"), ("A12", "A9"), ("A6", "A12")
    ],
    "Education": [
        ("E1", "E2"), ("E2", "E3"), ("E3", "E4"), ("E1", "E5"), 
        ("E5", "E3"), ("E2", "E6"), ("E6", "E4"), ("E7", "E2"), 
        ("E7", "E8"), ("E8", "E6"), ("E1", "E7"), ("E9", "E7"),
        ("E9", "E2"), ("E10", "E3"), ("E10", "E4"), ("E3", "E10")
    ],
    "General": [
        ("G1", "G2"), ("G1", "G7"), ("G7", "G2"), ("G2", "G3"), 
        ("G2", "G4"), ("G4", "G5"), ("G5", "G6"), ("G8", "G4"), 
        ("G8", "G9"), ("G9", "G10"), ("G10", "G6"), ("G3", "G5"), 
        ("G1", "G8"), ("G11", "G2"), ("G11", "G4"), ("G12", "G3"),
        ("G12", "G5"), ("G2", "G12")
    ]
}

# Pathway selector
st.markdown("### 🎯 Select Learning Pathways to Display")
col1, col2, col3, col4 = st.columns(4)

selected_pathways = {}
with col1:
    selected_pathways["Research"] = st.checkbox("Research", value=True)
with col2:
    selected_pathways["Admin"] = st.checkbox("Admin", value=True)
with col3:
    selected_pathways["Education"] = st.checkbox("Education", value=True)
with col4:
    selected_pathways["General"] = st.checkbox("General", value=True)

# Create the network visualization
fig = go.Figure()

# Add grid lines
for i in range(3):
    # Vertical lines
    fig.add_shape(type="line", x0=i-0.5, y0=-0.8, x1=i-0.5, y1=2.8,
                  line=dict(color="lightgray", width=1))
    # Horizontal lines
    fig.add_shape(type="line", x0=-0.8, y0=i-0.5, x1=2.8, y1=i-0.5,
                  line=dict(color="lightgray", width=1))

# Add pathway connections
for pathway, edges in connections.items():
    if selected_pathways.get(pathway, False):
        for edge in edges:
            start_course = courses[edge[0]]
            end_course = courses[edge[1]]
            
            # Calculate control point for curved line
            mid_x = (start_course["x"] + end_course["x"]) / 2
            mid_y = (start_course["y"] + end_course["y"]) / 2
            
            # Add some curvature
            if abs(start_course["x"] - end_course["x"]) > 0.5:
                mid_y += 0.05
            if abs(start_course["y"] - end_course["y"]) > 0.5:
                mid_x += 0.05
            
            # Create curved path
            import numpy as np
            t = np.linspace(0, 1, 50)
            x_curve = (1-t)**2 * start_course["x"] + 2*(1-t)*t * mid_x + t**2 * end_course["x"]
            y_curve = (1-t)**2 * start_course["y"] + 2*(1-t)*t * mid_y + t**2 * end_course["y"]
            
            # Add edge
            fig.add_trace(go.Scatter(
                x=x_curve,
                y=y_curve,
                mode="lines",
                line=dict(color=pathways[pathway]["color"], width=2),
                name=pathway,
                showlegend=False,
                hoverinfo="skip",
                opacity=0.7
            ))

# Add course nodes
for course_id, course in courses.items():
    if selected_pathways.get(course["pathway"], False):
        fig.add_trace(go.Scatter(
            x=[course["x"]],
            y=[course["y"]],
            mode="markers+text",
            marker=dict(
                size=18,
                color=pathways[course["pathway"]]["color"],
                line=dict(color="white", width=1)
            ),
            text=[course_id],
            textposition="middle center",
            textfont=dict(color="white", size=7, family="Arial Bold"),
            name=course["pathway"],
            showlegend=False,
            hovertext=f"<b>{course['name']}</b><br>Pathway: {course['pathway']}<br>Level: {course['spec']}<br>Exposure: {course['exp']}",
            hoverinfo="text"
        ))

# Update layout
fig.update_layout(
    title="Learning Pathway Network",
    xaxis=dict(
        title="Specificity →",
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=["Ideas", "Hands-on", "Issue Specific"],
        range=[-0.8, 2.8],
        showgrid=False
    ),
    yaxis=dict(
        title="← Exposure",
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=["Never", "Sometimes", "Daily"],
        range=[-0.8, 2.8],
        showgrid=False
    ),
    height=700,
    hovermode="closest",
    plot_bgcolor="white",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Legend
st.markdown("### 🎨 Pathway Legend")
cols = st.columns(4)
for i, (pathway, style) in enumerate(pathways.items()):
    with cols[i]:
        course_count = len([c for c in courses.values() if c["pathway"] == pathway])
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 20px; height: 20px; border-radius: 50%; background-color: {style["color"]}; border: 2px solid #333;"></div>
            <span style="font-weight: 500;">{pathway} ({course_count} courses)</span>
        </div>
        """, unsafe_allow_html=True)

# Course details section
st.markdown("### 📚 Course Details")
st.markdown("*Hover over any node in the graph to see course information*")

# Summary statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Courses", len(courses))
with col2:
    st.metric("Active Pathways", sum(selected_pathways.values()))
with col3:
    active_courses = len([c for c in courses.values() if selected_pathways.get(c["pathway"], False)])
    st.metric("Visible Courses", active_courses)
with col4:
    active_connections = sum([len(connections[p]) for p in pathways if selected_pathways.get(p, False)])
    st.metric("Connections", active_connections)

# Display selected courses in tabs
if any(selected_pathways.values()):
    tab_names = [p for p, selected in selected_pathways.items() if selected]
    tabs = st.tabs(tab_names)
    
    for i, pathway in enumerate(tab_names):
        with tabs[i]:
            pathway_courses = [c for c in courses.values() if c["pathway"] == pathway]
            
            for course in pathway_courses:
                with st.expander(f"**{course['name']}** ({course['spec']} - {course['exp']})"):
                    st.write(f"**Course Type:** {course['spec']}")
                    st.write(f"**Experience Level:** {course['exp']}")
                    st.write(f"**Learning Pathway:** {course['pathway']}")
                    
                    # Placeholder for future dropdown functionality
                    st.selectbox(
                        "Select delivery format:",
                        ["Online Self-Paced", "Virtual Instructor-Led", "In-Person Workshop", "Hybrid"],
                        key=f"format_{course['name']}"
                    )
                    
                    st.button("Enroll", key=f"enroll_{course['name']}", use_container_width=True)

# Instructions
st.markdown("---")
st.markdown("### 📖 How to Use This Learning Pathway")
st.markdown("""
1. **Select Pathways**: Use the checkboxes above to display different learning pathways
2. **Explore Courses**: Hover over nodes in the network to see course details
3. **Follow Connections**: Lines show the recommended progression through courses
4. **Choose Your Path**: Each pathway is designed for different roles and goals:
   - 🔴 **Research** (12 courses): For those pursuing AI research and advanced theory
   - 🔵 **Admin** (12 courses): For managers and leaders implementing AI strategies
   - 🟢 **Education** (10 courses): For educators teaching AI concepts
   - 🟣 **General** (12 courses): For general practitioners and beginners
5. **Navigate Complexity**: Courses progress from left to right (Ideas → Hands-on → Issue Specific) and bottom to top (Never → Sometimes → Daily)
""")

# Footer
st.markdown("---")
st.info("💡 **Next Steps**: Select courses from your chosen pathway and build your personalized learning journey! With 46 total courses across 4 pathways, there are multiple routes to AI mastery.")