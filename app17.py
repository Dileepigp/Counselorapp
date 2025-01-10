import streamlit as st
import pandas as pd
import os

# Load the data from the uploaded Excel file
file_path = r'C:\InGenius Prep\Counselor app\FAO and GC Information.xlsx'
fao_df = pd.read_excel(file_path, sheet_name='FAO')  # FAO sheet
gc_df = pd.read_excel(file_path, sheet_name='GC')    # GC sheet

fao_df.fillna("", inplace=True)
gc_df.fillna("", inplace=True)

fao_df.columns = fao_df.columns.str.strip()
gc_df.columns = gc_df.columns.str.strip()

# Load college rankings from the uploaded CSV file
college_rankings_file_path = r'C:\InGenius Prep\Counselor app\Colleges Rankings.csv'
college_rankings_df = pd.read_csv(college_rankings_file_path)

# Extract the list of colleges
Admission_experience_options = college_rankings_df['COLLEGE'].tolist()
# Admission_experience_options=['ABCD college']

incompatible_counselors = {
    'Hubert Mysliwiec': ['Will Fenton', 'Nick Strohl', 'Natalia Ostrowski', 'Heather McCutchen'],
    'Sam Heidepriem': ['Roscoe Nicholson'],
    'Kevin Covarrubias': ['Roscoe Nicholson', 'Claire Gumus'],
    'Robert Thomas': ['Roscoe Nicholson'],
    'Amy Greene': ['Zakaree Harris']
}
# Add professional icons for a more refined experience
fao_traits_options = [
    '🧠 Bubbly',
    '🎨 Creative',
    '📝 Detail-oriented',
    '➡️ Direct',
    '🧠 Energetic',
    '💪 Firm/strict',
    '🧠 Friend/sibling type',
    '🤝 Handholding',
    '📋 Organized',
    '🕊️ Patient',
    '🚀 Proactive',
    '🎓 Professor-type',
    '⚡ Responsive',
    '🤗 Sensitive/supportive',
    '🧠 Sporty',
    '🧠 Talkative/Chatty',
    '🔥 Warm'
]
subjects_options = [
    '📐 Applied Math',
    '🏛️ Architecture',
    '🧬 Biology',
    '💼 Business',
    '⚗️ Chemistry',
    '📖 Classics',
    '📢 Communication',
    '💻 Computer Science',
    '✍️ Creative Writing',
    '📊 Data Science',
    '💵 Economics',
    '🎓 Education',
    '🔧 Engineering',
    '📚 English',
    '🌿 Environmental Science',
    '🎥 Film',
    '🎨 Fine Arts',
    '📜 History',
    '🌍 Interdisciplinary',
    '🌐 International Relations',
    '⚖️ Law',
    '📚 Literature',
    '➗ Math',
    '📺 Media',
    '🩺 Medicine',
    '🧠 Neuroscience',
    '🎭 Performance',
    '🌌 Physics',
    '🏛️ Policy',
    '🗳️ Political Science',
    '🧠 Psychology',
    '🏥 Public Health',
    '🌎 Social Sciences',
    '📈 Statistics'
]
timezones_options = [
    '🌏 Asia',
    '🌏 Australia/NZ',
    '🌍 CST',
    '🌎 EST',
    '🌍 Europe',
    '🌍 MST',
    '🌍 PST'
]
degree_classification_options = ['🎓 PhD Degree', '🎓 Masters Degree', '🎓 Undergraduate Degree']

# Set up Streamlit page configuration
st.set_page_config(page_title="InGenius Prep - Counselor Matchmaking", page_icon="🔍", layout="wide")

