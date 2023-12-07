import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    SchoolInfo = pd.read_csv("data/2006_-_2012_School_Demographics_and_Accountability_Snapshot_20231129.csv")
    SchoolInfo = pd.DataFrame(SchoolInfo)

    SchoolInfo.fillna('none', inplace=True)
    SchoolInfo.replace(r'^\s*$', 'none', regex=True, inplace=True)

    #Title
    st.title("Annual school accounts of NYC public school 2006 - 2012")

    #Clean data
    SchoolInfo = SchoolInfo.drop(['fl_percent','frl_percent','ell_percent',
                                  'sped_percent','asian_per','black_per','hispanic_per',
                                  'white_per','male_per','female_per'], axis=1)
    SchoolInfo = SchoolInfo.rename(columns={"prek": "grade prek","k": "grade k",
                                            "male_num": "Male", "female_num": "Female",
                                            "asian_num": "Asian", "black_num": "Black", "hispanic_num": "Hispanic", "white_num": "White"
                                            })
    #Delete repeat
    unique_schools = set(SchoolInfo["Name"].tolist())
    #Filter
    st.sidebar.title("Filters")
    shl = st.sidebar.multiselect(
        'Select Schools:',
        options=list(unique_schools))

    syr = st.sidebar.radio(
        'Select Years:',
        options= ["All years"]+SchoolInfo["schoolyear"].unique().tolist())

    filterdataset = SchoolInfo.copy()

    #Make filteredDataset
    if not shl:
        st.subheader("Overview Insights of all schools")
    else:
        filterdataset = filterdataset[filterdataset["Name"].isin(shl)]


    #another filter for futher questions
    if not syr=="All years":
        filterdataset = filterdataset[filterdataset["schoolyear"] == syr]


    #Metrics Entrollment
    total_enrollment = filterdataset['total_enrollment'].sum()
    st.markdown(f"<div style='text-align: center;'><p style='font-size: 20px;"
                f" font-weight: bold;'>Total Enrollment</p><p style='font-size: 24px; font-weight: bold;'>{total_enrollment}</p></div>",
                unsafe_allow_html=True)

    #1 Overview of annual school accounts of NYC public school
    if filterdataset.empty:
        st.warning("No data available for the selected schools and year.")
    else:
        filterdataset['Male'] = pd.to_numeric(filterdataset['Male'], errors='coerce')
        filterdataset['Female'] = pd.to_numeric(filterdataset['Female'], errors='coerce')
    #Count
        filterdataset['total'] = filterdataset['Female'] + filterdataset['Male']
        filterdataset = filterdataset.dropna(subset=['Male', 'Female'])
    #Fig
        fig = px.bar(filterdataset, x='Name', y=['Male', 'Female'],
                 title="Percentage of Gender",
                 labels={'value': 'Number of Students', 'variable': 'Gender'},
                 color_discrete_sequence=['blue', 'pink'])

        st.plotly_chart(fig)


    #Race Pie
    melted_data = pd.melt(filterdataset, id_vars=['schoolyear','Name'], value_vars=['Asian', 'Black', 'Hispanic', 'White'], var_name='race', value_name='enrollment')
    fig = px.pie(melted_data, names='race', values='enrollment',
                 title='Race Distribution in Total Enrollment')

    st.plotly_chart(fig)

    #Delete this later
    #st.dataframe(SchoolInfo)
#st.dataframe(melted_data)