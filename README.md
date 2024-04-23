# Setup

## 1) wmata-backend
The `wmata-backend` server is hosted on [PythonAnywhere](https://www.pythonanywhere.com/) at [https://siahweehung1748.pythonanywhere.com/](https://siahweehung1748.pythonanywhere.com/).
To host your own, add a `.env` file in the root `cs4366-backend` folder with the following environment variables.

Note: To get your own `WMATA_PRIMARY_KEY` and `WMATA_SECONDARY_KEY` API keys, create a [WMATA developer account](https://developer.wmata.com/)
```
WMATA_PRIMARY_KEY=<WMATA_PRIMARY_KEY>
WMATA_SECONDARY_KEY=<WMATA_SECONDARY_KEY>
WMATA_API_URL="https://api.wmata.com/Bus.svc/json"
WMATA_MISC_API_URL="https://api.wmata.com/NextBusService.svc/json"
```
<br/>

Start the wmata-backend server
```
python wmata-backend/app.py
```
<br/>

In another terminal, expose your localhost server
```
ngrok http 5000
```
<br/>

## 2) ocr_backend + obj_detect_backend
### Google Cloud API Key
Obtain a Google Cloud API key and authenticate using [gcloud CLI](https://cloud.google.com/docs/authentication/gcloud) 

Start the `ocr_backend` & `obj_detect_backend` joint server
```
python main.py
```
In another terminal, expose your localhost server
```
ngrok http 5001
```