# Styling and CSS
st.markdown("""
    <style>
        :root {
            --primary-color: #005CAA;
            --secondary-color: #4A90E2;
            --accent-color: #00A86B;
            --background-color: #F4F7FA;
            --card-background: #FFFFFF;
            --text-primary: #1A2B3C;
            --text-secondary: #4A5568;
            --border-radius: 12px;
            --box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .stApp {
            background-color: var(--background-color);
            font-family: 'Inter', 'Roboto', sans-serif;
        }

        h1, h2, h3 {
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 20px;
        }

        .profile-card {
            background: var(--card-background);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            margin-bottom: 15px;
            border-left: 5px solid var(--primary-color);
            transition: all 0.3s ease;
        }

        .profile-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }

        .stButton>button {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            text-transform: uppercase;
            border: none !important;
        }

        .stButton>button:hover {
            background-color: var(--secondary-color) !important;
            transform: scale(1.05);
        }

        .gradient-accent {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Logo and Title
st.markdown("""
    <div class="logo-container">
        <img src="https://ingeniusprep.com/wp-content/uploads/2023/09/Ingeniusprep-logo-1.png" alt="InGenius Prep Logo">
        <h1>Counselor Matchmaking Platform</h1>
        <div class="gradient-accent">
            Find Your Perfect Academic Guidance Partner
        </div>
    </div>
""", unsafe_allow_html=True)

# Step 1: Select Timezone
st.header("Step 1: Select Student's Timezone")
student_timezone = st.selectbox("Select the timezone of the student", timezones_options)

# Extract unique packages from the FAO and GC data
all_packages = set()
fao_df['Available Packages'].dropna().str.split(',').apply(all_packages.update)
gc_df['Available Packages'].dropna().str.split(',').apply(all_packages.update)

# Create a sorted list of unique packages
package_options = sorted(all_packages)

# Step 2: Select Package
st.header("Step 2: Select Desired Package")
selected_packages = st.multiselect("Select the package(s) of interest", package_options)

# Filter FAO and GC data based on the selected timezone and packages
student_timezone_cleaned = student_timezone.split(" ", 1)[1]  # Extract timezone abbreviation
fao_df = fao_df[fao_df['Available Timezones'].str.contains(student_timezone_cleaned, na=False)]
gc_df = gc_df[gc_df['Available Timezones'].str.contains(student_timezone_cleaned, na=False)]

if selected_packages:
    fao_df = fao_df[fao_df['Available Packages'].apply(lambda x: any(pkg in selected_packages for pkg in str(x).split(',')))]
    gc_df = gc_df[gc_df['Available Packages'].apply(lambda x: any(pkg in selected_packages for pkg in str(x).split(',')))]

# Helper function to create rank input
def rank_input(label, available_ranks, key=None):
    """Render a rank input with restricted options."""
    st.markdown(f"**{label}**")
    st.markdown('<span style="color: #757575; font-size: 0.9rem;">Choose a unique rank</span>', unsafe_allow_html=True)
    rank = st.selectbox(label, available_ranks, key=key)
    return rank

# Split Screen: FAO on the left, GC on the right
col1, col2 = st.columns([1, 1])

# Initialize session state for FAO and GC priority sections
if "show_fao_priority" not in st.session_state:
    st.session_state["show_fao_priority"] = False

if "show_gc_priority" not in st.session_state:
    st.session_state["show_gc_priority"] = False

# FAO Section
with col1:
    with st.expander("FAO Counselors Section", expanded=True):
        st.subheader("Preferences for FAO Counselors")
        fao_preferences = {
            'FAO Personality Traits': st.multiselect("Select preferred personality traits (FAO)", fao_traits_options, key="fao_traits"),
            'Subjects': st.multiselect("Select subjects of interest (FAO)", subjects_options, key="fao_subjects"),
            'Degree Classification': st.multiselect("Preferred degree classification (FAO)", degree_classification_options, key="fao_degree")
        }
        fao_experience_level = st.selectbox("Years of Experience (FAO)", ["Choose...", "1+", "2+", "3+", "4+", "5+"], key="fao_experience")
        fao_Admission_experience = st.multiselect(
            "Preferred Admission Results (FAO)", 
            Admission_experience_options, 
            key="fao_Admission"
        )

        # Button to show the assign priority section
        if st.button("Assign Priority for FAO"):
            st.session_state["show_fao_priority"] = True

    # Display FAO priority section in the same column
    if st.session_state["show_fao_priority"]:
        st.subheader("Assign Priority for FAO Preferences")
        fao_points = {}
        # Count non-empty categories, including Years of Experience and Admission Experience if selected
        num_categories = len([opts for opts in fao_preferences.values() if opts])
        if fao_experience_level != "Choose...":
            num_categories += 1
        if fao_Admission_experience:
            num_categories += 1

        available_ranks = list(range(1, num_categories + 1))

        for category, options in fao_preferences.items():
            if options:
                category_rank = rank_input(f"Rank for {category} (FAO)", available_ranks, key=f"fao_rank_{category}")
                available_ranks.remove(category_rank)
                for option in options:
                    clean_option = option.split(" ", 1)[1]
                    fao_points[f"{category}: {clean_option}"] = 10 * (num_categories + 1 - category_rank)

        if fao_experience_level != "Choose...":
            category_rank = rank_input(f"Rank for Years of Experience (FAO)", available_ranks, key="fao_experience_rank")
            available_ranks.remove(category_rank)
            fao_points[f"Experience: {fao_experience_level}"] = 10 * (num_categories + 1 - category_rank)

        if fao_Admission_experience:
            category_rank = rank_input(f"Rank for Admission Experience (FAO)", available_ranks, key="fao_Admission_rank")
            available_ranks.remove(category_rank)
            for exp in fao_Admission_experience:
                fao_points[f"Admission Experience: {exp}"] = 10 * (num_categories + 1 - category_rank)

        st.session_state['fao_points'] = fao_points

# GC Section
with col2:
    with st.expander("GC Counselors Section", expanded=True):
        st.subheader("Preferences for GC Counselors")
        gc_preferences = {
            'GC Personality Traits': st.multiselect("Select preferred personality traits (GC)", fao_traits_options, key="gc_traits"),
            'Subjects': st.multiselect("Select subjects of interest (GC)", subjects_options, key="gc_subjects"),
            'Degree Classification': st.multiselect("Preferred degree classification (GC)", degree_classification_options, key="gc_degree")
        }
        gc_experience_level = st.selectbox("Years of Experience (GC)", ["Choose...", "1+", "2+", "3+", "4+", "5+"], key="gc_experience")
        gc_Admission_experience = st.multiselect(
            "Preferred Admission Results (GC)", 
            Admission_experience_options, 
            key="gc_Admission"
        )

        # Button to show the assign priority section
        if st.button("Assign Priority for GC"):
            st.session_state["show_gc_priority"] = True

    # Display GC priority section in the same column
    if st.session_state["show_gc_priority"]:
        st.subheader("Assign Priority for GC Preferences")
        gc_points = {}
        # Count non-empty categories, including Years of Experience and Admission Experience if selected
        num_categories = len([opts for opts in gc_preferences.values() if opts])
        if gc_experience_level != "Choose...":
            num_categories += 1
        if gc_Admission_experience:
            num_categories += 1

        available_ranks = list(range(1, num_categories + 1))

        for category, options in gc_preferences.items():
            if options:
                category_rank = rank_input(f"Rank for {category} (GC)", available_ranks, key=f"gc_rank_{category}")
                available_ranks.remove(category_rank)
                for option in options:
                    clean_option = option.split(" ", 1)[1]
                    gc_points[f"{category}: {clean_option}"] = 10 * (num_categories + 1 - category_rank)

        if gc_experience_level != "Choose...":
            category_rank = rank_input(f"Rank for Years of Experience (GC)", available_ranks, key="gc_experience_rank")
            available_ranks.remove(category_rank)
            gc_points[f"Experience: {gc_experience_level}"] = 10 * (num_categories + 1 - category_rank)

        if gc_Admission_experience:
            category_rank = rank_input(f"Rank for Admission Experience (GC)", available_ranks, key="gc_Admission_rank")
            available_ranks.remove(category_rank)
            for exp in gc_Admission_experience:
                gc_points[f"Admission Experience: {exp}"] = 10 * (num_categories + 1 - category_rank)

        st.session_state['gc_points'] = gc_points


def calculate_score(df, points):
    def score_row(row):
        score = 0
        for option, weight in points.items():
            try:
                # Experience Points
                if option.startswith("Experience"):
                    exp_level = int(option.split(": ")[1].replace("+", ""))
                    if int(row['Experience']) >= exp_level:
                        score += weight
                
                # Admission Experience Points
                elif option.startswith("Admission Experience"):
                    Admission_experiences = row.get('Admission Experience', "")
                    if isinstance(Admission_experiences, str):
                        Admission_experiences = Admission_experiences.split(", ")
                    if option.split(": ")[1] in Admission_experiences:
                        score += weight
                
                # General Traits/Subjects
                else:
                    column, value = option.split(": ")
                    if value in row.get(column, ""):
                        score += weight
            except (KeyError, TypeError, ValueError):
                continue  # Skip invalid rows
        return score

    df["Score"] = df.apply(score_row, axis=1)
    return df


# Process counselor data
fao_df = calculate_score(fao_df, st.session_state.get('fao_points', {}))
gc_df = calculate_score(gc_df, st.session_state.get('gc_points', {}))



# Filter out incompatible pairs and resolve conflicts
def filter_incompatible_pairs(fao_df, gc_df):
    for gc_name, fao_names in incompatible_counselors.items():
        if gc_name in gc_df['Counselor Name'].values:
            gc_counselor = gc_df.loc[gc_df['Counselor Name'] == gc_name]
            gc_score = gc_counselor['Score'].values[0]
            for fao_name in fao_names:
                if fao_name in fao_df['Counselor Name'].values:
                    fao_counselor = fao_df.loc[fao_df['Counselor Name'] == fao_name]
                    fao_score = fao_counselor['Score'].values[0]
                    if gc_score > fao_score:
                        fao_df = fao_df[fao_df['Counselor Name'] != fao_name]
                    elif fao_score > gc_score or fao_score == gc_score:
                        gc_df = gc_df[gc_df['Counselor Name'] != gc_name]
                        break  # Only remove the GC if there's a strict resolution
    return fao_df, gc_df

fao_df, gc_df = filter_incompatible_pairs(fao_df, gc_df)

# Display top 3 counselors after filtering
fao_top_matches = fao_df.sort_values(by="Score", ascending=False).head(3)
gc_top_matches = gc_df.sort_values(by="Score", ascending=False).head(3)


# # Path to the Biocards folder
# biocards_folder = r'C:\InGenius Prep\Counselor app\Biocards'


# if st.button("Find Top Counselors"):
#     st.header("Top Counselor Matches")
#     col1, col2 = st.columns(2)

#     # Function to embed a PDF in an iframe
#     def display_pdf(folder_path, counselor_name):
#         # Locate the PDF file by matching the name
#         pdf_files = [f for f in os.listdir(folder_path) if f.startswith(counselor_name) and f.endswith(".pdf")]
#         if pdf_files:
#             file_path = os.path.join(folder_path, pdf_files[0])
#             with open(file_path, "rb") as pdf_file:
#                 pdf_data = pdf_file.read()
            
#             # Encode the PDF data to base64
#             import base64
#             pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            
#             # Create an iframe to display the PDF
#             pdf_display = f"""
#                 <iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500" style="border: none;"></iframe>
#             """
#             st.markdown(pdf_display, unsafe_allow_html=True)
#         else:
#             st.warning(f"PDF for {counselor_name} not found!")

#     # FAO Section
#     with col1:
#         st.subheader("Top FAO Matches")
#         for _, row in fao_top_matches.iterrows():
#             counselor_name = row['Counselor Name']
#             fao_folder = os.path.join(biocards_folder, 'FAO Biocards')
#             st.markdown(f"**{counselor_name}**")
#             display_pdf(fao_folder, counselor_name)

#     # GC Section
#     with col2:
#         st.subheader("Top GC Matches")
#         for _, row in gc_top_matches.iterrows():
#             counselor_name = row['Counselor Name']
#             gc_folder = os.path.join(biocards_folder, 'GC Biocards')
#             st.markdown(f"**{counselor_name}**")
#             display_pdf(gc_folder, counselor_name)



if st.button("Find Top Counselors"):
    # Calculate top matches for both FAO and GC
    # fao_top_matches = calculate_score(fao_df, st.session_state.get('fao_points', {}))
    # gc_top_matches = calculate_score(gc_df, st.session_state.get('gc_points', {}))

    # Display results in two columns
    st.header("Top Counselor Matches")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top FAO Matches")
        for _, row in fao_top_matches.iterrows():
            st.markdown(f"""
            <div class="profile-card">
                <h3>{row['Counselor Name']}</h3>
                <p><strong>Score:</strong> {row['Score']}</p>
                <p><strong>Personality Traits:</strong> {row['FAO Personality Traits']}</p>
                <p><strong>Subjects:</strong> {row['Subjects']}</p>
                <p><strong>Timezone:</strong> {row['Available Timezones']}</p>
                <p><strong>Degree:</strong> {row['Degree Classification']}</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.subheader("Top GC Matches")
        for _, row in gc_top_matches.iterrows():
            st.markdown(f"""
            <div class="profile-card">
                <h3>{row['Counselor Name']}</h3>
                <p><strong>Score:</strong> {row['Score']}</p>
                <p><strong>Personality Traits:</strong> {row['GC Personality Traits']}</p>
                <p><strong>Subjects:</strong> {row['Subjects']}</p>
                <p><strong>Timezone:</strong> {row['Available Timezones']}</p>
                <p><strong>Degree:</strong> {row['Degree Classification']}</p>
            </div>
            """, unsafe_allow_html=True)
