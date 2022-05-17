FROM python:3.10

WORKDIR /pulse

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python pulse/db.py

CMD sh launcher.sh
