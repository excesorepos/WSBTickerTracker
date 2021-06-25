FROM python:3.7-alpine
RUN mkdir /app
RUN apk add make automake gcc g++ subversion python3-dev gcc libxslt-dev
ADD requirements.txt /app
ADD ticker_sentiment.py /app
RUN addgroup -S wsbtracker && adduser -S wsbtracker -G wsbtracker
RUN chown -R wsbtracker: /app
USER wsbtracker
WORKDIR /app
RUN pip3 install -r /app/requirements.txt --user
RUN python3 ticker_sentiment.py