FROM jjanzic/docker-python3-opencv
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD python main.py