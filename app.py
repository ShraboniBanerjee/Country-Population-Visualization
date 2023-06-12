import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv('Data/countries-table.csv')
    return df

# Create the app
def main():
    # Set the title and sidebar
    st.title("Country-wise Population Visualization")
    st.sidebar.title("Options")

    # Load the data
    data = load_data()

    # Show the raw data if requested
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.write(data)

    # Visualize the data
    st.sidebar.subheader("Visualization Options")

    # Select countries to visualize
    selected_countries = st.sidebar.multiselect("Select Countries", data['country'].unique())

    if len(selected_countries) > 0:
        # Filter the data for selected countries
        filtered_data = data[data['country'].isin(selected_countries)]

        # Create a bar chart of population by country
        st.subheader("Population by Country")
        fig = px.bar(filtered_data, x='country', y='pop2023',
                     labels={'country': 'Country', 'pop2023': 'Population'},
                     title='Population by Country')
        st.plotly_chart(fig)

        # Create a line chart of population over time for selected countries
        st.subheader("Population Over Time")
        line_chart_data = data[data['country'].isin(selected_countries)]
        fig = px.line(line_chart_data, x='place', y=['pop1980', 'pop2000', 'pop2010', 'pop2022'],
                      color='country',
                      labels={'place': 'Year', 'value': 'Population'},
                      title='Population Over Time')
        st.plotly_chart(fig)

        # Display statistics summary for selected countries
        st.subheader("Statistics Summary")
        stats_summary = filtered_data[['country', 'pop1980', 'pop2000', 'pop2010', 'pop2022']].describe()
        st.write(stats_summary)

        # Create an interactive map of population by country
        st.subheader("Population Map")
        map_data = filtered_data.groupby('country', as_index=False).agg({'pop2023': 'max', 'landAreaKm': 'max'})
        fig = px.choropleth(map_data, locations='country', locationmode='country names',
                            color='pop2023', hover_name='country',
                            color_continuous_scale='Viridis',
                            title='Population Map (2023)')
        fig.update_geos(showcountries=True, countrycolor="darkgrey", showcoastlines=True, coastlinecolor="darkgrey",
                        showland=True, landcolor="lightgrey", showocean=True, oceancolor="azure")
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()
