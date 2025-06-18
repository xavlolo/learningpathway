import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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

# CSV file URL (you can change this to your GitHub raw URL)
DEFAULT_CSV_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/courses.csv"

# Load data
st.sidebar.markdown("### 📁 Data Source")
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Upload CSV", "Load from URL", "Use Demo Data"]
)

@st.cache_data
def load_demo_data():
    # Demo data as a fallback
    demo_data = {
        'course_id': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12',
                      'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
                      'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
                      'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12'],
        'name': ['AI Fundamentals', 'ML Theory', 'Deep Learning Concepts', 'Research Methods', 'Advanced Research',
                 'Neural Networks', 'Statistics for AI', 'Computer Vision', 'NLP Research', 'Paper Writing',
                 'Math for ML', 'Reinforcement Learning',
                 'AI for Management', 'Data Governance', 'AI Strategy', 'Implementation Planning', 'AI Leadership',
                 'Budget & ROI', 'AI Ethics Policy', 'Team Building', 'Change Management', 'Risk Assessment',
                 'AI Compliance', 'Performance Metrics',
                 'Teaching AI Basics', 'Curriculum Design', 'Hands-on Workshops', 'Advanced Pedagogy',
                 'AI Ethics Teaching', 'Learning Assessment', 'Educational Tools', 'Student Projects',
                 'Online Teaching', 'AI Lab Setup',
                 'AI Overview', 'Basic Python', 'Applied AI', 'AI Tools', 'Problem Solving', 'AI Applications',
                 'Data Basics', 'ML Concepts', 'AI in Business', 'Practical Projects', 'AI Tools Basics',
                 'Industry Cases'],
        'x': [-0.3, -0.3, 0.7, 0.7, 1.7, 0.3, 0.0, 1.3, 1.3, 2.3, -0.1, 0.9,
              0.3, 1.3, 1.3, 2.3, 2.3, 2.3, -0.3, 0.7, 1.7, 0.7, 1.1, 1.9,
              0.3, 1.0, 1.0, 2.0, -0.3, 2.0, 1.0, 1.7, 0.7, 1.3,
              -0.1, 1.0, 2.0, 1.0, 2.0, 2.0, 0.3, -0.1, 0.3, 1.3, 0.7, 1.7],
        'y': [-0.2, 0.7, 1.3, 2.3, 2.3, 1.7, -0.3, 0.7, 2.3, 1.7, 0.1, 1.1,
              0.3, -0.3, 0.7, 0.7, 2.3, 0.3, 1.3, 0.3, 1.3, 1.7, -0.1, 0.9,
              1.3, 1.3, 1.7, 1.7, 2.3, 1.3, 0.3, 0.7, -0.1, 1.9,
              0.3, 0.1, -0.3, 0.9, 1.1, 2.1, 0.0, 1.1, 2.1, 2.1, -0.3, 0.1],
        'pathway': ['Research']*12 + ['Admin']*12 + ['Education']*10 + ['General']*12,
        'specificity': ['Ideas', 'Ideas', 'Hands-on', 'Hands-on', 'Issue Specific', 'Ideas', 'Ideas',
                        'Hands-on', 'Hands-on', 'Issue Specific', 'Ideas', 'Hands-on',
                        'Ideas', 'Hands-on', 'Hands-on', 'Issue Specific', 'Issue Specific', 'Issue Specific',
                        'Ideas', 'Hands-on', 'Issue Specific', 'Hands-on', 'Hands-on', 'Issue Specific',
                        'Ideas', 'Hands-on', 'Hands-on', 'Issue Specific', 'Ideas', 'Issue Specific',
                        'Hands-on', 'Issue Specific', 'Hands-on', 'Hands-on',
                        'Ideas', 'Hands-on', 'Issue Specific', 'Hands-on', 'Issue Specific', 'Issue Specific',
                        'Ideas', 'Ideas', 'Ideas', 'Hands-on', 'Hands-on', 'Issue Specific'],
        'exposure': ['Never', 'Sometimes', 'Sometimes', 'Daily', 'Daily', 'Daily', 'Never', 'Sometimes',
                     'Daily', 'Daily', 'Never', 'Sometimes',
                     'Never', 'Never', 'Sometimes', 'Sometimes', 'Daily', 'Never', 'Sometimes', 'Never',
                     'Sometimes', 'Daily', 'Never', 'Sometimes',
                     'Sometimes', 'Sometimes', 'Daily', 'Daily', 'Daily', 'Sometimes', 'Never', 'Sometimes',
                     'Never', 'Daily',
                     'Never', 'Never', 'Never', 'Sometimes', 'Sometimes', 'Daily', 'Never', 'Sometimes',
                     'Daily', 'Daily', 'Never', 'Never']
    }
    return pd.DataFrame(demo_data)

