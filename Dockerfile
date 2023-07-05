FROM python:3

WORKDIR /strava_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./strava_bot_main.py" ]