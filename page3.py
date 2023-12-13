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
    SchoolInfo = SchoolInfo.rename(columns={"prek": "Pre-kindergarten","k": "Kindergarten","grade1": "1st Grade", "grade2": "2nd Grade", "grade3": "3rd Grade",
                                            "grade4": "4th Grade", "grade5": "5th Grade", "grade6": "6th Grade", "grade7": "7th Grade",
                                            "grade8": "8th Grade", "grade9": "9th Grade",
                                            "grade10": "10th Grade", "grade11": "11th Grade", "grade12": "12th Grade",
                                            "male_num": "Male", "female_num": "Female",
                                            "asian_num": "Asian", "black_num": "Black", "hispanic_num": "Hispanic", "white_num": "White"
                                            })
    #st.dataframe(SchoolInfo)
    #Delete repeat
    unique_schools = set(SchoolInfo["Name"].tolist())

    #Melt Grade dataset
    melted_data = pd.melt(SchoolInfo, id_vars=['schoolyear','Name', 'total_enrollment'], value_vars=['Pre-kindergarten', 'Kindergarten',
                                                                                 '1st Grade', '2nd Grade', '3rd Grade', '4th Grade', '5th Grade',
                                                                                 '6th Grade', '7th Grade', '8th Grade', '9th Grade', '10th Grade',
                                                                                 '11th Grade', '12th Grade'], var_name='Grade', value_name='Total Number')

    #Filter
    st.sidebar.title("Filters")
    shl = st.sidebar.multiselect(
        'Select Schools:',
        options=list(unique_schools))

    syr = st.sidebar.radio(
        'Select Years:',
        options= ["All years"]+SchoolInfo["schoolyear"].unique().tolist())

    filterdataset = melted_data.copy()
    #st.dataframe(filterdataset)
    #Make filteredDataset
    if not shl:
        st.subheader("Overview of Grade percentage of all schools")
    else:
        filterdataset = filterdataset[filterdataset["Name"].isin(shl)]

    #another filter for futher questions
    #st.dataframe(filterdataset)

    #Count
    filterdataset['total'] = filterdataset['Grade'].sum()

    if not syr == "All years":
        filterdataset = filterdataset[filterdataset["schoolyear"] == syr]

    total_enrollment = filterdataset['total_enrollment'].sum()
    st.markdown(f"<div style='text-align: center;'><p style='font-size: 20px;"
                f" font-weight: bold;'>Total Enrollment</p><p style='font-size: 24px; font-weight: bold;'>{total_enrollment}</p></div>",
                unsafe_allow_html=True)
    #Fig
    fig = px.bar(filterdataset,
                 x='Name',
                 y='Total Number',
                 color='Grade',
                 title="Percentage of Grade",
                 labels={'value': 'Number of Students', 'variable': 'Grade'}
                )

    st.plotly_chart(fig)


    fig_pie = px.pie(filterdataset, names='Grade', values='Total Number',
                     title='Grade Distribution')

    st.plotly_chart(fig_pie)









