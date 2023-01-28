# pull latest python base image
FROM python:latest

# set working directory
WORKDIR /home/dealership_app

# upgrade pip and install depedencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project file
COPY . .

# expose container port
EXPOSE 8000

RUN chmod +x /home/dealership_app/entrypoint.sh
RUN chmod +x /home/dealership_app/set_superuser.sh

ENTRYPOINT [ "/bin/bash", "/home/dealership_app/entrypoint.sh" ]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
