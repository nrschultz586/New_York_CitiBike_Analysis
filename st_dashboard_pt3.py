################################################ DIVVY BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes Strategy Dashboard")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select a section:",
    ["Introduction", "Weather Impact on Bike Usage", "Most Popular Stations", "Interactive Map of Bike Trips", "Ride Duration Analysis", "Strategic Recommendations"]
)


########################## Import data ###########################################################################################

# Define the correct URLs
top20_url = "https://raw.githubusercontent.com/nrschultz586/New_York_CitiBike_Analysis/main/Data/Prepared_Data/top_20.csv"
df_DualAxis_url = "https://raw.githubusercontent.com/nrschultz586/New_York_CitiBike_Analysis/main/Data/Prepared_Data/avgTemp_BikeRidesDaily.csv"
RideDuration_top20_url = "https://raw.githubusercontent.com/nrschultz586/New_York_CitiBike_Analysis/main/Data/Prepared_Data/RideDuration_top20.csv"

# Read CSVs directly from GitHub
top20 = pd.read_csv(top20_url, index_col=0)
df_DualAxis = pd.read_csv(df_DualAxis_url, index_col=0)
RideDuration_top20 = pd.read_csv(RideDuration_top20_url)

######################################### DEFINE THE PAGES #####################################################################


# Introduction Page
if page == "Introduction":
    st.header("Introduction")
    
    # Add an image (if available)
    image_path = "Citi_Bikes.jpg"  # Ensure this image is in the working directory
    try:
        image = Image.open("Citi_Bikes.jpg") #source: https://unsplash.com/photos/lined-parked-bicycles-URK0rZTiOHc 
        st.image(image, caption="Citi Bike Network in NYC", use_container_width=True)
    except FileNotFoundError:
        st.warning("Image not found. Please ensure 'citi_bike_image.jpg' is available.")

    # Dashboard Overview
    st.write("""
    Welcome to the **Citi Bike Strategic Dashboard**! This dashboard analyzes Citi Bike trip data 
    in New York City, identifying distribution inefficiencies and seasonal demand variations.
    """)

    # Purpose of the Analysis
    st.markdown("""
    ### **Project Objective**
    Citi Bike has faced growing demand since its launch, but this success has led to **bike shortages** 
    at high-traffic stations and **availability issues** in certain neighborhoods. This dashboard 
    aims to **diagnose** these challenges and **recommend solutions**.
    """)

    # Key Sections Overview
    st.markdown("""
    ### **Dashboard Sections**
    - **Weather Impact on Bike Usage** → Examines the relationship between weather and trip demand.
    - **Most Popular Stations** → Identifies high-traffic stations with the most rides.
    - **Interactive Map of Bike Trips** → Visualizes trip data across NYC.
    - **Strategic Recommendations** → Presents insights and potential solutions.
    """)

    st.write("Use the **Navigation** menu on the left to explore different sections of the analysis.")



### Dual-Axis Line Chart ###
    
