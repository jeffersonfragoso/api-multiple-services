# API to Publish Numbers using multiple services

This project has the API Rest that receive numbers from multiple services using the RabbitMQ.

## Table of Contents

* [API to Publish Numbers using multiple services](#api-to-publish-numbers-using-multiple-services)
  + [Table of Contents](#table-of-contents)
  + [Requirements](#requirements)
  + [Setup](#setup)
  + [Running](#running)
  + [Get the list of numbers from API](#get-the-list-of-numbers-from-api)
  + [Access the API documentation](#access-the-api-documentation)
  + [Lint](#lint)
  + [Tests](#tests)

## Requirements

To run this project, you need to install the [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/).

## Services

There are five services in this project:

* Even numbers: service responsible for generate the even numbers when requested
* Odd numbers: service responsible for generate the odd numbers when requested
* Publish numbers: service responsbile for request number from even numbers service and odd numbers service at each 500 milliseconds and publish the numbers bigger than 100000
* Api consumer: service responsible for consume the numbers that was publish by publish numbers service and added the number inside the database
* Api: service that has the API service to list all the numbers generated

## Setup

To set up the container, you need to execute:

``` console
docker-compose build
```

This command will build the all containers that need to run

## Running

You can run all services with one single command:

``` console
docker-compose up
```

So this command will start all containers at once

## Get the list of numbers from API

To get the list of numbers that already was generated:

``` console
curl -X GET http://localhost:8000/numbers 
```

The response will be something like:

``` json
{
  "count": 198,
  "data": [
    156702, 192604, 229140, 230010, 192722, 364070, 497388, 977000, 176412, 161102, 433570, 168510, 311520, 207270, 486312, 116482, 422206, 176548, 103734, 573000
  ]
}
```

This response is paginate. So, to navegate between the pages you need to execute the command:

``` console
curl -X GET http://localhost:8000/numbers -d offset=20 -d limit=20
```

Now, you will get the numbers from the 20th until the 40th number

## Access the API documentation

You can access the API documentation and execute requests to the API by http://localhost:8000/apidocs/

## Lint

To check the lint of code

``` console
make lint
```

## Tests

To execute the unit tests

``` console
make tests
```
