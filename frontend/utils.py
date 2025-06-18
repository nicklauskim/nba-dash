# Useful functions to use in app for plotting and formatting data

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import gaussian_kde


def formatted_table(data):
    pass


def draw_nba_half_court():
    fig = go.Figure()

    fig.update_layout(
        plot_bgcolor="#F8F8F8",
        autosize=False,
        font=dict(family="Inter", size=14),
        height=650, width=650,
        xaxis=dict(
            visible=False,
            range=[-250, 250],
            scaleanchor='y',
            scaleratio=1,
            fixedrange=True
        ),
        yaxis=dict(
            visible=False,
            range=[0, 470],
            fixedrange=True
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )
    
    # Draw court lines
    width = 500
    length = 470
    key_length = 190
    inner_key_width = 120
    outer_key_width = 160
    backboard_width = 60
    backboard_offset = 40
    neck_length = 5
    hoop_radius = 7.5
    hoop_center_y = backboard_offset + neck_length + hoop_radius
    restricted_area_radius = 40
    three_point_radius = 237.5
    three_point_side_radius = 220
    three_point_side_length = 140
    
    # Perimeter
    fig.add_trace(go.Scatter(x=[width/2, width/2, -width/2, -width/2, width/2], 
                                y=[length, 0, 0, length, length], 
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=4, showlegend=False))
    # Key
    fig.add_trace(go.Scatter(x=[outer_key_width/2, outer_key_width/2, -outer_key_width/2, -outer_key_width/2], 
                                y=[0, key_length, key_length, 0], 
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # Backboard
    fig.add_trace(go.Scatter(x=[-backboard_width/2, backboard_width/2], 
                                y=[backboard_offset, backboard_offset], 
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # Neck
    fig.add_trace(go.Scatter(x=[0, 0], 
                                y=[backboard_offset, backboard_offset + neck_length], 
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # Foul Circle
    x_grid = np.linspace(start=-inner_key_width/2, stop=inner_key_width/2, num=360)
    # top half
    fig.add_trace(go.Scatter(x=x_grid,
                                y=np.sqrt((inner_key_width/2)**2 - x_grid**2) + key_length,
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # bottom half
    fig.add_trace(go.Scatter(x=x_grid,
                                y=-np.sqrt((inner_key_width/2)**2 - x_grid**2) + key_length,
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, line_dash='dash', showlegend=False))
    # Hoop
    x_grid = np.linspace(start=-hoop_radius, stop=hoop_radius, num=360)
    # top half
    fig.add_trace(go.Scatter(x=x_grid,
                                y=np.sqrt((hoop_radius)**2 - x_grid**2) + hoop_center_y,
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # bottom half
    fig.add_trace(go.Scatter(x=x_grid,
                                y=-np.sqrt((hoop_radius)**2 - x_grid**2) + hoop_center_y,
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # Restricted Circle
    x_grid = np.linspace(start=-restricted_area_radius, stop=restricted_area_radius, num=360)
    fig.add_trace(go.Scatter(x=x_grid,
                                y=np.sqrt((restricted_area_radius)**2 - x_grid**2) + hoop_center_y,
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # 3-Point Line
    # circle
    x_grid = np.linspace(start=-220.5, stop=220.5, num=360)
    fig.add_trace(go.Scatter(x=x_grid,
                                y=np.sqrt((three_point_radius)**2 - x_grid**2) + hoop_center_y,
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    # line
    fig.add_trace(go.Scatter(x=[-three_point_side_radius, -three_point_side_radius], 
                                y=[0, three_point_side_length],
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))
    fig.add_trace(go.Scatter(x=[three_point_side_radius, three_point_side_radius], 
                                y=[0, three_point_side_length],
                                hoverinfo='skip',
                                mode='lines', line_color='#000000', line_width=2, showlegend=False))

    fig.add_shape(type='rect',
        x0=-outer_key_width/2, y0=0, x1=outer_key_width/2, y1=key_length,
        line=dict(color='black', width=1),
        fillcolor="#BFA78A",
        layer='below')

    return fig


def plot_events(df, fig, title="Play Chart", **kwargs):
    x = df['xlegacy']
    y = df['ylegacy'] + 40  # Align with half-court

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(size=8, color='orange', opacity=0.7, line=dict(width=1, color='black')),
        name='Events',
        hoverinfo='text',
        text=df['actiontype'] + ' ' + df['shot_distance'].astype(str) + ' ft.' + '<br>' + df['subtype']
    ))

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=20, family='Inter')
        )
    )

    return fig


def shot_type_heatmap(df, fig, title="Play Location Density Heatmap", **kwargs):
    from scipy.stats import gaussian_kde
    import numpy as np
    import plotly.graph_objects as go

    df = df.rename(columns={'xlegacy': 'X', 'ylegacy': 'Y'})
    df['Y'] += 40  # Align with half-court layout

    df = df[(df['X'] >= -250) & (df['X'] <= 250) & (df['Y'] >= 0) & (df['Y'] <= 470)]

    x = df['X'].values
    y = df['Y'].values

    # KDE smoothing
    kde = gaussian_kde(np.vstack([x, y]), bw_method=0.3)

    xi, yi = np.mgrid[-250:250:300j, 0:470:300j]  # xi is x (width), yi is y (height)
    zi = kde(np.vstack([xi.ravel(), yi.ravel()])).reshape(xi.shape)

    # Smooth, clip extreme values
    zi = np.sqrt(zi)
    z_cap = np.percentile(zi, 99)
    zi = np.clip(zi, 0, z_cap)

    fig = go.Figure(data=go.Heatmap(
        x=xi[:, 0],      
        y=yi[0],       
        z=zi.T,        
        colorscale='Bluered',    # 'Viridis', 'Cividis', 'Blues', 'Reds', etc.
        zsmooth='best',
        hoverinfo='skip',
        showscale=False,
        colorbar=dict(
            title='Density',
            ticklen=3,
            thickness=15,
            outlinewidth=0,
        ),
        **kwargs
    ))

    fig.update_layout(
        autosize=False,
        height=650,
        width=650,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            visible=False,
            range=[-250, 250],
            scaleanchor="y",
            scaleratio=1,
            fixedrange=True
        ),
        yaxis=dict(
            visible=False,
            range=[0, 470],
            fixedrange=True
        ),
        plot_bgcolor='white',
        font=dict(family="Inter", size=14),
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=20, family='Inter')
        )
    )

    return fig



def shot_type_bar_chart(df, **kwargs):
    pass




def scoring_timeline(df):
    df_sorted = df.sort_values(by="game_minute")
    df_sorted["cumulative_points"] = df_sorted["points"].cumsum()
    
    fig = px.line(
        df_sorted, 
        x="game_minute", 
        y="cumulative_points", 
        title="Scoring Timeline",
        labels={"game_minute": "Game Minute", "cumulative_points": "Cumulative Points"}
    )
    return fig

