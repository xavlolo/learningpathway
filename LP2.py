import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="AI Training Offers Learning Pathway",
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
    .filter-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AI Training Offers Learning Pathway")
st.markdown("### Interactive Learning Pathways: Explore Available Training Sessions")

# Define pathways with colors (based on actual CSV Learning Pathway column)
pathways = {
    "Engineering": {"color": "#E74C3C", "symbol": "circle"},  # Red
    "Operation": {"color": "#3498DB", "symbol": "circle"},    # Blue
    "Research": {"color": "#2ECC71", "symbol": "circle"},     # Green
    "Education": {"color": "#9B59B6", "symbol": "circle"}     # Purple
}

# Function to process training offers data
@st.cache_data
def process_training_data(df):
    """Process the training offers data to match the expected format"""
    processed_data = []
    
    for idx, row in df.iterrows():
        # Generate course ID
        course_id = f"T{idx+1:02d}"
        
        # Map exposure level
        exposure_mapping = {
            "Lv. 1 - Never used AI": "Never",
            "Lv. 2 - Sometimes use AI": "Sometimes", 
            "Lv. 3 - Use AI on a daily basis": "Daily",
            "Lv. Anyone": "Anyone"
        }
        exposure = exposure_mapping.get(row['Audience Exposure Level'], 'Anyone')
        
        # Map specificity
        specificity_mapping = {
            "Lv.1 - Ideas": "Ideas",
            "Lv.2 - Hands On": "Hands-on",
            "Lv.3 - Issue Specific": "Issue Specific"
        }
        specificity = specificity_mapping.get(row['Specificity'], 'Ideas')
        
        # Use the actual Learning Pathway from CSV (clean up any trailing spaces)
        pathway = row['Learning Pathway'].strip() if pd.notna(row['Learning Pathway']) else 'General'
        
        # Generate coordinates based on specificity and exposure
        specificity_x = {"Ideas": 0, "Hands-on": 1, "Issue Specific": 2}
        exposure_y = {"Never": 0, "Sometimes": 1, "Daily": 2, "Anyone": 1.5}
        
        # Add some randomness to avoid overlapping
        x = specificity_x.get(specificity, 0) + np.random.uniform(-0.3, 0.3)
        y = exposure_y.get(exposure, 1) + np.random.uniform(-0.3, 0.3)
        
        processed_data.append({
            'course_id': course_id,
            'name': row['Name'],
            'instructor': row['Instructor/Presenter'],
            'description': row['Short description'],
            'x': x,
            'y': y,
            'pathway': pathway,
            'specificity': specificity,
            'exposure': exposure,
            'original_exposure': row['Audience Exposure Level'],
            'original_specificity': row['Specificity']
        })
    
    return pd.DataFrame(processed_data)

# Load data
st.sidebar.markdown("### 📁 Data Source")
data_source = st.sidebar.radio(
    "Choose data source:",
    ["Training Offers Database", "Upload CSV", "Use Demo Data"]
)

@st.cache_data
def load_training_data():
    """Load the training offers database"""
    try:
        # Try to load the training database
        df = pd.read_csv('TrainingOffersDatabase2025.csv')
        return process_training_data(df)
    except FileNotFoundError:
        st.error("Training Offers Database2025.csv not found. Please upload the file.")
        return None
    except Exception as e:
        st.error(f"Error loading training database: {str(e)}")
        return None

