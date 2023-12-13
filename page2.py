import pandas as pd
import plotly.express as px
import streamlit as st

def show():
    #Data
    SchoolInfo = pd.read_csv("data/2006_-_2012_School_Demographics_and_Accountability_Snapshot_20231129.csv")
    SchoolInfo.fillna('none', inplace=True)
    SchoolInfo.replace(r'^\s*$', 'none', regex=True, inplace=True)

    #Clean
    SchoolInfo = SchoolInfo.drop(['fl_percent', 'frl_percent', 'ell_percent',
                                  'sped_percent', 'asian_per', 'black_per', 'hispanic_per',
                                  'white_per', 'male_per', 'female_per'], axis=1)
    SchoolInfo = SchoolInfo.rename(columns={"ell_num": "English Language Learner", "sped_num": "Special Education",
                                            "ctt_num": "Collaborative Team Teaching", "selfcontained_num": "Self Contained Special",
                                            "male_num": "Male", "female_num": "Female", "schoolyear": "School Year",
                                            })



    # Melt
    melted_data = pd.melt(SchoolInfo, id_vars=['Name', 'School Year'], value_vars=['English Language Learner', 'Special Education', 'Collaborative Team Teaching', 'Self Contained Special'], var_name='Special Courses', value_name='Total Enrollment')
    #Delete repeat
    unique_schools = set(melted_data["Name"].tolist())

    # Filters
    st.sidebar.title("Filters")
    shl = st.sidebar.multiselect(
        'Select Schools:',
        options=list(unique_schools))

    syr = st.sidebar.radio(
        'Select Years:',
        options= ["All years"]+SchoolInfo["School Year"].unique().tolist())

    #st.dataframe(melted_data)
    # FD dataset
    filterdataset = melted_data.copy()


    if not shl:
        st.subheader("Select Schools")
    else:
        filterdataset = filterdataset[filterdataset["Name"].isin(shl)]



    filterdataset = filterdataset.dropna(subset=['Total Enrollment'])


    # Count of rows in filtered data
    filterdataset['Total Enrollment'] = pd.to_numeric(filterdataset['Total Enrollment'], errors='coerce')

    # FIG
    fig = px.line(filterdataset, x='School Year', y='Total Enrollment', color='Special Courses',
                  title='Special Courses Over School Years',
                  labels={'Total Enrollment': 'Total Enrollment', 'School Year': 'School Year', 'Special Courses': 'Special Courses'})

    st.plotly_chart(fig)



    if not syr == "All years":
        filterdataset = filterdataset[filterdataset["School Year"] == syr]

    # Total enrollment in special courses
    total_enrollment_special_courses = filterdataset['Total Enrollment'].sum()
    st.metric("Total Enrollment in Special Courses", total_enrollment_special_courses)

    # Average total enrollment
    average_enrollment = filterdataset['Total Enrollment'].mean()
    st.metric("Average Total Enrollment", average_enrollment)

    # Maximum total enrollment
    max_enrollment = filterdataset['Total Enrollment'].max()
    st.metric("Maximum Total Enrollment", max_enrollment)

    # Pie
    fig_pie = px.pie(filterdataset, names='Special Courses', values='Total Enrollment',
                     title='Special Courses Distribution')
    #st.write(filterdataset)
    st.plotly_chart(fig_pie)


