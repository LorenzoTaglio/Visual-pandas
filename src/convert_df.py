import pandas as pd


def df_html(df: pd.DataFrame):
    html = ['<table class="dataframe table table-striped">']
    
    # Header
    html.append('<thead><tr>')
    for col in df.columns:
        html.append(f'<th>{col}</th>')
    html.append('</tr></thead>')
    
    # Body
    html.append('<tbody>')
    for row_idx, row in df.iterrows():
        html.append('<tr>')
        for col in df.columns:
            value = row[col]
            cell_id = f'{col}_{row_idx}'
            html.append(f"<td><input type='text' class='cell' id='{cell_id}' value='{value if value is not None else ""}'></td>")
        html.append('</tr>')
    html.append('</tbody></table>')
    
    
    return ''.join(html)