if page == "Weather Impact on Bike Usage":
    st.header("Weather Impact on Bike Usage")

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df_DualAxis['date'], y = df_DualAxis['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_DualAxis['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df_DualAxis['date'], y = df_DualAxis['avgTemp'], name = 'Daily temperature', marker={'color': df_DualAxis['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily Bike Trips and Temperatures in 2022',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    # Markdown Interpretation Section
    st.markdown("### **Key Observations from the Chart:**")
    st.markdown("""
    1. **Seasonal Variations** → Bike usage increases in warmer months (May–October) and drops during colder months, aligning with temperature fluctuations.
    2. **Correlation with Weather** → Higher temperatures correspond to more bike rides, suggesting weather significantly impacts ridership.
    3. **Demand Surges & Shortages** → Peak summer months see an increased demand, possibly leading to availability shortages at key stations.
    4. **Strategic Considerations** → Citi Bike may need to adjust bike distribution patterns seasonally to prevent shortages in high-demand periods.
    """)


# Most Popular Stations Page
if page == "Most Popular Stations":
    st.header("Most Popular Bike Stations")

    # Bar Chart
    fig = go.Figure(go.Bar(
        x=top20['start_station_name'], 
        y=top20['value'], 
        marker={'color': top20['value'], 'colorscale': 'Blues'}
    ))

    fig.update_layout(
        title=dict(
            text='Top 20 Most Popular Bike Stations in NYC',
            font=dict(color="white", size=18)
        ),
        xaxis_title='Bike Station Name',
        yaxis_title='Total Trips Taken',
        width=900, height=600,
    
     # Dark theme settings
        plot_bgcolor="#1E1E1E",  # Chart background color
        paper_bgcolor="#1E1E1E",  # Overall background color
    font=dict(color="white"),  # Change font color for text elements
    xaxis=dict(
        title=dict(font=dict(color="white")),
        tickfont=dict(color="white"),  # Change x-axis labels color
        showgrid=False  # Remove grid lines for a cleaner look
    ),
    yaxis=dict(
        title=dict(font=dict(color="white")),
        tickfont=dict(color="white"),  # Change y-axis labels color
        showgrid=False  # Remove grid lines
        )
    )
    
    # Show the Plotly chart
    st.plotly_chart(fig, use_container_width=True)

    # Markdown Interpretation Section
    st.markdown("### **Key Observations from the Chart:**")
    st.markdown("""
    1. **High-Traffic Stations** → The top stations account for a significant portion of Citi Bike trips, suggesting concentrated usage in key areas.
    2. **Skewed Distribution** → A few stations dominate usage, indicating demand is not evenly spread across the city.
    3. **Potential Shortages** → The highest-ranking stations likely experience shortages during peak hours, affecting customer experience.
    4. **Expansion Considerations** → Insights from this chart can inform strategic expansion efforts to balance bike availability and improve accessibility.
    """)


 #Interactive Map Page
if page == "Interactive Map of Bike Trips":
    st.header("Bike Trip Patterns Across New York City")

    # Add the map
    html_url = 'https://raw.githubusercontent.com/nrschultz586/New_York_CitiBike_Analysis/main/Bike%20Trips%20Aggregated.html'  # Ensure this file is available in the working directory

    # Fetch the HTML file content
    response = requests.get(html_url)
    
    try:
        with open('Bike_Trips_Aggregated.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        # Display confirmation
        print("HTML file successfully downloaded and saved!")
        
        st.subheader("Visualizing Citi Bike Usage Across NYC")
        st.components.v1.html(html_data, height=1000)

    except FileNotFoundError:
        st.error(f"Map file not found: {path_to_html}. Please ensure the file is in the correct directory.")

    # Markdown Interpretation Section
    st.markdown("### **Key Observations from the Map:**")
    st.markdown("""
    1. **High Activity in Manhattan** → The densest trip clusters are in lower and midtown Manhattan, where bike demand is the highest.
    2. **Key Commuter Routes** → Strong travel connections exist between Manhattan, Brooklyn, and Jersey City, indicating major commuting routes.
    3. **Uneven Distribution** → Some areas, especially in outer boroughs, have lower Citi Bike usage, suggesting gaps in accessibility or demand.
    4. **Expansion Opportunities** → Insights from this map can help optimize station placement and redistribution strategies to meet peak-time demand.
    """)


# Ride Duration Analysis Page 
if page == "Ride Duration Analysis":
    st.header("Ride Duration Analysis")

    # Bar Chart
    fig2 = go.Figure(go.Bar(
        x=RideDuration_top20['start_station_name'], 
        y=RideDuration_top20['ride_duration'], 
        marker={'color': RideDuration_top20['ride_duration'], 'colorscale': 'Blues'}
    ))

    fig2.update_layout(
        title=dict(
            text='Top 20 Stations by Ride Duration',
            font=dict(color="white", size=18)
        ),
        xaxis_title='Bike Station Name',
        yaxis_title='Average Ride Duration (minutes)',
        width=900, height=600,
        
    # Dark theme settings
        plot_bgcolor="#1E1E1E",  # Chart background color
        paper_bgcolor="#1E1E1E",  # Overall background color
    font=dict(color="white"),  # Change font color for text elements
    xaxis=dict(
        title=dict(font=dict(color="white")),
        tickfont=dict(color="white"),  # Change x-axis labels color
        showgrid=False  # Remove grid lines for a cleaner look
    ),
    yaxis=dict(
        title=dict(font=dict(color="white")),
        tickfont=dict(color="white"),  # Change y-axis labels color
        showgrid=False  # Remove grid lines
        )
    )

    # Show the Plotly chart
    st.plotly_chart(fig2, use_container_width=True)

    # Interpretation Section
    st. markdown("### **Key Takeaways**")
    st.markdown("""
    - **Drastic Variation in Ride Duration**  
       - The top stations (e.g., 2 Ave & 43 St, Broad St & Water St, South St & Broad St) have significantly higher average ride durations compared to others.  
       - The difference between the top three stations and the remaining stations is substantial, indicating that certain locations may experience longer bike retention times.  

    - **Potential Bike Shortages at High-Duration Stations**  
       - Stations with longer average rides might face bike availability issues if riders are keeping bikes for extended periods.  
       - Citi Bike may need to increase bike supply or introduce ride duration limits at these stations.  

    - **Possible Reasons for High Ride Durations**  
       - **Tourist Areas**: Locations with long rides could be near tourist attractions, where bikes are rented for leisure rather than commuting.  
       - **Low Dock Availability**: Some stations may not have enough docks, forcing riders to continue riding until a dock is found.  
       - **Fewer Nearby Stations**: If alternative stations are far apart, users might be riding longer distances to return their bikes.  

    - **Clusters of Short-Duration Stations**  
       - The majority of stations have an average ride duration below 100 minutes, suggesting efficient turnover and usage.  
       - These stations might be located in business or commuter-heavy areas, where users take short trips rather than long rides.  

    - **Need for Strategic Bike Redistribution**  
       - The stark contrast between high-duration stations and lower-duration stations suggests that Citi Bike should reallocate bikes based on demand patterns.  
       - Longer-duration stations might require more available bikes, while shorter-duration stations might benefit from better redistribution of idle bikes.  
    """)
    

# Recommendations Page
if page == "Strategic Recommendations":
    st.header("Strategic Recommendations for Citi Bike")

    # Add an image (if available)
    image_path = "Citi_Bikes2.jpg"  # Ensure this image is in the working directory
    try:
        image = Image.open("Citi_Bikes2.jpg") #source: https://unsplash.com/photos/a-row-of-blue-bicycles-parked-next-to-each-other-OGaaDTtttvI
        st.image(image, caption="", use_container_width=True)
    except FileNotFoundError:
        st.warning("Image not found. Please ensure 'citi_bike_image.jpg' is available.")
        
    st.markdown("""
    ## **Summary of Key Insights**
    - **Stations with Long Ride Durations**  
      - Certain stations have significantly longer ride durations, indicating possible bike retention issues.
      - Potential causes: Tourist areas, lack of docking stations, or bikes being taken out of service improperly.
      - Impact: Longer ride durations may reduce bike availability, leading to shortages.

    - **Stations with High Trip Counts**  
      - Some stations handle far more trips than others, making them critical transit hubs.
      - Impact: These stations may experience high demand for bikes, requiring frequent rebalancing.

    - **Variation in Demand by Location**  
      - Commuter-heavy areas tend to have shorter, frequent rides.
      - Tourist-heavy locations may see longer ride durations but fewer total trips.

    ## **Strategic Recommendations**
    ### **1. Increase Bike Supply in High-Demand Areas**
    - Stations with high trip counts should be prioritized for bike redistribution.
    - Identify peak usage hours and adjust supply accordingly.

    ### **2. Optimize Docking Station Availability**
    - Expand docking stations near high-duration stations to prevent riders from extending trips due to lack of docks.
    - Implement a dynamic rebalancing system to move bikes from low-use stations to high-use stations.

    ### **3. Investigate and Reduce Ride Duration Outliers**
    - Some stations experience unusually long ride durations, potentially due to bikes not being properly checked in.
    - Citi Bike should track stations with extreme ride durations and investigate possible issues like system errors or retention abuse.

    ### **4. Adjust Pricing or Incentives Based on Usage Patterns**
    - Offer incentives for users to return bikes to high-demand areas to improve availability.
    - Implement dynamic pricing to encourage faster turnaround times in bike-shortage zones.

    ### **5. Seasonal and Time-Based Adjustments**
    - Analyze trip counts and ride durations by season to ensure enough bikes are available during peak months.
    - Implement a higher bike deployment strategy during summer months and major city events.

    ## **Next Steps**
    - Integrate real-time tracking for Citi Bike demand trends.
    - Further analyze user behavior (e.g., commuter vs. casual rider patterns).
    - Explore alternative transportation modes to complement Citi Bike in underserved areas.
    """)


