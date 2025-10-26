from flask import Flask, url_for, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pandas as pd
import uuid
from src.dataframe import VisualDataframe
import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

Session(app)
CORS(app)


sessions_dataframes = {}

@app.before_request
def ensure_session_id():
    """Create session id if not existent"""
    # testdf=pd.DataFrame({"a":pd.Series([1,2,3,4]),"b":["eenie","meenie","money", "moo"]})
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        sessions_dataframes[session["session_id"]] = {}
    if session["session_id"] not in sessions_dataframes.keys():
        sessions_dataframes[session["session_id"]] = {}

@app.route('/')
def index():        
    return render_template('index.html')
    
    

@app.get("/get_df")
def get_df():
    dfs = sessions_dataframes[session["session_id"]]
    return jsonify({
        'success': True,
        'dataframes': [{
            "id": df.df_id,
            "name": df.title,
            "html": df.df_html()
        }for _, df in dfs.items()]
    })
    
@app.post("/add_column")
def add_column():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    
    data = request.get_json()
    df[data.get("column_name", f'Colonna_{len(df.columns) + 1}')] = '' 
    
    return jsonify({
        'success': True,
        'html': " "
    })
    
@app.post("/update_cell")
def modify_cell():
    data = request.get_json()
    df_id = uuid.UUID(data.get("df_id"))
    df: VisualDataframe = sessions_dataframes[session["session_id"]][df_id]
    print(data.get("value"))
    df.at[int(data.get("row")) ,data.get("column")] = data.get("value")
    
    return jsonify({
        'success': True,
        'html': df.df_html()
    })
    
    
@app.get("/add_row")
def add_row():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    df.loc[len(df)] = [None for _ in df.columns]
    return jsonify({
        'success': True,
        'html': " "
    })
    
@app.get("/columns_len")
def columns_len():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    print(df)
    print(len(df.columns))
    return jsonify({
        'success': True,
        'columnsLen': len(df.columns)
    })
    
@app.post("/import_dataframe")
def import_df():
    df_file = request.files['file']
    df_id = uuid.uuid4()
    
    while df_id in sessions_dataframes[session["session_id"]]:
        df_id = uuid.uuid4()

    visual_df = VisualDataframe(df_id, df_file.filename, pd.read_csv(df_file))
    sessions_dataframes[session["session_id"]][df_id] = visual_df
    
    return jsonify({
        'success': True,
        'df_id': df_id,
        'name': visual_df.title,
        'html': visual_df.df_html()
    })