@st.cache_data
def load_demo_data():
    # Demo data as a fallback
    demo_data = {
        'course_id': ['T01', 'T02', 'T03', 'T04', 'T05', 'T06'],
        'name': ['AI Development Basics', 'Operations with AI', 'AI Leadership', 'General AI Overview', 'Advanced AI Tools', 'AI Ethics'],
        'instructor': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', 'Diana Lee'],
        'description': ['Learn AI development fundamentals', 'AI in operations', 'Leading AI initiatives', 'General AI concepts', 'Advanced AI applications', 'AI ethics and governance'],
        'x': [0.1, 1.2, 2.1, 0.8, 1.5, 0.3],
        'y': [0.2, 1.1, 2.0, 0.5, 1.8, 1.3],
        'pathway': ['Engineering', 'Operation', 'Research', 'Education', 'Engineering', 'Research'],
        'specificity': ['Ideas', 'Hands-on', 'Issue Specific', 'Ideas', 'Hands-on', 'Ideas'],
        'exposure': ['Never', 'Sometimes', 'Daily', 'Anyone', 'Daily', 'Sometimes'],
        'original_exposure': ['Lv. 1 - Never used AI', 'Lv. 2 - Sometimes use AI', 'Lv. 3 - Use AI on a daily basis', 'Lv. Anyone', 'Lv. 3 - Use AI on a daily basis', 'Lv. 2 - Sometimes use AI'],
        'original_specificity': ['Lv.1 - Ideas', 'Lv.2 - Hands On', 'Lv.3 - Issue Specific', 'Lv.1 - Ideas', 'Lv.2 - Hands On', 'Lv.1 - Ideas']
    }
    return pd.DataFrame(demo_data)

# Load data based on selection
if data_source == "Training Offers Database":
    df = load_training_data()
    if df is None:
        st.info("Using demo data instead.")
        df = load_demo_data()
elif data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            if 'Name' in raw_df.columns and 'Instructor/Presenter' in raw_df.columns and 'Learning Pathway' in raw_df.columns:
                df = process_training_data(raw_df)
            else:
                st.error("CSV must contain 'Name', 'Instructor/Presenter', and 'Learning Pathway' columns")
                df = load_demo_data()
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            df = load_demo_data()
    else:
        st.info("Please upload a CSV file or select another data source.")
        df = load_demo_data()
else:
    df = load_demo_data()

# Filter Section
st.markdown("### 🔍 Search and Filter Training Sessions")
with st.container():
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        # Search box
        search_term = st.text_input("🔎 Search by name or instructor", placeholder="Type to search...")
        
    with col2:
        # Exposure level filter
        exposure_options = ["All"] + sorted(df['original_exposure'].unique().tolist())
        selected_exposure = st.selectbox("👥 Filter by Audience Level", exposure_options)
        
    with col3:
        # Specificity filter
        specificity_options = ["All"] + sorted(df['original_specificity'].unique().tolist())
        selected_specificity = st.selectbox("🎯 Filter by Specificity", specificity_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply search filter
    if search_term:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_term, case=False, na=False) |
            filtered_df['instructor'].str.contains(search_term, case=False, na=False) |
            filtered_df['description'].str.contains(search_term, case=False, na=False)
        ]
    
    # Apply exposure filter
    if selected_exposure != "All":
        filtered_df = filtered_df[filtered_df['original_exposure'] == selected_exposure]
    
    # Apply specificity filter
    if selected_specificity != "All":
        filtered_df = filtered_df[filtered_df['original_specificity'] == selected_specificity]
    
    st.markdown('</div>', unsafe_allow_html=True)

# Show filter results
if search_term or selected_exposure != "All" or selected_specificity != "All":
    st.info(f"Showing {len(filtered_df)} training sessions matching your filters")

# Pathway selector
st.markdown("### 🎯 Select Learning Pathways to Display")
col1, col2, col3, col4 = st.columns(4)

selected_pathways = {}
with col1:
    selected_pathways["Engineering"] = st.checkbox("Engineering", value=True)
with col2:
    selected_pathways["Operation"] = st.checkbox("Operation", value=True)
with col3:
    selected_pathways["Research"] = st.checkbox("Research", value=True)
with col4:
    selected_pathways["Education"] = st.checkbox("Education", value=True)

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

# Add course nodes from filtered DataFrame
for _, course in filtered_df.iterrows():
    if selected_pathways.get(course['pathway'], False):
        # Add hover text
        hover_text = f"<b>{course['name']}</b><br>Instructor: {course['instructor']}<br>Pathway: {course['pathway']}<br>Audience: {course['original_exposure']}<br>Type: {course['original_specificity']}"
        
        fig.add_trace(go.Scatter(
            x=[course['x']],
            y=[course['y']],
            mode="markers+text",
            marker=dict(
                size=20,
                color=pathways[course['pathway']]["color"],
                line=dict(color="white", width=2)
            ),
            text=[course['course_id']],
            textposition="middle center",
            textfont=dict(color="white", size=8, family="Arial Bold"),
            name=course['pathway'],
            showlegend=False,
            hovertext=hover_text,
            hoverinfo="text"
        ))

