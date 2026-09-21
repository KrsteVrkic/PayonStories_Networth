@echo off
cd /d "C:\Users\krste\Documents\PayonStories_Networth"

start "" http://127.0.0.1:8000

python -m uvicorn app.main:app