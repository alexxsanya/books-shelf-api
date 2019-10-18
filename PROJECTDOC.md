# The Great Bookshelf of Udacity
This project is a virtual bookshelf for Udacity students. Students are able to add their books to the bookshelf, give them a rating, update the rating and search through their book lists. 

As a part of the Fullstack Nanodegree, it serves as a practice module for lessons from Course 2: 
- API Development and Documentation. By completing this project, students learn and apply their skills structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.

Its built using Python3 with support of the Flask Micro-framework following
[PEP8](https://www.python.org/dev/peps/pep-0008/) standards and using Postgres as it's database.

### Why I started this project
- To enhance my development skills handling things like 
    - API & Product documentation
    - API development.
    - Building reliable API endpoints

## Getting Started.
Postgres
Below are the various thing to do to get started

### Prerequisites & Installation

1. Install Python

   [Click here to see the installation guide](https://realpython.com/installing-python/)

2. Install virtual environment 

   ```bash
   >> sudo apt-get install python3-pip
   >> sudo pip3 install virtualenv 
   ```

3. Install Postgres database

    [Click here to see the installation guide](https://www.postgresql.org/download/)

### Local Development

1. Create a directory and clone this repo

```bash
   >> mkdir books & cd books
   >> git clone https://github.com/alexxsanya/books-shelf-api.git
```

2. Create a virtual environment for this project and then activate it.

```bash
   >> virtualenv venv
   >> source ./venv/bin/activate
```

3. Install the project dependencies

```bash
   >> pip3 install -r requirements.txt
```

4. Run the setup.sh script to setup the database

```bash
   >> sudo chmod +x ./setup.sh
   >> ./setup.sh
```

5. Export the ENV variables in your environment

```bash
   >> export FLASK_APP=app
   >> export FLASK_ENV=development
```

6. Now you should be ready to run it locally

```bash
   >> flask run
```

The application will run on http://127.0.0.1:5000/ by default.

### Tests

Run the back-end with the scripts below

```bash
    >> dropdb bookshelf_test
    >> createdb bookshelf_test
    >> psql bookshelf_test < books.psql
    >> python test_app.py
```

## API Reference

Check the [README.md](README.md) file

## Authors

Yours Truly [alexxsanya](http://github.com/alexxsanya)


## Acknockledgement

Coach [Carthy](https://github.com/cmccarthy15)