python pulse/pulse.py &
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
sleep 1
python gui/main.py
