# Docker Flask application template

## Introduction

This project is a Flask application that provides a template for building RESTful APIs
using Docker and Flask.
It includes a basic Flask application with a Swagger UI endpoint.

## Prerequisites

- Docker should be installed on your system. You can download it
  from [here](https://www.docker.com/get-started).

## Installation

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/enricoGiga/888SpectateDemoAPI.git
   
  
   cd project-directory

## Usage

1. Clone the repository.
2. Navigate to the project directory.
3. Build the Docker image.
4. Run the Dockers container:
   ```bash
   docker-compose up
5. Once the Docker container is up and running, you can access the Swagger UI by visiting
   the following URL in your web browser: http://localhost:5000/swagger-ui

## Troubleshooting

If you encounter any issues during the installation or execution of the project, please
ensure that your Docker setup is correct and that there are no conflicts with existing
services on your machine.



## Some useful commands:
- Access to your docker container with:
```shell
docker container exec flask_api_container sh -c "<your linux command here>" 
docker-compose exec app sh -c "<your linux command here>"
  ```
- Run flake8:
```shell
docker-compose run  app sh -c "flake8"   
```
- Run the unit tests:
```shell
docker-compose run app sh -c "pytest tests/**" 
docker-compose run app sh -c "python manage.py test"
```


## Deploying a CI/CD pipeline
- Linting (Enforce coding standards, improve code quality, catch errors early in the design cycle)
- Unit tests ( Checks code at the component level, exploses problems closer to the code, unit tests must be
 fast running)

# Continuous Delivery and Deployment.
- In this part of the development cycle, the integrated code is compiled into artifact and stored.
 To further improve the quality of the product, the artifacts can be used for additional testing before
they're made available for deployment. And in a full continuous deployment cycle, artifacts are deployed
to live environments which could be used for further testing or even production use.
