from flask import Flask,jsonify,request
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app=Flask(__name__)

def get_db_connection():
    conn=psycopg2.connect(
        user=os.getenv('user'),
        host=os.getenv('host'),
        password=os.getenv('password'),
        port=os.getenv('port'),
        database=os.getenv('database')
    )
    print("Database connection established")
    return conn

