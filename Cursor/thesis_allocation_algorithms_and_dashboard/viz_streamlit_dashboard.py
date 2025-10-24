"""
Thesis Allocation System - Interactive Streamlit Dashboard
Provides real-time visualization and configuration of thesis allocations.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import json
from io import StringIO

# Import from allocator
from allocator.data_repository import DataRepository
from allocator.preference_model import PreferenceModel
from allocator.allocation_model_ilp import AllocationModelILP, AllocationConfig as LegacyAllocationConfig
from allocator.allocation_model_flow import AllocationModelFlow
from allocator.config import AllocationConfig, PreferenceConfig, CapacityConfig, SolverConfig
from allocator.validation import InputValidator
from allocator.logging_config import setup_logging


# Set page config
st.set_page_config(
    page_title="Thesis Allocation Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        color: #0066cc;
        font-weight: bold;
        margin-bottom: 1em;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5em;
        border-radius: 0.5em;
        border-left: 5px solid #0066cc;
    }
    .success-color { color: #00cc00; }
    .warning-color { color: #ff9900; }
    .error-color { color: #cc0000; }
</style>
""", unsafe_allow_html=True)


# Initialize session state for file persistence
if 'uploaded_students' not in st.session_state:
    st.session_state.uploaded_students = None
if 'uploaded_capacities' not in st.session_state:
    st.session_state.uploaded_capacities = None
if 'uploaded_overrides' not in st.session_state:
    st.session_state.uploaded_overrides = None
if 'last_allocation' not in st.session_state:
    st.session_state.last_allocation = None
if 'last_summary' not in st.session_state:
    st.session_state.last_summary = None


def download_combined_results(allocation_df, summary_text):
    """Create download options for allocation results."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        csv_data = allocation_df.to_csv(index=False)
        st.download_button(
            "📥 Allocation CSV",
            csv_data,
            "allocation_result.csv",
            "text/csv"
        )
    
    with col2:
        st.download_button(
            "📥 Summary TXT",
            summary_text,
            "allocation_summary.txt",
            "text/plain"
        )
    
    with col3:
        # Combined download as both CSV + TXT (separate files)
        import zipfile
        import io
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("allocation.csv", allocation_df.to_csv(index=False))
            zip_file.writestr("summary.txt", summary_text)
        
        zip_buffer.seek(0)
        st.download_button(
            "📦 Both as ZIP",
            zip_buffer.getvalue(),
            "allocation_results.zip",
            "application/zip"
        )
    
    with col4:
        st.write("")  # Placeholder for alignment


def create_preference_satisfaction_chart(summary_data):
    """Create preference satisfaction visualization."""
    if "Ranked choice satisfaction:" not in summary_data:
        return None
    
    # Parse ranked satisfaction
    lines = summary_data.split('\n')
    satisfaction = {}
    in_ranked = False
    for line in lines:
        if "Ranked choice satisfaction:" in line:
            in_ranked = True
        elif in_ranked and ':' in line and not line.startswith('  Unranked'):
            parts = line.strip().split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                try:
                    value = int(parts[1].strip())
                    satisfaction[key] = value
                except:
                    pass
        elif in_ranked and line.strip() == "":
            break
    
    if satisfaction:
        fig = px.bar(
            x=list(satisfaction.keys()),
            y=list(satisfaction.values()),
            title="Preference Satisfaction (Ranked Choices)",
            labels={"x": "Choice Rank", "y": "Number of Students"},
            color=list(satisfaction.values()),
            color_continuous_scale="Viridis"
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    return None


def create_capacity_utilization_chart(summary_data):
    """Create topic capacity utilization visualization."""
    if "Topic utilization:" not in summary_data:
        return None
    
    # Parse topic utilization
    lines = summary_data.split('\n')
    topics = {}
    in_util = False
    for line in lines:
        if "Topic utilization:" in line:
            in_util = True
        elif in_util and ':' in line and line.startswith('  topic'):
            parts = line.strip().split(':')[1].split('/')
            if len(parts) == 2:
                topic_name = line.split(':')[0].strip()
                used = int(parts[0].strip())
                total = int(parts[1].strip())
                topics[topic_name] = {'used': used, 'total': total, 'pct': (used/total*100) if total > 0 else 0}
        elif in_util and line.strip() == "" and topics:
            break
    
    if topics:
        df = pd.DataFrame(topics).T
        fig = px.bar(
            df,
            x=df.index,
            y=['used', 'total'],
            title="Topic Capacity Utilization",
            labels={"index": "Topic", "value": "Number of Students"},
            barmode="overlay",
            color_discrete_map={"used": "#0066cc", "total": "#cccccc"}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        return fig
    return None


def create_department_distribution_chart(summary_data):
    """Create department distribution visualization."""
    if "Department totals:" not in summary_data:
        return None
    
    lines = summary_data.split('\n')
    departments = {}
    in_dept = False
    for line in lines:
        if "Department totals:" in line:
            in_dept = True
        elif in_dept and ':' in line and line.startswith('  department'):
            parts = line.split(':')
            if len(parts) >= 2:
                dept_name = parts[0].strip()
                try:
                    count = int(parts[1].split('(')[0].strip())
                    departments[dept_name] = count
                except:
                    pass
        elif in_dept and line.strip() == "" and departments:
            break
    
    if departments:
        fig = px.pie(
            values=list(departments.values()),
            names=list(departments.keys()),
            title="Student Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        return fig
    return None


def create_allocation_summary_metrics(allocation_df, summary_data):
    """Create summary metrics from allocation results."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_students = len(allocation_df)
        st.metric(
            "Total Students Assigned",
            total_students,
            delta=None,
            delta_color="off"
        )
    
    with col2:
        first_choice = len(allocation_df[allocation_df['preference_rank'].between(10, 14)])
        pct = (first_choice / total_students * 100) if total_students > 0 else 0
        st.metric(
            "Got Ranked Choice",
            f"{first_choice}",
            delta=f"{pct:.1f}%"
        )
    
    with col3:
        if "Objective:" in summary_data:
            objective = summary_data.split("Objective:")[1].split('\n')[0].strip()
            st.metric(
                "Optimal Cost",
                objective,
                delta=None,
                delta_color="off"
            )
    
    with col4:
        unassigned = summary_data.count("Unassigned after solve: 0")
        status = "✓ All Assigned" if unassigned > 0 else "⚠ Some Unassigned"
        st.metric(
            "Assignment Status",
            status,
            delta=None,
            delta_color="off"
        )


