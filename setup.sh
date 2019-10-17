service postgresql start
su - postgres bash -c "psql < /home/alex/Documents/Udacity/projects/bookshelf/db_setup.sql"
su - postgres bash -c "psql bookshelf < /home/alex/Documents/Udacity/projects/bookshelf/books.psql"
su - postgres bash -c "psql bookshelf_test < /home/alex/Documents/Udacity/projects/bookshelf/books.psql"