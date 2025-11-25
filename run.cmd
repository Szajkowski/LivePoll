@echo off
cmd /c "" .\venv\Scripts\python.exe -m pip install -r requirements.txt
cmd /c "" .\venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000