# PIR_lib

PIR_lib is a personal information register API. This API will allow the
users to view, update and delete a person’s personal data. You are provided with a random
dataset with the following fields in JSON format:
- id (ID of the person)
- first_name (First name of the person)
- last_name (Last name of the person)
- email (Email address of the person)
- gender (Gender of the person)
- ip_address (IP Address v4 of person’s device)
- country_code (Country code of the person)

The file name is data.json

### Virtual environment
- Create the virtualenv
```bash 
virtualenv -p python3.8 venv
```
- Activate the virtualenv
```bash
source venv/bin/activate
```

### How to Run It
#### Locally
- Install requirements as usual:
    ```bash
       pip install -r requirements/requirements.txt
       pip install -r requirements/test-requirements.txt
    ```

- Run unit tests with coverage:
  ```bash
  coverage run -m pytest
  ```
- Run the FastAPI app using:
  ```bash
  uvicorn app.main:app --reload
  ```
- Open API Documentation after running to try out the API: http://127.0.0.1:8000/docs


#### Or via Dockerfile
- Build docker image of `PIR_lib`
  ```bash
  docker build -t PIR_lib_image .
  ```
- Start the Docker Container based on the image of `PIR_lib`
  ```bash
  docker run -d --name PIR_lib_container -p 80:80 PIR_lib_image
  ```
- Now you should be able to check it in your Docker container's URL, for example: http://127.0.0.1/docs (or equivalent, using your Docker host).

### Improvement TODO:

- 
