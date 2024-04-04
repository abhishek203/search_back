Clone the repo

The frontend folder contains the chrome extension

The backend folder contains the fastAPI backend
## Front end
Go to chrome://extensions/

Enable developer mode(top right)

Click Load Unpacked and upload the front_end folder as a whole

## Backend
```
cd backend
pip install -r requirements.txt
uvicorn docsearch:app --reload
```
