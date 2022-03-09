# docs_python_lib
Set of methods to working with google docs api

## Docker
1. Follow step 6 in <b>Local</b> part (Get Google API Oauth keys)
2. 

## Local
1. Install python 3.9 locally on your system from [the official web-page](https://www.python.org/).
2. Clone the repository
    ```
   git clone https://github.com/Moonsteel22/docs_python_lib.git
   ```
3. Create virtual environment using `python3 -m venv venv` command. It will create a virtual environment in a nested `venv/` directory. Creating virtual environment is done once after cloning this repo - no need to repeat.
    Sometimes you may be asked to install `python3-venv` into your machine - in most cases you will see commands that need to be executed as a prompt, e.g.
    ```
   sudo apt update
   sudo apt install python3-venv
   ```
4. Activate virtual environment. You need to activate virtual environment every time you want to work with the backend part.
    Use `source venv/bin/activate` if you use Linux/macOS or `venv\Scripts\activate.bat` if you use Windows.
    You will see `(venv)` in a shell prompt if you create and activate a virtual environment correctly.
5. Install dependencies using `pip install -r requirements.txt` command **inside virtual environment**.
6. Get Google API OAuth keys.
    - Create a project here: https://console.developers.google.com/
    - Enable Drive and Docs APIs for your project: follow [this](https://console.cloud.google.com/apis/library/docs.googleapis.com) and this [link](https://console.cloud.google.com/apis/library/drive.googleapis.com), select your project and enable APIs.
    - Go to the [Credentials Page](https://console.developers.google.com/apis/credentials) and click on "Create Credentials"
    - Choose OAuth client ID, choose "Desktop app" as an application type, type any name and download provided credentials as json file (you can find it on the creds page OAuth 2.0 Client IDs table). Name this file as `credentials.json` and place it in the root of the backend part.
    - Choose OAuth client ID, choose "Web application" as an application type, type any name, add `http://127.0.0.1:8000/api/accounts/google/login/callback/` as an Authorized redirect URI (hostname may be another if you want your app to be explorable not only from your local machine).
    - Copy-paste provided Client ID and Client secret, they will be required on the next step
7. Get service credentials
    - Go to: https://developers.google.com/workspace/guides/create-credentials#service-account
    - Create credentials for service account: https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account
    - Download credentials as json and rename it to credentials_service.json
    - Replace credentials_service.json to /src
8. Create `.env` file, copy-paste content of `.env.example` file into `.env` and replace `GOOGLE_SECRET_KEY` and `GOOGLE_CLIENT_ID` values with your Google OAuth keys.
9. Change `BASE_URL` and `SECRET_KEY` values in `.env` if you want your app to be explorable not only from your local machine.
10. Run migrations `python3 manage.py migrate`
11. Create super user `python3 manage.py createsuperuser`
12. Run server `python3 manage.py runserver 0.0.0.0:8000`
13. You will be asked to confirm google API credentials - follow instructions in the console.
14. Open back-end part on `127.0.0.1:8000` locally.