def main():
    """Main Streamlit app."""
    st.markdown('<div class="main-header">🎓 Thesis Allocation Dashboard</div>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["🏠 Home", "⚙️ Configuration", "🚀 Run Allocation", "📊 Results Analysis", "🔍 Data Explorer", "📈 Advanced Charts"]
    )
    
    # Home Page
    if page == "🏠 Home":
        st.header("Welcome to the Thesis Allocation System")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📖 About")
            st.write("""
            This interactive dashboard allows you to:
            - Configure thesis allocation parameters
            - Upload student preferences and topic data
            - Run allocations with different algorithms
            - Analyze results with rich visualizations
            - Export allocation results
            """)
        
        with col2:
            st.subheader("🚀 Quick Start")
            st.write("""
            1. Go to **Configuration** to set parameters
            2. Upload CSV files with students and capacities
            3. Click **Run Allocation**
            4. View results in **Results Analysis**
            5. Explore data in **Data Explorer**
            """)
        
        st.divider()
        
        st.subheader("📂 File Management")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Load Sample Data:**")
            if st.button("📥 Load Default Data", key="load_default"):
                st.session_state.students_file = Path("data/input/students.csv")
                st.session_state.capacities_file = Path("data/input/capacities.csv")
                st.success("Default data loaded!")
        
        with col2:
            st.write("**Upload Custom Data:**")
            students_upload = st.file_uploader("Students CSV", type=['csv'], key="students_upload")
            capacities_upload = st.file_uploader("Capacities CSV", type=['csv'], key="capacities_upload")
    
    # Configuration Page
    elif page == "⚙️ Configuration":
        st.header("⚙️ Configuration")
        st.info("""
        📋 **Configuration Guide:**
        These settings control how the allocation algorithm behaves. 
        Adjust them to prioritize different outcomes (fairness, speed, preference satisfaction, etc.)
        """)
        
        st.subheader("Preference Settings")
        st.markdown("*How to value different preference levels*")
        col1, col2 = st.columns(2)
        
        with col1:
            allow_unranked = st.checkbox(
                "Allow Unranked Topics", 
                value=True,
                help="If OFF: Students MUST get a ranked preference. If ON: Can be assigned to any topic."
            )
            tier2_cost = st.slider(
                "Tier 2 Cost", 
                0, 10, 1,
                help="Penalty for assigning to a Tier 2 preference (lower = better). Default: 1"
            )
            tier3_cost = st.slider(
                "Tier 3 Cost", 
                0, 20, 5,
                help="Penalty for assigning to a Tier 3 preference (lower = better). Default: 5"
            )
        
        with col2:
            unranked_cost = st.slider(
                "Unranked Cost", 
                0, 500, 200,
                help="Penalty for assigning to an unranked topic (very high = avoid if possible). Default: 200"
            )
            top2_bias = st.checkbox(
                "Apply Top-2 Bias", 
                value=True,
                help="If ON: Strongly prefer 1st & 2nd choices. If OFF: All ranks treated equally."
            )
        
        st.divider()
        st.subheader("Capacity Settings")
        st.markdown("*How to handle capacity constraints*")
        col1, col2 = st.columns(2)
        
        with col1:
            enable_topic_overflow = st.checkbox(
                "Enable Topic Overflow", 
                value=True,
                help="If ON: Topics can exceed capacity (with penalty). If OFF: Hard cap on topics."
            )
            enable_coach_overflow = st.checkbox(
                "Enable Coach Overflow", 
                value=True,
                help="If ON: Coaches can exceed capacity (with penalty). If OFF: Hard cap on coaches."
            )
            dept_min_mode = st.selectbox(
                "Department Min Mode", 
                ["soft", "hard"],
                help="'soft' = Try but don't require minimums. 'hard' = Enforce department minimums strictly."
            )
        
        with col2:
            P_dept_shortfall = st.slider(
                "Dept Shortfall Penalty", 
                0, 5000, 1000,
                help="Penalty when department minimum not met (higher = stricter enforcement). Default: 1000"
            )
            P_topic = st.slider(
                "Topic Overflow Penalty", 
                0, 2000, 800,
                help="Penalty when topic exceeds capacity (higher = stricter). Default: 800"
            )
            P_coach = st.slider(
                "Coach Overflow Penalty", 
                0, 2000, 600,
                help="Penalty when coach exceeds capacity (higher = stricter). Default: 600"
            )
        
        st.markdown("💡 **Tip**: Higher penalties = stricter constraints = slower solving but fairer results")
        
        st.divider()
        st.subheader("Solver Settings")
        st.markdown("*Algorithm selection and optimization parameters*")
        col1, col2 = st.columns(2)
        
        with col1:
            algorithm = st.selectbox(
                "Algorithm", 
                ["ilp", "flow", "hybrid"],
                help="""
                • 'ilp' = Optimal solution (slow, up to 2 min)
                • 'flow' = Fast approximate solution (seconds)
                • 'hybrid' = ILP verified with flow (balanced)
                """
            )
            time_limit = st.slider(
                "Time Limit (seconds)", 
                0, 600, 60,
                help="Max time solver can spend. 0 = no limit. Higher = better results but slower."
            )
        
        with col2:
            random_seed = st.number_input(
                "Random Seed", 
                value=None, 
                min_value=0,
                help="Same seed = same results (for reproducibility). Leave empty for random."
            )
            epsilon = st.slider(
                "Epsilon Suboptimal", 
                0.0, 1.0, 0.0, 0.05,
                help="Allow solutions within X% of optimal (e.g., 0.05 = 5% worse but faster). Default: 0 (optimal only)"
            )
        
        st.markdown("💡 **Quick presets:**")
        st.markdown("""
        - **Fast**: flow, 10-30 sec, results in seconds
        - **Balanced**: hybrid, 60 sec, good quality & speed
        - **Optimal**: ilp, 300 sec, best results
        """)
        
        # Save config
        st.divider()
        if st.button("💾 Save Configuration"):
            config = AllocationConfig(
                preference=PreferenceConfig(
                    allow_unranked=allow_unranked,
                    tier2_cost=tier2_cost,
                    tier3_cost=tier3_cost,
                    unranked_cost=unranked_cost,
                    top2_bias=top2_bias
                ),
                capacity=CapacityConfig(
                    enable_topic_overflow=enable_topic_overflow,
                    enable_coach_overflow=enable_coach_overflow,
                    dept_min_mode=dept_min_mode,
                    P_dept_shortfall=P_dept_shortfall,
                    P_topic=P_topic,
                    P_coach=P_coach
                ),
                solver=SolverConfig(
                    algorithm=algorithm,
                    time_limit_sec=time_limit if time_limit > 0 else None,
                    random_seed=random_seed if random_seed and random_seed > 0 else None,
                    epsilon_suboptimal=epsilon if epsilon > 0 else None
                )
            )
            config.save_json("config_streamlit.json")
            st.success("✓ Configuration saved to config_streamlit.json")
    
    # Run Allocation Page
    elif page == "🚀 Run Allocation":
        st.header("🚀 Run Allocation")
        st.write("Run thesis allocation directly from the dashboard with live progress tracking.")
        
        col1, col2 = st.columns(2)
        
        # File uploads
        with col1:
            st.subheader("📥 Input Files")
            students_file = st.file_uploader(
                "Students CSV",
                type=['csv'],
                key="run_students",
                help="CSV with student preferences"
            )
            capacities_file = st.file_uploader(
                "Capacities CSV",
                type=['csv'],
                key="run_capacities",
                help="CSV with topic/coach capacities"
            )
            overrides_file = st.file_uploader(
                "Overrides CSV (Optional)",
                type=['csv'],
                key="run_overrides",
                help="Optional: CSV with manual cost overrides"
            )
        
        with col2:
            st.subheader("⚙️ Algorithm Settings")
            run_algorithm = st.selectbox(
                "Algorithm",
                ["ilp", "flow", "hybrid"],
                key="run_algorithm"
            )
            run_time_limit = st.slider(
                "Time Limit (seconds)",
                0, 600, 60,
                key="run_time_limit"
            )
            run_seed = st.number_input(
                "Random Seed (optional)",
                value=None,
                min_value=0,
                key="run_seed"
            )
        
        st.divider()
        
        # Validation section
        if students_file and capacities_file:
            st.subheader("✓ Validation")
            col1, col2 = st.columns(2)
            
            with col1:
                students_df = pd.read_csv(students_file)
                st.write(f"**Students:** {len(students_df)} records")
                st.write(f"**Columns:** {', '.join(students_df.columns.tolist()[:5])}")
            
            with col2:
                capacities_df = pd.read_csv(capacities_file)
                st.write(f"**Capacities:** {len(capacities_df)} records")
                st.write(f"**Columns:** {', '.join(capacities_df.columns.tolist()[:5])}")
            
            st.divider()
            
            # Run button with status
            if st.button("▶️ Run Allocation", key="run_btn", type="primary"):
                with st.spinner("🔄 Running allocation..."):
                    try:
                        # Save uploaded files temporarily
                        import tempfile
                        from pathlib import Path
                        
                        with tempfile.TemporaryDirectory() as tmpdir:
                            students_path = Path(tmpdir) / "students.csv"
                            capacities_path = Path(tmpdir) / "capacities.csv"
                            output_path = Path(tmpdir) / "allocation.csv"
                            summary_path = Path(tmpdir) / "summary.txt"
                            
                            # Write files
                            students_path.write_text(students_file.getvalue().decode())
                            capacities_path.write_text(capacities_file.getvalue().decode())
                            
                            # Load data
                            st.info("📂 Loading data...")
                            repo = DataRepository(
                                str(students_path),
                                str(capacities_path),
                                str(Path(tmpdir) / "overrides.csv") if overrides_file else None
                            )
                            if overrides_file:
                                (Path(tmpdir) / "overrides.csv").write_text(overrides_file.getvalue().decode())
                            repo.load()
                            
                            st.info(f"✓ Loaded {len(repo.students)} students, {len(repo.topics)} topics")
                            
                            # Validate
                            st.info("🔍 Validating data...")
                            validator = InputValidator()
                            is_valid, validation_results = validator.validate_all(
                                repo.students, repo.topics, repo.coaches, repo.departments
                            )
                            
                            if not is_valid:
                                st.error("❌ Validation failed!")
                                for result in validation_results:
                                    if result.severity == "error":
                                        st.error(str(result))
                            else:
                                st.success("✓ Validation passed")
                                
                                # Build preference model
                                st.info("🎯 Building preference model...")
                                pref_model = PreferenceModel(
                                    topics=repo.topics,
                                    overrides=repo.overrides,
                                    cfg=PreferenceConfig()
                                )
                                
                                # Create allocation config
                                legacy_cfg = LegacyAllocationConfig(
                                    pref_cfg=PreferenceConfig(),
                                    dept_min_mode="soft",
                                    enable_topic_overflow=True,
                                    enable_coach_overflow=True,
                                    P_dept_shortfall=1000,
                                    P_topic=800,
                                    P_coach=600,
                                    time_limit_sec=run_time_limit if run_time_limit > 0 else None,
                                    random_seed=run_seed if run_seed and run_seed > 0 else None,
                                    epsilon_suboptimal=None
                                )
                                
                                # Build model
                                st.info(f"🔨 Building {run_algorithm.upper()} model...")
                                if run_algorithm == "ilp":
                                    model = AllocationModelILP(
                                        students=repo.students,
                                        topics=repo.topics,
                                        coaches=repo.coaches,
                                        departments=repo.departments,
                                        pref_model=pref_model,
                                        cfg=legacy_cfg
                                    )
                                elif run_algorithm == "flow":
                                    model = AllocationModelFlow(
                                        students=repo.students,
                                        topics=repo.topics,
                                        coaches=repo.coaches,
                                        departments=repo.departments,
                                        pref_model=pref_model,
                                        cfg=legacy_cfg
                                    )
                                else:  # hybrid
                                    model = AllocationModelILP(
                                        students=repo.students,
                                        topics=repo.topics,
                                        coaches=repo.coaches,
                                        departments=repo.departments,
                                        pref_model=pref_model,
                                        cfg=legacy_cfg
                                    )
                                
                                # Solve
                                st.info("⚡ Solving...")
                                model.build()
                                rows, diagnostics = model.solve()
                                
                                # Results
                                st.success("✅ Allocation complete!")
                                
                                # Display results
                                st.divider()
                                st.subheader("📊 Results")
                                
                                # Metrics
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Students Assigned", len(rows))
                                with col2:
                                    obj_value = diagnostics.get("objective_value", "N/A")
                                    st.metric("Optimal Cost", obj_value)
                                with col3:
                                    first_choice = len([r for r in rows if 10 <= r.preference_rank <= 14])
                                    pct = (first_choice / len(rows) * 100) if rows else 0
                                    st.metric("Got Choice %", f"{pct:.1f}%")
                                with col4:
                                    status = "✓ Success" if diagnostics.get("unassigned_after_solve", 1) == 0 else "⚠ Partial"
                                    st.metric("Status", status)
                                
                                # Explain status
                                st.info("""
                                📌 **Status Explanation:**
                                • **✓ Success**: All students were successfully assigned to a topic
                                • **⚠ Partial**: Some students could NOT be assigned (constraints too tight)
                                  - Check if topic/coach capacity is exceeded
                                  - Try enabling "Topic Overflow" or "Coach Overflow"
                                  - Or relax "Department Min Mode" to "soft"
                                """)
                                
                                # Allocation table
                                st.divider()
                                st.subheader("📋 Allocation Details")
                                allocation_df = pd.DataFrame([
                                    {
                                        'student': row.student,
                                        'assigned_topic': row.assigned_topic,
                                        'assigned_coach': row.assigned_coach,
                                        'department_id': row.department_id,
                                        'preference_rank': row.preference_rank,
                                        'effective_cost': row.effective_cost
                                    }
                                    for row in rows
                                ])
                                st.dataframe(allocation_df, use_container_width=True)
                                
                                # Create summary text
                                summary_text = f"""ALLOCATION RESULTS
==================

Algorithm: {run_algorithm.upper()}
Time Limit: {run_time_limit} seconds
Total Students: {len(rows)}
Objective Value: {diagnostics.get('objective_value', 'N/A')}

Status: {'✓ All assigned' if diagnostics.get('unassigned_after_solve', 0) == 0 else '⚠ Some unassigned'}

Assignment Details:
- Preference Rank 10-14 (ranked choices): {len([r for r in rows if 10 <= r.preference_rank <= 14])}
- Preference Rank 0-2 (tier preferences): {len([r for r in rows if 0 <= r.preference_rank <= 2])}
- Preference Rank 999 (unranked): {len([r for r in rows if r.preference_rank == 999])}
- Forced assignments (rank -1): {len([r for r in rows if r.preference_rank == -1])}

Diagnostics:
{str(diagnostics)}
"""
                                
                                # Download buttons
                                st.divider()
                                download_combined_results(allocation_df, summary_text)
                                
                                # Store in session for Results Analysis
                                st.session_state.last_allocation = allocation_df
                                st.session_state.last_summary = summary_text
                                
                                st.info("💡 Go to 📊 Results Analysis to view visualizations!")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        st.error(traceback.format_exc())
        else:
            st.warning("👆 Upload both students.csv and capacities.csv files to begin")
    
    # Results Analysis Page
    elif page == "📊 Results Analysis":
        st.header("📊 Results Analysis")
        st.info("""
        📈 **How to interpret these visualizations:**
        - **Key Metrics**: Quick overview of allocation quality
        - **Preference Chart**: Shows how many students got their ranked choices
        - **Department Pie**: Shows student distribution across departments
        - **Capacity Bars**: Shows how full each topic is vs its capacity
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📥 Input Files")
            students_file = st.file_uploader("Students CSV", type=['csv'], key="results_students")
            capacities_file = st.file_uploader("Capacities CSV", type=['csv'], key="results_capacities")
        
        with col2:
            st.subheader("📤 Allocation Results")
            allocation_file = st.file_uploader("Allocation CSV", type=['csv'], key="results_allocation")
            summary_file = st.file_uploader("Summary TXT", type=['txt'], key="results_summary")
        
        if allocation_file and summary_file:
            # Load data
            allocation_df = pd.read_csv(allocation_file)
            summary_text = summary_file.read().decode("utf-8")
            
            # Display summary metrics
            st.divider()
            st.subheader("📊 Key Metrics")
            create_allocation_summary_metrics(allocation_df, summary_text)
            
            # Display charts
            st.divider()
            st.subheader("📈 Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_preference_satisfaction_chart(summary_text)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_department_distribution_chart(summary_text)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            fig = create_capacity_utilization_chart(summary_text)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Allocation details table
            st.divider()
            st.subheader("📋 Allocation Details")
            st.dataframe(allocation_df, use_container_width=True)
            
            # Download results
            st.divider()
            st.subheader("📥 Download Results")
            download_combined_results(allocation_df, summary_text)
    
    # Data Explorer Page
    elif page == "🔍 Data Explorer":
        st.header("🔍 Data Explorer")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📊 Students")
            students_file = st.file_uploader("Upload Students CSV", type=['csv'], key="explorer_students")
            if students_file:
                df = pd.read_csv(students_file)
                st.write(f"**Total Students:** {len(df)}")
                st.dataframe(df.head(10), use_container_width=True)
        
        with col2:
            st.subheader("🎯 Topics")
            capacities_file = st.file_uploader("Upload Capacities CSV", type=['csv'], key="explorer_capacities")
            if capacities_file:
                df = pd.read_csv(capacities_file)
                st.write(f"**Total Topics:** {len(df)}")
                st.dataframe(df.head(10), use_container_width=True)
        
        with col3:
            st.subheader("👥 Coaches")
            if capacities_file:
                df = pd.read_csv(capacities_file)
                coaches_df = df[['coach_id', 'maximum students per coach']].drop_duplicates('coach_id')
                st.write(f"**Total Coaches:** {len(coaches_df)}")
                st.dataframe(coaches_df.head(10), use_container_width=True)
    
    # Advanced Charts Page
    elif page == "📈 Advanced Charts":
        st.header("📈 Advanced Charts")
        
        st.info("""
        🔍 **Advanced Visualizations:**
        - **Sankey Diagram**: Flow from Students → Topics → Coaches → Departments (colored by preference rank)
        - **Network Flow**: Network graph showing allocations as connections
        - **Cost Matrix**: Heatmap of costs for student-topic pairs
        - **Statistics**: Histograms of costs and preference ranks
        """)
        
        # Sankey Visualization
        st.divider()
        st.subheader("🌊 Sankey Diagram (Student → Topic → Coach → Department)")
        st.write("Shows the flow of allocations with colors representing preference satisfaction (green=good, red=bad)")
        
        sankey_file = st.file_uploader("Allocation CSV for Sankey", type=['csv'], key="sankey_alloc")
        if sankey_file:
            try:
                import tempfile
                from pathlib import Path
                
                # Write uploaded file to temp location
                with tempfile.TemporaryDirectory() as tmpdir:
                    temp_csv = Path(tmpdir) / "temp_allocation.csv"
                    temp_csv.write_text(sankey_file.getvalue().decode())
                    
                    # Import and run Sankey generator
                    from viz_sankey_enhanced import load_allocation, create_sankey_html
                    
                    rows = load_allocation(str(temp_csv))
                    sankey_html = create_sankey_html(rows)
                    
                    # Display as HTML
                    st.components.v1.html(sankey_html, height=800, scrolling=True)
                    st.success("✓ Sankey diagram generated successfully!")
            except Exception as e:
                st.warning(f"⚠️ Could not generate Sankey diagram: {str(e)}")
        
        st.divider()
        
        # Network Flow Visualization
        st.subheader("🕸️ Network Flow Graph")
        st.write("Shows the network structure of allocations (Students ↔ Topics ↔ Coaches ↔ Departments)")
        
        network_file = st.file_uploader("Allocation CSV for Network", type=['csv'], key="network_alloc")
        if network_file:
            try:
                import tempfile
                from pathlib import Path
                
                # Write uploaded file to temp location
                with tempfile.TemporaryDirectory() as tmpdir:
                    temp_csv = Path(tmpdir) / "temp_allocation.csv"
                    temp_csv.write_text(network_file.getvalue().decode())
                    
                    # Import and run Network visualization
                    from viz_network_flow import load_allocation, create_network_visualization
                    
                    rows = load_allocation(str(temp_csv))
                    network_html = create_network_visualization(rows)
                    
                    # Display as HTML
                    st.components.v1.html(network_html, height=800, scrolling=True)
                    st.success("✓ Network flow diagram generated successfully!")
            except Exception as e:
                st.warning(f"⚠️ Could not generate network diagram: {str(e)}")
        
        st.divider()
        
        # Cost Heatmap
        st.subheader("🔥 Cost Matrix Heatmap")
        st.write("Shows effective cost for each student-topic pair (darker red = higher cost/worse fit)")
        
        allocation_file = st.file_uploader("Allocation CSV for Heatmap", type=['csv'], key="heatmap_alloc")
        
        if allocation_file:
            try:
                df = pd.read_csv(allocation_file)
                
                # Create a pivot table for costs
                if 'effective_cost' in df.columns and 'student' in df.columns and 'assigned_topic' in df.columns:
                    # Sample for visualization (limit to first 50 students and 15 topics)
                    sample_df = df.head(50)
                    
                    cost_pivot = sample_df.pivot_table(
                        values='effective_cost',
                        index='student',
                        columns='assigned_topic',
                        fill_value=0
                    )
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=cost_pivot.values,
                        x=cost_pivot.columns,
                        y=cost_pivot.index,
                        colorscale='RdYlGn_r'
                    ))
                    fig.update_layout(
                        title="Effective Cost Heatmap (Student × Topic)",
                        height=600,
                        xaxis_title="Topic",
                        yaxis_title="Student"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Required columns not found. Need: 'student', 'assigned_topic', 'effective_cost'")
            except Exception as e:
                st.warning(f"⚠️ Could not generate heatmap: {str(e)}")
        
        st.divider()
        st.subheader("📊 Summary Statistics")
        st.write("Histograms showing distribution of costs and preference ranks")
        
        stats_file = st.file_uploader("Allocation CSV for Statistics", type=['csv'], key="stats_alloc")
        
        if stats_file:
            try:
                df = pd.read_csv(stats_file)
                
                if df.empty:
                    st.warning("⚠️ Allocation file is empty. Cannot generate statistics.")
                else:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Cost Distribution**")
                        if 'effective_cost' in df.columns:
                            fig = px.histogram(
                                df,
                                x='effective_cost',
                                nbins=30,
                                title="Distribution of Effective Costs",
                                labels={"effective_cost": "Cost", "count": "Number of Students"}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("'effective_cost' column not found in allocation file")
                    
                    with col2:
                        st.write("**Preference Rank Distribution**")
                        if 'preference_rank' in df.columns:
                            fig = px.histogram(
                                df,
                                x='preference_rank',
                                nbins=20,
                                title="Distribution of Preference Ranks",
                                labels={"preference_rank": "Preference Rank", "count": "Number of Students"}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("'preference_rank' column not found in allocation file")
            except pd.errors.EmptyDataError:
                st.error("❌ Error: The allocation file appears to be empty or corrupted.")
            except Exception as e:
                st.error(f"❌ Error reading allocation file: {str(e)}")


if __name__ == "__main__":
    main()
