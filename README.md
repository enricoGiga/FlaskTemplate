# Docker Flask application template

## Introduction

This project serves as a baseline template for building RESTful APIs using Flask and Postgres. 
The application is fully dockerized (see [docker-compose.yml](docker-compose.yml)). 
Additionally, it includes a GitHub workflow to automate CI.


## Description of the REST Application

The Flask application manages a sportsbook product, responsible for handling sports, events, and selections. 
The screenshot below illustrates the display of sports, events, and selections (for reference only, no GUI implementation required):
![UI-example.png](images%2FUI-example.png)


### A **sport** contains the following elements:
* Name 
* Slug (URL-friendly version of the name)
* Active (either true or false)  

### An **event** contains the following elements:
* Name
* Slug (URL-friendly version of the name)
* Active (either true or false)
* Type (either preplay or inplay)
* Sport
* Status (Pending, Started, Ended, or Cancelled)
* Scheduled start (UTC datetime)
* Actual start (created at the time the event's status changes to "Started")

### A **selection** contains the following elements:
* Name
* Event
* Price (Decimal value, to 2 decimal places)
* Active (either true or false)
* Outcome (Unsettled, Void, Lose, or Win)

### System Requirements
1. REST API demonstrating the following functionalities:
    * Creating sports, events, or selections
    * Searching for sports, events, or selections
    * The system should be able to combine N filters with an AND expression
    * Filters may be more or less complex
    * Updating sports, events, or selections
2. A sport may have multiple events
3. An event may have multiple selections
4. When all the selections of a particular event are inactive, the event becomes inactive
5. When all the events of a sport are inactive, the sport becomes inactive
6. Sports, events, and selections need to be persistently stored (SQLite is allowed)

### Examples of Filters:
* All (sports/events/selections) with a name satisfying a particular regex
* All (sports/events) with a minimum number of active (events/selections) higher than a threshold
* Events scheduled to start in a specific timeframe for a specific timezone

### Database structure:
![database_structure.png](images%2Fdatabase_structure.png)

## Prerequisites
- Docker should be installed on your system. You can download it
  from [here](https://www.docker.com/get-started).

## Installation
1. Clone this repository to your local machine and navigate to the local directory:

   ```bash
   git clone https://github.com/enricoGiga/888SpectateDemoAPI.git
   cd project-directory

2. Set up the Dockers container:
   ```bash
   docker-compose up
3. Once the Docker container is up and running, you can access the Swagger UI by visiting
   the following URL in your web browser: http://localhost:5000/swagger-ui 



## Some useful commands:
- Access to your docker container with:
```shell
docker container run flask_api_container sh -c "<your linux command here>" 
docker-compose run app sh -c "<your linux command here>"
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
## Configure Pycharm
If you use a profession edition of Pycharm, you can debug the application on your docker container.
Here how to configure:
![pycharm1.png](images%2Fpycharm1.png)
![pycharm2.png](images%2Fpycharm2.png)

## CI pipeline descriptions
![CI.png](images%2FCI.png)

The above image shows the steps of the CI pipeline defined [here](.github%2Fworkflows%2Fci.yml) with GithHub actions.
### Login to docker hub
This step is used to log in to Docker Hub using the docker/login-action action. It uses the Docker Hub username and token stored as secrets in the GitHub repository.
### Checkout
This step is used to log in to Docker Hub using the 'docker/login-action' action. It uses the Docker Hub username and token stored as secrets in the GitHub repository.
### Coverage
This step calculates the test coverage using the command docker-compose exec -T app sh -c "pytest --cov=server tests/*". This step fails if the coverage is under 70%, as defined in the configuration file [.coveragerc](flask_template%2F.coveragerc)

#### Lint
Lint: This step performs linting on the code using the commands:

* **flake8** with the specified ignore flags for the Python files.
* **pylint** with disabled warnings. The _continue-on-error_ parameter is set to true, which means that if there are any linting errors, the job will continue to run rather than stopping.


# Continuous Delivery and Deployment.
[(AWS Continuous delivery will be released soon)]
- In this part of the development cycle, the integrated code is compiled into artifact and stored.
To further improve the quality of the product, the artifacts can be used for additional testing before
they're made available for deployment. And in a full continuous deployment cycle, artifacts are deployed
to live environments which could be used for further testing or even production use.
