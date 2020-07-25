# airnow-visualize
A Dash App using Plotly and Python (and others) to visualize data from Airnow.gov

## install
- requirement: `python3.6 or later`
```
git clone https://github.com/binh-bk/airnow-visualize.git
cd airnow-visualize
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn app:server
```
the app should boot up, by default, the local address is `localhost:8000`

- to stop the app, press `Ctrl + C`
- to run the app in the background `gunicorn app:server &`
- to run the app in a server with two workers gunicorn app:server --workers 2 --bind 0.0.0.0:8000`

## screenshot

  <p align="center">
    <img src="img/screenshot.png"/>
  </p
