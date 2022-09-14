def get_traces_and_layout(title: str,
                          labels: list[str],
                          x_data: list[list],
                          y_data: list[list]):
    """
    This function converts regular lists to the data and layout from the dash module.
    Just send label, x axis data and y axis data respectively for each graph.
    Example:
    labels = ['graph1', 'graph2']
    x_data = [[0, 1, 2], [0, 1, 2]]
    y_data = [[2, 6, -1], [100, 13, 5]]

    :param title: Title of the graphs block
    :param labels: Labels of each separate line
    :param x_data: list of lists with graph x axis values
    :param y_data: list of lists with y data values
    :return: data, layout
    """

    if len(labels) > 21:
        raise IndexError("Too many lines on one graph. Only 21 graphs are allowed")

    if not (len(labels) == len(x_data) == len(y_data)):
        raise IndexError("All parameters must be of the same length")

    colors = ["rgb(230, 25, 75)",
              "rgb(60, 180, 75)",
              "rgb(255, 225, 25)",
              "rgb(0, 130, 200)",
              "rgb(245, 130, 48)",
              "rgb(145, 30, 180)",
              "rgb(70, 240, 240)",
              "rgb(240, 50, 230)",
              "rgb(210, 245, 60)",
              "rgb(250, 190, 190)",
              "rgb(0, 128, 128)",
              "rgb(230, 190, 255)",
              "rgb(170, 110, 40)",
              "rgb(255, 250, 200)",
              "rgb(128, 0, 0)",
              "rgb(170, 255, 195)",
              "rgb(128, 128, 0)",
              "rgb(255, 215, 180)",
              "rgb(0, 0, 128)",
              "rgb(128, 128, 128)",
              "rgb(0, 0, 0)"]
    colors = colors[:len(labels)]

    line_size = [2 for x in range(len(labels))]

    traces = []

    for i in range(len(x_data)):
        traces.append(dict(
            x=x_data[i],
            y=y_data[i],
            mode='lines+markers',
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
            name=labels[i],
        ))

    layout = dict(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickcolor='rgb(204, 204, 204)',
            tickwidth=2,
            ticklen=5,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                xanchor='right', yanchor='middle',
                                text=f'{label} {y_trace[0]}',
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[-1],
                                xanchor='left', yanchor='middle',
                                text=f'{y_trace[-1]} {label}',
                                font=dict(family='Arial',
                                          size=16),
                                showarrow=False))
    # title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text=title,
                            font=dict(family='Arial',
                                      size=30,
                                      color='rgb(37,37,37)'),
                            showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Source: bot rest API',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    layout['annotations'] = annotations

    return traces, layout