# Update layout
fig.update_layout(
    title="AI Training Offers Learning Pathway Network",
    xaxis=dict(
        title="Specificity →",
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=["Ideas", "Hands-on", "Issue Specific"],
        range=[-0.8, 2.8],
        showgrid=False
    ),
    yaxis=dict(
        title="← Audience Experience Level",
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
        course_count = len(filtered_df[filtered_df['pathway'] == pathway])
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 20px; height: 20px; border-radius: 50%; background-color: {style["color"]}; border: 2px solid #333;"></div>
            <span style="font-weight: 500;">{pathway} ({course_count} sessions)</span>
        </div>
        """, unsafe_allow_html=True)

# Summary statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sessions", len(filtered_df))
with col2:
    st.metric("Active Pathways", sum(selected_pathways.values()))
with col3:
    active_courses = len(filtered_df[filtered_df['pathway'].isin([p for p, sel in selected_pathways.items() if sel])])
    st.metric("Visible Sessions", active_courses)
with col4:
    unique_instructors = len(filtered_df['instructor'].unique())
    st.metric("Instructors", unique_instructors)

# Display selected courses in tabs
if any(selected_pathways.values()):
    tab_names = [p for p, selected in selected_pathways.items() if selected]
    tabs = st.tabs(tab_names)
    
    for i, pathway in enumerate(tab_names):
        with tabs[i]:
            pathway_courses = filtered_df[filtered_df['pathway'] == pathway].sort_values(['exposure', 'specificity'])
            
            for _, course in pathway_courses.iterrows():
                with st.expander(f"**{course['name']}** - {course['instructor']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Training ID:** {course['course_id']}")
                        st.write(f"**Instructor/Presenter:** {course['instructor']}")
                        st.write(f"**Audience Level:** {course['original_exposure']}")
                        st.write(f"**Training Type:** {course['original_specificity']}")
                        st.write(f"**Learning Pathway:** {course['pathway']}")
                        st.write("**Description:**")
                        st.write(course['description'])
                    
                    with col2:
                        st.selectbox(
                            "Select delivery format:",
                            ["Online Self-Paced", "Virtual Instructor-Led", "In-Person Workshop", "Hybrid"],
                            key=f"format_{course['course_id']}"
                        )
                        
                        if st.button("Register Interest", key=f"register_{course['course_id']}", use_container_width=True):
                            st.success(f"Interest registered for: {course['name']}")

# Instructions
st.markdown("---")
st.markdown("### 📖 How to Use This Training Pathway")
st.markdown("""
1. **Search & Filter**: Use the search box to find specific training sessions by name, instructor, or description
2. **Filter by Level**: Choose audience experience level and training specificity to narrow down options
3. **Select Pathways**: Use the checkboxes to display different learning pathways (Engineering, Operation, Research, Education)
4. **Explore Sessions**: Hover over nodes in the network to see detailed training information
5. **Session Details**: Click on the pathway tabs below to see complete session information and register interest

**Training Pathways:**
- 🔴 **Engineering**: Technical development, programming, and AI system building
- 🔵 **Operation**: Administrative, workflow, and operational AI applications  
- 🟢 **Research**: Academic research, methodology, and theoretical AI concepts
- 🟣 **Education**: Teaching, curriculum development, and educational AI applications

**Audience Experience Levels:**
- **Lv. 1 - Never used AI**: Beginner level, no prior AI experience
- **Lv. 2 - Sometimes use AI**: Intermediate level, occasional AI usage
- **Lv. 3 - Use AI on a daily basis**: Advanced level, regular AI users
- **Lv. Anyone**: Suitable for all experience levels

**Training Types:**
- **Lv.1 - Ideas**: Conceptual understanding and awareness
- **Lv.2 - Hands On**: Practical application and skills
- **Lv.3 - Issue Specific**: Targeted solutions for specific problems
""")

# Footer
st.markdown("---")
st.info("💡 **Note**: Training sessions are organized by the Learning Pathway specified in your CSV file. Hover over any node to see session details!")
