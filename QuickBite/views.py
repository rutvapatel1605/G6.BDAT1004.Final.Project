# myapp/views.py
from django.shortcuts import render
import plotly.express as px
import plotly.graph_objects as go
from .models import QuickBiteDocument
import pandas as pd
from plotly.subplots import make_subplots

def your_view(request):
    # Fetching all documents from the MongoDB collection
    documents = QuickBiteDocument.objects.all()

    # Creating a DataFrame from the documents
    data = [
        {
            'Id': doc.Id,
            'Name': doc.Name,
            'Rating': doc.Rating,
            'Discount': doc.Discount,
            'CashBack': doc.CashBack,
            'Cost_for_Two': doc.Cost_for_Two,
            'City': doc.City,
            'Locality': doc.Locality,
            'Home_Delivery': doc.Home_Delivery,
            'Manu_Count': doc.Manu_Count,
        }
        for doc in documents
    ]

    df = pd.DataFrame(data)

    # Filtering data for Mumbai city
    mumbai_data = df[df['City'] == 'Mumbai']

    # Creating histogram for ratings in Mumbai
    fig_mumbai = px.histogram(
        mumbai_data,
        x='Rating',
        nbins=10,  
        title='Rating Distribution in Mumbai',
        labels={'Rating': 'Rating'},
    )

    fig_mumbai.update_layout(
    height=400,  # Setting the height of the figure
    width=800,   # Setting the width of the figure
    )

    # Filter out data for New Delhi city
    delhi_data = df[df['City'] == 'New Delhi']

    # Creating a bar graph for ratings in New Delhi
    fig_delhi = px.histogram(
        delhi_data,
        x='Rating',
        nbins=10,
        title='Rating Distribution in New Delhi',
        labels={'Rating': 'Rating'},
    )

    fig_delhi.update_layout(
    height=400,  # Setting the height of the figure
    width=800,   # Setting the width of the figure
    )

    # Creating subplots
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=['Mumbai - Rating Distribution', 'New Delhi - Rating Distribution'])
    fig.add_trace(fig_mumbai['data'][0], row=1, col=1)
    fig.add_trace(fig_delhi['data'][0], row=1, col=2)

    # Updating the layout for the entire figure
    fig.update_layout(
        height=600,  # Setting the height of the entire figure
        width=995,   # Setting the width of the entire figure
    )

    # x-axis labels
    fig.update_xaxes(title_text='Rating', row=1, col=1)
    fig.update_xaxes(title_text='Rating', row=1, col=2)

    # y-axis labels
    fig.update_yaxes(title_text='Count', row=1, col=1)
    fig.update_yaxes(title_text='Count', row=1, col=2)

    mumbai_delhi_data = df[df['City'].isin(['Mumbai', 'New Delhi'])]

    avg_cost_grouped = mumbai_delhi_data.groupby(['City']).agg({'Cost_for_Two': 'mean'}).reset_index()

    # Creating a stacked bar chart
    fig_stacked_bar = px.bar(
        avg_cost_grouped,
        x='City',
        y='Cost_for_Two',
        title='Average Cost for Two in Mumbai and New Delhi',
        labels={'Cost_for_Two': 'Average Cost for Two', 'City': 'City'},
        color='City',  # This line makes the bar chart stacked
    )

    # Adjusting the layout for a better appearance 
    fig_stacked_bar.update_layout(
        xaxis_title='City',
        yaxis_title='Average Cost for Two',
        width=800,  # Setting the width of the figure
        height=500,  # Setting the height of the figure
    )

    table_columns = ['Name', 'Rating', 'CashBack', 'City', 'Locality','Discount','Cost_for_Two']

    # Creating a table trace for Mumbai
    table_mumbai = go.Figure(data=[go.Table(
        header=dict(values=table_columns),
        cells=dict(values=[mumbai_data[col] for col in table_columns])
    )])

    # Setting up the title for the table in Mumbai
    table_mumbai.update_layout(
        title='Data for Mumbai',
        title_x=0.5,  # Setting the title position along the x-axis
    )

    # Creating a table trace for New Delhi
    table_delhi = go.Figure(data=[go.Table(
        header=dict(values=table_columns),
        cells=dict(values=[delhi_data[col] for col in table_columns])
    )])

    table_delhi.update_layout(
    title='Data for New Delhi',
    title_x=0.5,  # Setting the title position along the x-axis
    )

    # Filter out data for restaurants with Home_Delivery = True
    delivery_true_data = df[df['Home_Delivery'] == 'TRUE']

    # Count the number of such restaurants in each city
    city_delivery_counts = delivery_true_data['City'].value_counts()

    # Creating a pie chart for all cities
    fig_1 = px.pie(
        names=city_delivery_counts.index,
        values=city_delivery_counts.values,
        title='Home Delivery which is Available Across Cities',
        labels={'City': 'City'},
    )

    fig_1.update_layout(
        height=400,  # Setting the height of the entire figure
        width=800,   # Setting the width of the entire figure
    )

    # Filter out data for restaurants with Home_Delivery = False
    delivery_false_data = df[(df['Home_Delivery'] == 'FALSE') & (df['City'].isin(['Mumbai', 'New Delhi']))]

    # Count the number of such restaurants in each city
    city_delivery_counts_false = delivery_false_data['City'].value_counts()

    # Creating a pie chart for all cities
    fig_2 = px.pie(
        names=city_delivery_counts_false.index,
        values=city_delivery_counts_false.values,
        title='Home Delivery which is Not Available Across Cities',
        labels={'City': 'City'},
    )

    fig_2.update_layout(
        height=400,  # Set the height of the entire figure
        width=800,   # Set the width of the entire figure
    )

    
    # Combinning the two plots into a single HTML
    graph_html = fig.to_html(full_html=False)+ fig_stacked_bar.to_html(full_html=False) +table_mumbai.to_html(full_html=False) + table_delhi.to_html(full_html=False)+ fig_1.to_html(full_html=False)+ fig_2.to_html(full_html=False)

    # Passing the HTML content to the template
    context = {'graph_html': graph_html}
    return render(request, 'plot.html', context)
