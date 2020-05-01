FROM python:3
ADD app.py /
ADD index.html /
ADD requirements.txt /
ADD campusmap.png /
RUN pip install -r requirements.txt 
CMD [ "python", "./app.py"]