# Load data based on selection
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("Please upload a CSV file or select another data source.")
        df = load_demo_data()
elif data_source == "Load from URL":
    csv_url = st.sidebar.text_input("CSV URL:", value=DEFAULT_CSV_URL)
    try:
        df = pd.read_csv(csv_url)
    except:
        st.error("Could not load CSV from URL. Using demo data instead.")
        df = load_demo_data()
else:
    df = load_demo_data()

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

# Add course nodes from DataFrame
for _, course in df.iterrows():
    if selected_pathways.get(course['pathway'], False):
        fig.add_trace(go.Scatter(
            x=[course['x']],
            y=[course['y']],
            mode="markers+text",
            marker=dict(
                size=18,
                color=pathways[course['pathway']]["color"],
                line=dict(color="white", width=1)
            ),
            text=[course['course_id']],
            textposition="middle center",
            textfont=dict(color="white", size=7, family="Arial Bold"),
            name=course['pathway'],
            showlegend=False,
            hovertext=f"<b>{course['name']}</b><br>Pathway: {course['pathway']}<br>Level: {course['specificity']}<br>Exposure: {course['exposure']}",
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
        course_count = len(df[df['pathway'] == pathway])
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
    st.metric("Total Courses", len(df))
with col2:
    st.metric("Active Pathways", sum(selected_pathways.values()))
with col3:
    active_courses = len(df[df['pathway'].isin([p for p, sel in selected_pathways.items() if sel])])
    st.metric("Visible Courses", active_courses)
with col4:
    st.metric("Data Source", data_source)

# Display selected courses in tabs
if any(selected_pathways.values()):
    tab_names = [p for p, selected in selected_pathways.items() if selected]
    tabs = st.tabs(tab_names)
    
    for i, pathway in enumerate(tab_names):
        with tabs[i]:
            pathway_courses = df[df['pathway'] == pathway].sort_values(['exposure', 'specificity'])
            
            for _, course in pathway_courses.iterrows():
                with st.expander(f"**{course['name']}** ({course['specificity']} - {course['exposure']})"):
                    st.write(f"**Course ID:** {course['course_id']}")
                    st.write(f"**Course Type:** {course['specificity']}")
                    st.write(f"**Experience Level:** {course['exposure']}")
                    st.write(f"**Learning Pathway:** {course['pathway']}")
                    
                    # Additional fields from CSV if available
                    extra_cols = [col for col in df.columns if col not in ['course_id', 'name', 'x', 'y', 'pathway', 'specificity', 'exposure']]
                    for col in extra_cols:
                        if pd.notna(course[col]):
                            st.write(f"**{col.replace('_', ' ').title()}:** {course[col]}")
                    
                    # Placeholder for future dropdown functionality
                    st.selectbox(
                        "Select delivery format:",
                        ["Online Self-Paced", "Virtual Instructor-Led", "In-Person Workshop", "Hybrid"],
                        key=f"format_{course['course_id']}"
                    )
                    
                    st.button("Enroll", key=f"enroll_{course['course_id']}", use_container_width=True)

# Instructions
st.markdown("---")
st.markdown("### 📖 How to Use This Learning Pathway")
st.markdown("""
1. **Load Your Data**: Use the sidebar to upload a CSV file, load from URL, or use demo data
2. **Select Pathways**: Use the checkboxes above to display different learning pathways
3. **Explore Courses**: Hover over nodes in the network to see course details
4. **Course Information**: Click on the pathway tabs below to see detailed course information
5. **CSV Format**: Your CSV should include columns: course_id, name, x, y, pathway, specificity, exposure
   - Optional columns: description, duration, prerequisites, learning_outcomes, etc.
""")

# Footer
st.markdown("---")
st.info("💡 **Tip**: You can add additional columns to your CSV file such as 'description', 'duration', 'prerequisites', 'learning_outcomes', etc. These will automatically appear in the course details!")
