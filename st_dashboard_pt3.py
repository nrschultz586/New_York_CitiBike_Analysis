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

    # Load the HTML file from local storage
    html_file = "Bike_Trips_Aggregated.html"  # Ensure this file exists in the same directory
    
    try:
        with open(html_file, "r", encoding="utf-8") as file:
            html_data = file.read()
    
        # Display the HTML in Streamlit
        st.components.v1.html(html_data, height=1000)
    
    except FileNotFoundError:
        st.error(f"Error: {html_file} not found. Make sure the file is in the app's directory.")

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
        
    # Key Insights Section
    st.markdown("### **Weather & Seasonal Impact** (Weather Impact on Bike Usage)")
    st.markdown("""
    - Ridership drops significantly between November and April, correlating with colder temperatures.
    - Demand is highest from May to September, suggesting the need for seasonal bike distribution adjustments.
    - Failing to adjust supply could lead to excess bikes in winter and shortages in peak months.
    """)
    st.markdown("**Recommendation:** Reduce bike supply in low-demand areas during colder months while maintaining full stock in commuter-heavy zones. Adjust maintenance schedules to prepare bikes for peak season.")

    st.markdown("### **High-Demand Stations**")
    st.markdown("""
    - Some stations handle far more trips than others, making them critical transit hubs.
    - High trip counts indicate strong demand, but without proper redistribution, bikes may not be available when needed.
    """)
    st.markdown("**Recommendation:** Implement real-time tracking and redistribution models to ensure availability. Adjust supply dynamically throughout the day based on peak usage hours.")

    st.markdown("### **Expansion Along the Water**")
    st.markdown("""
    - Locations along Brooklyn Bridge Park and the Hudson River Greenway are experiencing increased demand, especially in warmer months.
    - Expanding stations in these areas would improve connectivity for riders traveling between boroughs and waterfront attractions.
    """)
    st.markdown("**Recommendation:** Use trip data, peak usage trends, and rider feedback to determine the need for additional stations. Connect waterfront stations with ferries and subway stops to improve accessibility.")

    st.markdown("### **Ride Duration & Bike Availability**")
    st.markdown("""
    - Certain stations have significantly longer ride durations, possibly due to bike retention issues or lack of docking stations.
    - Tourist-heavy areas see longer average ride times, while commuter hubs have shorter, more frequent rides.
    """)
    st.markdown("**Recommendation:** Implement dynamic bike redistribution strategies to balance supply. Investigate long-duration outliers to identify system errors or areas where additional docking stations may be needed.")

    # Strategic Recommendations
    st.header("Strategic Recommendations")

    st.markdown("#### **1. Increase Bike Supply in High-Demand Areas**")
    st.markdown("""
    - Prioritize high-trip stations for bike redistribution to prevent shortages.
    - Adjust supply based on peak usage hours to ensure availability during rush hours and weekends.
    """)

    st.markdown("#### **2. Optimize Docking Station Availability**")
    st.markdown("""
    - Expand docking stations in locations with high ride durations where limited docks may lead to extended trips.
    - Implement a real-time bike rebalancing system to dynamically move bikes between low-use and high-use stations.
    """)

    st.markdown("#### **3. Investigate and Reduce Ride Duration Outliers**")
    st.markdown("""
    - Identify stations with excessively long ride durations and investigate potential causes.
    - Address system errors, bike retention issues, and station shortages to improve circulation.
    """)

    st.markdown("#### **4. Adjust Pricing or Incentives Based on Usage Patterns**")
    st.markdown("""
    - Offer incentives for returning bikes to high-demand stations.
    - Implement dynamic pricing to encourage faster returns in peak areas.
    """)

    st.markdown("#### **5. Seasonal and Time-Based Adjustments**")
    st.markdown("""
    - Analyze trip counts and ride durations seasonally to optimize bike availability.
    - Deploy more bikes during summer months and major city events to accommodate increased usage.
    """)

    # Next Steps
    st.header("Next Steps")

    st.markdown("""
    - **Enhance real-time tracking** to monitor Citi Bike demand trends and adjust availability dynamically.
    - **Further analyze user behavior** to distinguish between commuters, tourists, and casual riders.
    - **Explore partnerships with public transit** to expand Citi Bike’s role in the city’s transportation network.
    """)


