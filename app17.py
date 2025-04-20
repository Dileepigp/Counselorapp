import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials

# Set page configuration
st.set_page_config(
    page_title="InGenius Prep - Counselor Matchmaking",
    page_icon="🔍",
    layout="wide"
)

# Authentication credentials
USERNAME = "counselorapp"
PASSWORD = "igpcsapp@#*25"

# Authentication function
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Login Page
if not st.session_state["authenticated"]:
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.success("Login successful! Please proceed.")
        else:
            st.error("Invalid username or password.")

# Main App
if st.session_state["authenticated"]:
    # Logout button
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_set_query_params()  # Reset the app state

    # Initialize Google Sheets Client only once
    if 'client' not in st.session_state:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file('keys.json', scopes=scope)
        st.session_state['client'] = gspread.authorize(creds)
        st.session_state['spreadsheet'] = st.session_state['client'].open_by_key('19a7DqNpQHUdm4rV_1Em-IdfKMgnhwcARx9QhQUqlhNw')
        st.session_state['fao_worksheet'] = st.session_state['spreadsheet'].worksheet("UG FAOs")
        st.session_state['gc_worksheet'] = st.session_state['spreadsheet'].worksheet("US UG GCs")
        
        # Load data only once
        st.session_state['fao_df'] = pd.DataFrame(st.session_state['fao_worksheet'].get_all_records())
        st.session_state['gc_df'] = pd.DataFrame(st.session_state['gc_worksheet'].get_all_records())
        st.session_state['college_rankings_df'] = pd.read_csv('Colleges Rankings.csv')

    # Function to clean comma-separated values in counselor data
    def clean_counselor_data(df):
        """Clean all string columns in counselor data (FAO/GC)"""
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                # Clean individual comma-separated values
                df[col] = df[col].apply(
                    lambda x: ', '.join([item.strip() for item in str(x).split(',')]) 
                    if pd.notnull(x) else x
                )
        return df

    # Function to clean college rankings data
    def clean_college_rankings(df):
        """Clean only the COLLEGE column in rankings data"""
        if 'COLLEGE' in df.columns:
            df['COLLEGE'] = df['COLLEGE'].str.strip()
        return df

    # Clean the data
    fao_df = clean_counselor_data(st.session_state['fao_df'])
    gc_df = clean_counselor_data(st.session_state['gc_df'])
    college_rankings_df = clean_college_rankings(st.session_state['college_rankings_df'])

    # Standard cleaning for both DataFrames
    for df in [fao_df, gc_df]:
        df.fillna("", inplace=True)
        df.columns = df.columns.str.strip()

    Admission_experience_options = college_rankings_df['COLLEGE'].tolist()

    incompatible_counselors = {
        'Hubert Mysliwiec': ['Will Fenton', 'Nick Strohl', 'Natalia Ostrowski', 'Heather McCutchen'],
        'Sam Heidepriem': ['Roscoe Nicholson'],
        'Kevin Covarrubias': ['Roscoe Nicholson', 'Claire Gumus'],
        'Robert Thomas': ['Roscoe Nicholson'],
        'Amy Greene': ['Zakaree Harris'],
        'Sophia Jung':['Kevin Dupont'],
        'Kndeya Gebrewahed':['Zakaree Harris'],
        'Avi Kapach':['Crissy Gaffney'],
        'Chloe Mercado Weber': ['Roscoe Nicholson'],
        'Megan Bailey': ['Roscoe Nicholson']
    }
    fao_traits_options = [
        '🧠 Bubbly',
        '🎨 Creative',
        '📝 Detail-oriented',
        '➡️ Direct',
        '⭐ Encouraging',
        '🧠 Energetic',
        '💪 Firm/strict',
        '🧠 Friend/sibling type',
        '😂 Funny',
        '🤝 Handholding',
        '✨ Kind',
        '📋 Organized',
        '🕊️ Patient',
        '🔥 Passionate',
        '🚀 Proactive',
        '💼 Professional',
        '🎓 Professor-type',
        '⚡ Responsive',
        '😊 Sensitive/supportive',
        '🧠 Sporty',
        '🗣️ Talkative/Chatty',
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
        '🗣️ Linguistics', 
        '📚 Literature',  
        '🎵 Music',        
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

    # Center the logo using a container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1]) 
        with col2:
            st.image("IGP Logo.png", width=600)


    # Add the title and tagline, centered
    st.markdown("""
        <h1 style="text-align: center; color: #005CAA; font-size: 2.5em; margin-top: 0;">
            Counselor Matchmaking Platform
        </h1>
        <div style="text-align: center; 
                    background: linear-gradient(135deg, #005CAA, #4A90E2); 
                    color: white; 
                    padding: 15px 20px; 
                    border-radius: 10px; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    font-size: 1.2em; 
                    width: fit-content; 
                    margin: 0 auto;">
            Find Your College Counseling Team
        </div>
    """, unsafe_allow_html=True)

    keys_to_reset = [
        'student_name', 'show_results', 'selected_fao', 'selected_gc',
        'selection_sent', 'reset', 'personality_traits', 'subjects',
        'timezones', 'packages', 'additional_filters'
    ]

    # Check if a reset is needed at the start of your script
    if st.session_state.get('reset', False):
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['reset'] = False  # Clear the reset flag

    # Input for student name
# Replace the current student name input with this expanded section
    student_name = st.text_input("Enter Student Name:", key="student_name", value="")
    if student_name.strip() == "":
        st.warning("Please enter the student name before proceeding.")
        st.stop()

    # Add new fields for Responsible Region and Hubspot Deal
    responsible_regions = [
        'Atlanta',
        'Australia',
        'Beijing',
        'Boston',
        'Calgary',
        'Canada',
        'Chengdu',
        'Chicago',
        'China',
        'China in USA',
        'CIUAE',
        'CIUS - Other',
        'Cupertino',
        'Dallas',
        'Global Scholar Launch',
        'Greater New York',
        'Guangzhou',
        'Hong Kong',
        'Houston',
        'IIUS',
        'India',
        'Ireland',
        'Irvine',
        'Japan',
        'Jordan',
        'KIUS',
        'Korea',
        'Los Angeles',
        'Malaysia',
        'Montreal',
        'NCIC',
        'New Jersey',
        'New Zealand',
        'Northern California - Other',
        'Oman',
        'Ottawa',
        'Philadelphia',
        'Qatar',
        'San Diego',
        'Saudi Arabia',
        'Seattle',
        'Seoul',
        'Shanghai',
        'Shenzhen',
        'Singapore',
        'South Africa',
        'Taiwan',
        'Thailand',
        'Toronto',
        'UK',
        'United Arab Emirates',
        'United Kingdom',
        'US Domestic',
        'USA',
        'Vancouver',
        'Vietnam',
        'Washington DC'
    ]
    responsible_region = st.selectbox("Select Responsible Region", responsible_regions)
    hubspot_deal = st.text_input("Link to Hubspot Deal", type="password")

    # Function to extract unique values from a column
    def extract_unique_values(df, column_name):
        values = set()
        for val in df[column_name].dropna().unique():
            if isinstance(val, str):
                values.update([v.strip() for v in val.split(',')])
        return sorted(values)

    # Timezone selection
    fao_timezones = extract_unique_values(fao_df, 'Available Timezones')
    gc_timezones = extract_unique_values(gc_df, 'Available Timezones')
    combined_timezones = sorted(set(fao_timezones).union(set(gc_timezones)))
    selected_timezone = st.selectbox("Student's Time Zone During School Year", combined_timezones)

    # Student type selection
    fao_student_types = extract_unique_values(fao_df, 'Domestic/International')
    gc_student_types = extract_unique_values(gc_df, 'Domestic/International')
    combined_student_types = sorted(set(fao_student_types).union(set(gc_student_types)))
    selected_student_type = st.selectbox("Select Student Package", combined_student_types)

    # Package selection
    def get_linked_package(selected_package, package_mapping):
        return package_mapping.get(selected_package, None)

    def on_fao_package_change():
        fao_package = st.session_state['fao_package']
        gc_package = get_linked_package(fao_package, package_links)
        if fao_package == 'CB FAO Biweekly Meeting (Diamond)':
            st.session_state['gc_package'] = None
            st.session_state['disable_gc'] = True
        else:
            st.session_state['gc_package'] = gc_package
            st.session_state['disable_gc'] = False

    def on_gc_package_change():
        gc_package = st.session_state['gc_package']
        fao_package = get_linked_package(gc_package, reverse_package_links)
        if gc_package == 'CB GC Monthly Meeting (7- 8th Grade Platinum)':
            st.session_state['fao_package'] = None
            st.session_state['disable_fao'] = True
        else:
            st.session_state['fao_package'] = fao_package
            st.session_state['disable_fao'] = False

    package_links = {
        'CB FAO Biweekly Meeting (Diamond)': None,
        'CB FAO Bimonthly Meeting (Gold/Platinum)': 'CB GC Biweekly Meeting (Platinum/Gold/Silver)',
        'CB FAO Quarterly Meeting (Silver)': 'CB GC Biweekly Meeting (Platinum/Gold/Silver)',
        'AC 5-school Package (Silver)': 'AC 5-school Package (Silver)',
        'AC 8-school Package (Gold)': 'AC 8-school Package (Gold)',
        'AC 12-school Package (Platinum)': 'AC 12-school Package (Platinum)',
        'AC 5-school Transfer (Silver)': 'AC 5-school Transfer (Silver)'
    }
    reverse_package_links = {v: k for k, v in package_links.items() if v}

    # Initialize session states for packages
    if 'fao_package' not in st.session_state:
        st.session_state['fao_package'] = None
    if 'gc_package' not in st.session_state:
        st.session_state['gc_package'] = None
    if 'disable_fao' not in st.session_state:
        st.session_state['disable_fao'] = False
    if 'disable_gc' not in st.session_state:
        st.session_state['disable_gc'] = False

    # Add these new lines right after the package initializations
    if 'responsible_region' not in st.session_state:
        st.session_state['responsible_region'] = ''
    if 'hubspot_deal' not in st.session_state:
        st.session_state['hubspot_deal'] = ''

    # This is your existing code that continues with:
    fao_packages = extract_unique_values(fao_df, 'Available Packages')
    gc_packages = extract_unique_values(gc_df, 'Available Packages')

    st.markdown("### Package Selection for FAO and GC")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Select FAO Package")
        selected_fao_package = st.selectbox(
            "FAO Packages",
            options=fao_packages,
            index=fao_packages.index(st.session_state['fao_package']) if st.session_state['fao_package'] in fao_packages else 0,
            key='fao_package',
            on_change=on_fao_package_change,
            disabled=st.session_state['disable_fao']
        )

    with col2:
        st.markdown("#### Select GC Package")
        selected_gc_package = st.selectbox(
            "GC Packages",
            options=gc_packages,
            index=gc_packages.index(st.session_state['gc_package']) if st.session_state['gc_package'] in gc_packages else 0,
            key='gc_package',
            on_change=on_gc_package_change,
            disabled=st.session_state['disable_gc']
        )



    fao_package_available = selected_fao_package and not st.session_state['disable_fao']
    gc_package_available = selected_gc_package and not st.session_state['disable_gc']

    # Counselor preferences section
    def rank_input(label, available_ranks, key=None):
        """Render a rank input with restricted options."""
        st.markdown(f"**{label}**")
        st.markdown("""
            <span style="color: #757575; font-size: 0.9rem;">
            Assign a rank to this category based on its importance to you:
            <br><strong>Rank 1:</strong> Represents your top-most priority category.
            <br><strong>Subsequent Ranks (e.g., 2, 3...):</strong> Reflect progressively lower priority based on the assigned ranks.
            </span>
        """, unsafe_allow_html=True)
        rank = st.selectbox(label, available_ranks, key=key)
        return rank

    # Extract unique credentials for each counselor type
    fao_credentials = college_rankings_df['COLLEGE'].tolist()
    gc_credentials = college_rankings_df['COLLEGE'].tolist()

    # Split Screen: FAO on the left, GC on the right
    col1, col2 = st.columns([1, 1])

    # Initialize session state for FAO and GC priority sections
    if "show_fao_priority" not in st.session_state:
        st.session_state["show_fao_priority"] = False
    if "show_gc_priority" not in st.session_state:
        st.session_state["show_gc_priority"] = False

    # FAO Section
    if fao_package_available:
        with col1:
            with st.expander("FAO Counselors Section", expanded=True):
                st.subheader("Preferences for FAO Counselors")
                fao_preferences = {
                    'FAO Personality Traits': st.multiselect("Select preferred personality traits (FAO)", fao_traits_options, key="fao_traits",max_selections=3),
                    'Subjects': st.multiselect("Select subjects of interest (FAO)", subjects_options, key="fao_subjects",max_selections=3),
                    'Credentials': st.multiselect("Preferred Credentials (Graduated College - FAO)", fao_credentials, key="fao_credentials",max_selections=3)
                }
                fao_Admission_experience = st.multiselect(
                    "Preferred Admission Results (FAO)", 
                    Admission_experience_options, 
                    key="fao_Admission",max_selections=3
                )

                if st.button("Rank Preferences for FAO"):
                    st.session_state["show_fao_priority"] = True

            if st.session_state["show_fao_priority"]:
                st.subheader("Rank Preferences for FAO")
                fao_points = {}
                num_categories = len([opts for opts in fao_preferences.values() if opts])
                if fao_Admission_experience:
                    num_categories += 1

                available_ranks = list(range(1, num_categories + 1))

                for category, options in fao_preferences.items():
                    if options:
                        category_rank = rank_input(f"Rank for {category} (FAO)", available_ranks, key=f"fao_rank_{category}")
                        available_ranks.remove(category_rank)
                        for option in options:
                            clean_option = option.split(" ", 1)[1] if " " in option else option
                            fao_points[f"{category}: {clean_option}"] = 10 * (num_categories + 1 - category_rank)

                if fao_Admission_experience:
                    category_rank = rank_input(f"Rank for Admission Results (FAO)", available_ranks, key="fao_Admission_rank")
                    available_ranks.remove(category_rank)
                    for exp in fao_Admission_experience:
                        fao_points[f"Admission Results: {exp}"] = 10 * (num_categories + 1 - category_rank)

                st.session_state['fao_points'] = fao_points

    # GC Section
    if gc_package_available:
        with col2:
            with st.expander("GC Counselors Section", expanded=True):
                st.subheader("Preferences for GC Counselors")
                gc_preferences = {
                    'GC Personality Traits': st.multiselect("Select preferred personality traits (GC)", fao_traits_options, key="gc_traits",max_selections=3),
                    'Subjects': st.multiselect("Select subjects of interest (GC)", subjects_options, key="gc_subjects",max_selections=3),
                    'Credentials': st.multiselect("Preferred Credentials (Graduated College - GC)", gc_credentials, key="gc_credentials",max_selections=3)
                }
                gc_Admission_experience = st.multiselect(
                    "Preferred Admission Results (GC)", 
                    Admission_experience_options, 
                    key="gc_Admission",max_selections=3
                )

                if st.button("Rank Preferences for GC"):
                    st.session_state["show_gc_priority"] = True

            if st.session_state["show_gc_priority"]:
                st.subheader("Rank Preferences for GC")
                gc_points = {}
                num_categories = len([opts for opts in gc_preferences.values() if opts])
                if gc_Admission_experience:
                    num_categories += 1

                available_ranks = list(range(1, num_categories + 1))

                for category, options in gc_preferences.items():
                    if options:
                        category_rank = rank_input(f"Rank for {category} (GC)", available_ranks, key=f"gc_rank_{category}")
                        available_ranks.remove(category_rank)
                        for option in options:
                            clean_option = option.split(" ", 1)[1] if " " in option else option
                            gc_points[f"{category}: {clean_option}"] = 10 * (num_categories + 1 - category_rank)

                if gc_Admission_experience:
                    category_rank = rank_input(f"Rank for Admission Results (GC)", available_ranks, key="gc_Admission_rank")
                    available_ranks.remove(category_rank)
                    for exp in gc_Admission_experience:
                        gc_points[f"Admission Results: {exp}"] = 10 * (num_categories + 1 - category_rank)

                st.session_state['gc_points'] = gc_points

    def calculate_score(df, points):
        # Always create a Score column, defaulting to 0
        df["Score"] = 0
        
        if not points:  # If no points are assigned, return with all scores = 0
            return df
            
        def score_row(row):
            score = 0
            for option, weight in points.items():
                try:
                    # Admission Results Points
                    if option.startswith("Admission Results"):
                        admission_experiences = row.get('Admission Results', "")
                        if isinstance(admission_experiences, str):
                            # Split and clean each admission result
                            admission_experiences = [e.strip().lower() for e in admission_experiences.split(",") if e.strip()]
                        # Check if any matches (case-insensitive)
                        if option.split(": ")[1].lower() in admission_experiences:
                            score += weight
                    
                    # Credentials Points - Enhanced matching
                    elif option.startswith("Credentials"):
                        credentials = row.get('Credentials', "")
                        if isinstance(credentials, str):
                            # Split, clean, and normalize credentials
                            credentials = [c.strip().lower() for c in credentials.split(",") if c.strip()]
                            # Check if any credential matches (case-insensitive, substring allowed)
                            selected_cred = option.split(": ")[1].lower()
                            if any(selected_cred in cred for cred in credentials):
                                score += weight
                    
                    # General Traits/Subjects (case-sensitive for emoji prefixes)
                    else:
                        column, value = option.split(": ")
                        if value in row.get(column, ""):
                            score += weight
                except (KeyError, TypeError, ValueError) as e:
                    print(f"Error processing option '{option}': {str(e)}")
                    continue
            return score

        df["Score"] = df.apply(score_row, axis=1)
        return df

    def filter_incompatible_pairs(fao_df, gc_df):
        for gc_name, fao_names in incompatible_counselors.items():
            if gc_name in gc_df['Name'].values:
                gc_counselor = gc_df.loc[gc_df['Name'] == gc_name]
                gc_score = gc_counselor['Score'].values[0]
                for fao_name in fao_names:
                    if fao_name in fao_df['Name'].values:
                        fao_counselor = fao_df.loc[fao_df['Name'] == fao_name]
                        fao_score = fao_counselor['Score'].values[0]
                        if gc_score > fao_score:
                            fao_df = fao_df[fao_df['Name'] != fao_name]
                        elif fao_score > gc_score or fao_score == gc_score:
                            gc_df = gc_df[gc_df['Name'] != gc_name]
                            break  # Only remove the GC if there's a strict resolution
        return fao_df, gc_df

    def filter_counselors(df, package_type, selected_timezone, selected_student_type):
        # Apply initial filters
        df = df[df['Available Timezones'].apply(lambda x: selected_timezone in [tz.strip() for tz in x.split(',')])]
        df = df[df['Domestic/International'].apply(lambda x: selected_student_type in [t.strip() for t in x.split(',')])]
        
        # Filter by package
        if package_type:
            df = df[df['Available Packages'].apply(lambda x: package_type in [pkg.strip() for pkg in x.split(',')])]
        
        return df

    def sort_counselors(df, package_type):
        # Filter out entries with zero or negative spots available
        if "AC" in package_type and '# AC spots left after recommendations' in df.columns:
            df = df[df['# AC spots left after recommendations'] > 0]
            return df.sort_values(by=['# AC spots left after recommendations', 'Score'], ascending=[False, False])
        elif "CB" in package_type and '# CB spots left after recommendations' in df.columns:
            df = df[df['# CB spots left after recommendations'] > 0]
            return df.sort_values(by=['# CB spots left after recommendations', 'Score'], ascending=[False, False])
        return df  # Return the dataframe unmodified if conditions are not met




    def increment_assigned_google_sheet(sheet_name, counselor_name, selected_package, student_name):
        try:
            worksheet = st.session_state['spreadsheet'].worksheet(sheet_name)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Get all records and headers
            records = worksheet.get_all_records()
            headers = worksheet.row_values(1)

            # Find the row index for the counselor
            row_index = None
            for i, record in enumerate(records, start=2):  # start=2 because header is row 1
                if record.get('Name') == counselor_name:
                    row_index = i
                    break
            
            if row_index is None:
                raise ValueError(f"Counselor {counselor_name} not found in {sheet_name}")

            # Determine package type and column names
            package_prefix = 'AC' if selected_package.startswith('AC') else 'CB'
            recommended_col_name = f'# {package_prefix} recommended'
            spots_left_col_name = f'# {package_prefix} spots left after recommendations'
            student_col_prefix = f'Recommended {package_prefix} Student'

            # Find column indices
            try:
                recommended_col_idx = headers.index(recommended_col_name) + 1
                spots_left_col_idx = headers.index(spots_left_col_name) + 1
            except ValueError as e:
                print("Available column names:")
                print(headers)
                raise ValueError(f"Columns for {selected_package} not found. {str(e)}")

            # Determine increment/decrement values
            increment_value = 1  # Default for AC
            decrement_value = 1
            if "Biweekly" in selected_package and 'FAO' in sheet_name:
                increment_value = 3  # FAO Biweekly packages
                decrement_value = 3
            elif "Monthly" in selected_package and 'GC' in sheet_name:
                increment_value = 0.5  # GC Monthly packages
                decrement_value = 0.5

            # Get current values safely
            def get_float_value(row, col):
                value = worksheet.cell(row, col).value
                try:
                    return float(value) if value else 0.0
                except ValueError:
                    raise ValueError(f"Non-numeric value in cell ({row}, {col}): {value}")

            current_recommended = get_float_value(row_index, recommended_col_idx)
            current_spots_left = get_float_value(row_index, spots_left_col_idx)

            # Update recommendation counts
            worksheet.update_cell(row_index, recommended_col_idx, current_recommended + increment_value)
            worksheet.update_cell(row_index, spots_left_col_idx, current_spots_left - decrement_value)

            # Find the first empty student column
            student_col_idx = None
            for i, header in enumerate(headers, start=1):
                if header.startswith(student_col_prefix):
                    if not worksheet.cell(row_index, i).value:
                        student_col_idx = i
                        break
            
            if student_col_idx is None:
                # Add new column if all existing ones are filled
                student_col_idx = len(headers) + 1
                worksheet.update_cell(1, student_col_idx, f"{student_col_prefix} {int(current_recommended + increment_value)}")
                headers = worksheet.row_values(1)  # Refresh headers

            # Prepare student info with clickable HubSpot link
            hubspot_deal = st.session_state.get('hubspot_deal', '')
            if hubspot_deal:
                # Build formula parts safely
                parts = [
                    f'"Student: {student_name}"',
                    f'"Date: {now}"',
                    f'"Package: {selected_package}"',
                    f'"Region: {st.session_state.get("responsible_region", "")}"',
                    '"Click for HubSpot Deal"'
                ]
                joined_parts = " & CHAR(10) & ".join(parts)
                student_info = f'=HYPERLINK("{hubspot_deal}", {joined_parts})'
            else:
                # Regular format if no HubSpot deal
                student_info = f"""Student: {student_name}
    Date: {now}
    Package: {selected_package}
    Responsible Region: {st.session_state.get('responsible_region', '')}"""

            # Update the cell
            worksheet.update_cell(row_index, student_col_idx, student_info)

            return True

        except Exception as e:
            st.error(f"Error updating Google Sheet: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return False


    def display_and_select_counselors(df, state_key, counselor_type):
        st.subheader(f"Top {counselor_type} Matches")
        
        # Determine selection limit based on package
        if counselor_type == 'FAO':
            fao_package = st.session_state.get('fao_package', '')
            selection_limit = 2 if fao_package == 'CB FAO Biweekly Meeting (Diamond)' else 1
        elif counselor_type == 'GC':
            fao_package = st.session_state.get('fao_package', '')
            selection_limit = 0 if fao_package == 'CB FAO Biweekly Meeting (Diamond)' else 2
        else:
            selection_limit = 1  # default fallback

        # Ensure session state list exists
        selected_names = st.session_state.get(state_key, [])

        for index, row in df.iterrows():
            is_selected = row['Name'] in selected_names

            # Render card
            counselor_card = f"""
            <div class="profile-card" style="background-color: {'#ADD8E6' if is_selected else '#FFFFFF'};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3>{row['Name']}</h3>
                </div>
            """

            if counselor_type == 'FAO':
                degree = row.get('Degree', '')
                admission_experience = row.get('Admissions Experience', '')
                if degree:
                    counselor_card += f"<p><strong>Degree:</strong> {degree}</p>"
                if admission_experience:
                    counselor_card += f"<p><strong>Admissions Experience:</strong> {admission_experience}</p>"
            elif counselor_type == 'GC':
                degree = row.get('Degree', '')
                if degree:
                    counselor_card += f"<p><strong>Degree:</strong> {degree}</p>"

            counselor_card += f"<p><strong>Selected:</strong> {'✅' if is_selected else '❌'}</p></div>"
            st.markdown(counselor_card, unsafe_allow_html=True)

            button_key = f"{counselor_type.lower()}_{index}"
            button_label = "Deselect" if is_selected else "Select"
            if st.button(f"{button_label} {row['Name']}", key=button_key):
                if is_selected:
                    selected_names.remove(row['Name'])
                else:
                    if len(selected_names) >= selection_limit:
                        st.warning(f"You can select up to {selection_limit} {counselor_type}(s).")
                    else:
                        selected_names.append(row['Name'])

                st.session_state[state_key] = selected_names
                st.rerun()


    if st.button("Find Top Counselors"):
        st.session_state['selected_fao'] = []
        st.session_state['selected_gc'] = []
        # Initialize validation flags
        fao_needs_ranking = False
        gc_needs_ranking = False
        
        # Check if FAO preferences need ranking
        if fao_package_available:
            has_fao_prefs = (
                st.session_state.get('fao_traits') or 
                st.session_state.get('fao_subjects') or 
                st.session_state.get('fao_credentials') or 
                st.session_state.get('fao_Admission')
            )
            if has_fao_prefs and 'fao_points' not in st.session_state:
                fao_needs_ranking = True
        
        # Check if GC preferences need ranking
        if gc_package_available:
            has_gc_prefs = (
                st.session_state.get('gc_traits') or 
                st.session_state.get('gc_subjects') or 
                st.session_state.get('gc_credentials') or 
                st.session_state.get('gc_Admission')
            )
            if has_gc_prefs and 'gc_points' not in st.session_state:
                gc_needs_ranking = True
        
        # Show error messages if ranking is needed
        if fao_needs_ranking or gc_needs_ranking:
            error_messages = []
            if fao_needs_ranking:
                error_messages.append("Please rank your FAO preferences by clicking 'Rank Preferences for FAO'")
            if gc_needs_ranking:
                error_messages.append("Please rank your GC preferences by clicking 'Rank Preferences for GC'")
            
            st.error("\n".join(error_messages))
            st.stop()
        
        # Proceed with counselor matching if all validations pass
        try:
            # Process FAO counselors if package is available
            if fao_package_available:
                fao_df_filtered = filter_counselors(
                    fao_df.copy(), 
                    selected_fao_package, 
                    selected_timezone, 
                    selected_student_type
                )
                
                # Only calculate score if points exist (ranking was done)
                if 'fao_points' in st.session_state:
                    fao_df_filtered = calculate_score(fao_df_filtered, st.session_state['fao_points'])
                
                fao_df_filtered = sort_counselors(fao_df_filtered, selected_fao_package)
                st.session_state['fao_top_matches'] = fao_df_filtered.head(3)
            
            # Process GC counselors if package is available
            if gc_package_available:
                gc_df_filtered = filter_counselors(
                    gc_df.copy(), 
                    selected_gc_package, 
                    selected_timezone, 
                    selected_student_type
                )
                
                # Only calculate score if points exist (ranking was done)
                if 'gc_points' in st.session_state:
                    gc_df_filtered = calculate_score(gc_df_filtered, st.session_state['gc_points'])
                
                gc_df_filtered = sort_counselors(gc_df_filtered, selected_gc_package)
                st.session_state['gc_top_matches'] = gc_df_filtered.head(3)
            
            # Handle incompatible counselor pairs
            if (fao_package_available and gc_package_available and 
                'fao_top_matches' in st.session_state and 
                'gc_top_matches' in st.session_state):
                
                fao_filtered, gc_filtered = filter_incompatible_pairs(
                    st.session_state['fao_top_matches'].copy(),
                    st.session_state['gc_top_matches'].copy()
                )
                st.session_state['fao_top_matches'] = fao_filtered
                st.session_state['gc_top_matches'] = gc_filtered

            # Clean previously selected counselors not in top matches
            if fao_package_available and 'fao_top_matches' in st.session_state:
                valid_fao_names = st.session_state['fao_top_matches']['Name'].tolist()
                st.session_state['selected_fao'] = [
                    name for name in st.session_state.get('selected_fao', []) if name in valid_fao_names
                ]

            if gc_package_available and 'gc_top_matches' in st.session_state:
                valid_gc_names = st.session_state['gc_top_matches']['Name'].tolist()
                st.session_state['selected_gc'] = [
                    name for name in st.session_state.get('selected_gc', []) if name in valid_gc_names
                ]
            
            # Set flags for results display
            st.session_state['show_results'] = True
            st.session_state['selection_sent'] = False
            
        except Exception as e:
            st.error(f"An error occurred while processing counselor matches: {str(e)}")
            st.stop()

    if st.session_state.get('show_results'):
        st.header("Top Counselor Matches")
        
        # Create columns for FAO and GC displays
        if fao_package_available and gc_package_available:
            col1, col2 = st.columns(2)
            cols = [col1, col2]
        else:
            cols = [st.container()]
        
        # Display FAO matches if available
        if fao_package_available and 'fao_top_matches' in st.session_state:
            with cols[0]:
                display_and_select_counselors(st.session_state['fao_top_matches'], 'selected_fao', 'FAO')
        
        # Display GC matches if available
        if gc_package_available and 'gc_top_matches' in st.session_state:
            with cols[1] if fao_package_available else cols[0]:
                display_and_select_counselors(st.session_state['gc_top_matches'], 'selected_gc', 'GC')
        
        # Create a centered container for the buttons
        st.markdown("---")  # Optional divider line
        
        # Check conditions for showing Submit button
        both_packages_required = fao_package_available and gc_package_available
        fao_selected = st.session_state.get('selected_fao', [])
        gc_selected = st.session_state.get('selected_gc', [])

        
        # Create centered columns for buttons
        button_col1, button_col2, button_col3 = st.columns([2, 1, 2])
        
        with button_col2:  # This is the center column
            send_button = False
            
            if both_packages_required:
                if fao_selected and gc_selected:
                    send_button = st.button("Submit Choices")
            else:
                if fao_selected or gc_selected:
                    send_button = st.button("Submit Choices")
            
            if send_button and not st.session_state.get('selection_sent', False):
                # Store the additional information in session state
                st.session_state['responsible_region'] = responsible_region
                st.session_state['hubspot_deal'] = hubspot_deal
                
                success = True
                if fao_selected:
                    for fao_name in fao_selected:
                        success &= increment_assigned_google_sheet('UG FAOs', fao_name, selected_fao_package, student_name)

                if gc_selected:
                    for gc_name in gc_selected:
                        success &= increment_assigned_google_sheet('US UG GCs', gc_name, selected_gc_package, student_name)

                
                if success:
                    st.success("Submitted choices successfully!")
                    st.session_state['selection_sent'] = True
                    st.session_state['show_results'] = False
                else:
                    st.error("Failed to update one or more selections.")
            elif send_button:
                st.error("Selections already sent, please Return to Login or make new selections.")
            
            # Return to Login button (always shown)
            if st.button("Return to Login"):
                st.session_state.clear()
                st.session_state["authenticated"] = True  # Keep user logged in
                st.session_state["reset"] = True  # Reset user form inputs
                st.rerun()
    # def sort_counselors(df, package_type):
    #     # Filter out entries with zero or negative spots available
    #     if "AC" in package_type and '# AC spots left after recommendations' in df.columns:
    #         df = df[df['# AC spots left after recommendations'] > 0]
    #         return df.sort_values(by=['# AC spots left after recommendations', 'Score'], ascending=[False, False])
    #     elif "CB" in package_type and '# CB spots left after recommendations' in df.columns:
    #         df = df[df['# CB spots left after recommendations'] > 0]
    #         return df.sort_values(by=['# CB spots left after recommendations', 'Score'], ascending=[False, False])
    #     return df  # Return the dataframe unmodified if conditions are not met

    # def display_counselors(df, counselor_type):
    #     st.subheader(f"Top {counselor_type} Matches")
    #     for _, row in df.iterrows():
    #         counselor_card = f"""
    #         <div class="profile-card" style="background-color: #FFFFFF;">
    #             <div style="display: flex; justify-content: space-between; align-items: center;">
    #                 <h3>{row['Name']}</h3>
    #             </div>
    #             <p><strong>Personality Traits:</strong> {row[f'{counselor_type} Personality Traits']}</p>
    #             <p><strong>Subjects:</strong> {row['Subjects']}</p>
    #             <p><strong>Timezone:</strong> {row['Available Timezones']}</p>
    #         </div>
    #         """
    #         st.markdown(counselor_card, unsafe_allow_html=True)

    # if st.button("Find Top Counselors"):
    #     # Apply all filters at once to minimize API calls
    #     if fao_package_available:
    #         fao_df_filtered = filter_counselors(
    #             fao_df.copy(), 
    #             selected_fao_package, 
    #             selected_timezone, 
    #             selected_student_type
    #         )
    #         if 'fao_points' in st.session_state:
    #             fao_df_filtered = calculate_score(fao_df_filtered, st.session_state['fao_points'])
    #         fao_df_filtered = sort_counselors(fao_df_filtered, selected_fao_package)
    #         st.session_state['fao_top_matches'] = fao_df_filtered.head(3)
        
    #     if gc_package_available:
    #         gc_df_filtered = filter_counselors(
    #             gc_df.copy(), 
    #             selected_gc_package, 
    #             selected_timezone, 
    #             selected_student_type
    #         )
    #         if 'gc_points' in st.session_state:
    #             gc_df_filtered = calculate_score(gc_df_filtered, st.session_state['gc_points'])
    #         gc_df_filtered = sort_counselors(gc_df_filtered, selected_gc_package)
    #         st.session_state['gc_top_matches'] = gc_df_filtered.head(3)
        
    #     # Filter incompatible pairs after all other filters
    #     if fao_package_available and gc_package_available and 'fao_top_matches' in st.session_state and 'gc_top_matches' in st.session_state:
    #         fao_filtered, gc_filtered = filter_incompatible_pairs(
    #             st.session_state['fao_top_matches'].copy(),
    #             st.session_state['gc_top_matches'].copy()
    #         )
    #         st.session_state['fao_top_matches'] = fao_filtered
    #         st.session_state['gc_top_matches'] = gc_filtered
        
    #     st.session_state['show_results'] = True

    # if st.session_state.get('show_results'):
    #     st.header("Top Counselor Matches")
    #     cols = st.columns(2) if fao_package_available and gc_package_available else [st.container()]

    #     if fao_package_available and 'fao_top_matches' in st.session_state:
    #         with cols[0]:
    #             display_counselors(st.session_state['fao_top_matches'], 'FAO')

    #     if gc_package_available and 'gc_top_matches' in st.session_state:
    #         with cols[1] if fao_package_available else cols[0]:
    #             display_counselors(st.session_state['gc_top_matches'], 'GC')

    # if st.button("Return to Login"):
    #     st.session_state.clear()
    #     st.rerun()
