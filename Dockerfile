FROM python:3.8.6-buster

COPY seedling_model.h5 /seedling_model.h5
COPY fast.py /fast.py
COPY requirements.txt /requirements.txt
COPY seedling-sorter-71d06b77468c.json /seedling-sorter-71d06b77468c.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
