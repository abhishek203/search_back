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

## To create vector database
Put all the files in data folder

Send POST request to http://127.0.0.1:8000/create-vector-db
