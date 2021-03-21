# Data Engineering Mini-project with Spotify Data

This repository contains my code for a data engineering mini-project I undertook on 21/03/2021. It was guided by the [3-part Data Engineering Course for Beginners](https://www.youtube.com/watch?v=dvviIUKwH7o) by [Karolina Sowinska](https://www.linkedin.com/in/karolina-sowinska-b3070b103/). 

[**Original source code by Ms. Sowinska**](https://github.com/karolina-sowinska/free-data-engineering-course-for-beginners)

## The Task

Build a data pipeline for my spotify habits using ETL

## Notes
This section contains some short notes I took while listening to the videos

### Extract
Means to download data or bring it on board

- Data vendors provide data using APIs or FTP
- Data formats can be csv, json or compressed or uncompressed

API: https://developer.spotify.com/console/get-recently-played/
Reference: [Web API Reference | Spotify for Developers](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recently-played)

Spotify data is in json

Step 1. Get the OAuth token from spotify
Step 2. Download the data using python with the help of the spotify API
Step 3. Convert the data into a tabular format

### Transform
This is like a validation stage, this is where you fix problems with the data

Potential things to check for
- Empty data
	- Is this a data vendor problem? - Call this a failure
	- Or is it a case of an event not happening? - Let it be
- Primary key
	- In this spotify case, `played_at` is the primary key
	- Impose a primary key constraint - In this column, all the values must be unique
- Check for nulls
- Check that data is not too old

### Load
Loading data into databases

Databases can be relational or non-relational

Here, we use SQLite. 

Database location types
- On-premise
- Cloud

**ORM: Object Relational Mappers**
Imagine you are writing code in python, and you want to use data on you database. ORM allows you to query data from python without using SQL. An example is SQLAlchemy.

Interact with your database(to see your data in it) using **DBeaver**.