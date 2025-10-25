from flask import Flask, url_for, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pandas as pd
import uuid
from src.convert_df import df_html

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
        sessions_dataframes[session["session_id"]] = pd.DataFrame({})
    if session["session_id"] not in sessions_dataframes.keys():
        sessions_dataframes[session["session_id"]] = pd.DataFrame({})

@app.route('/')
def index():        
    return render_template('test.html')
    
    

@app.get("/get_df")
def get_df():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    return jsonify({
        'html': df_html(df),
        'columns': list(df.columns)
    })
    
@app.post("/add_column")
def add_column():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    
    data = request.get_json()
    df[data.get("column_name", f'Colonna_{len(df.columns) + 1}')] = '' 
    
    return jsonify({
        'success': True,
        'html': df_html(df)
    })
    
@app.post("/update_cell/")
def modify_cell():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    data = request.get_json()
    print(data.get("value"))
    df.at[int(data.get("row")) ,data.get("column")] = data.get("value")
    
    return jsonify({
        'success': True,
        'html': df_html(df)
    })
    
    
@app.get("/add_row")
def add_row():
    df: pd.DataFrame = sessions_dataframes[session["session_id"]]
    df.loc[len(df)] = [None for _ in df.columns]
    return jsonify({
        'success': True,
        'html': df_html(df)
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
    print(request.files)
    sessions_dataframes[session["session_id"]] = pd.read_csv(df_file)
    return jsonify({
        'success': True,
        'html': df_html(sessions_dataframes[session["session_id"]])
    })