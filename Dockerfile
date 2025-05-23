FROM python:3.13.3-slim 

WORKDIR /strava_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "bot/strava_bot_main.py" ]