import pandas as pd
import uuid



class VisualDataframe:
    """Class representing the dataframe visualized in a page."""
    def __init__(self, df_id: uuid.UUID, title: str, df: pd.DataFrame):
        self.df_id = df_id
        self.title = title
        self.df = df
    
    def df_html(self):
        html = [f'<table class="dataframe table table-striped">']

        # Header
        html.append('<thead><tr>')
        for col in self.df.columns:
            html.append(f'<th>{col}</th>')
        html.append('</tr></thead>')

        # Body
        html.append('<tbody>')
        for row_idx, row in self.df.iterrows():
            html.append('<tr>')
            for col in self.df.columns:
                value = row[col]
                cell_id = f'{self.df_id}_{col}_{row_idx}'
                html.append(f"<td><input type='text' class='cell' id='{cell_id}' value='{value if value is not None else ""}'></td>")
            html.append('</tr>')
        html.append('</tbody></table>')


        return ''.join(html)
    