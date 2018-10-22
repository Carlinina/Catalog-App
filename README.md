# Catalog-App
Catalog App is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
In order to run this program you will need the following:

1. Computer (Windows or Mac OS)
2. Working knowlage of using the command-line.
  
## Instructions

1. Install Vagrant and VirtualBox
2. Clone the fullstack-nanodegree-vm
3. Launch the Vagrant VM (vagrant up)
4. Copy the Flask application locally in the vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM).
5. Run your application within the VM (python /vagrant/catalog/application.py)
6. Access and test the application by visiting http://localhost:8000 locally

1.  Use the psql command-line tool to create the following Views for each of the questions in the database:
  
  Question1:
  
  	CREATE VIEW popular_path AS SELECT title, slug, path FROM articles JOIN log ON log.path = CONCAT('/article/',articles.slug);
  
  Question2:
  
    CREATE VIEW popular_authors AS SELECT author, slug, path FROM articles JOIN log ON log.path = CONCAT('/article/',articles.slug);
 	  
    CREATE VIEW authors_views AS SELECT author, count(*) AS views FROM popular_authors GROUP BY author ORDER BY views DESC;
  
  Question3:

  	CREATE VIEW date_status AS SELECT DATE(time), status FROM log ORDER BY DATE(time);
  
  	CREATE VIEW date_error AS SELECT DATE(time), status FROM log WHERE status='404 NOT FOUND' ORDER BY DATE(time);

  	CREATE VIEW total_entries AS SELECT date, count(*) AS total_number FROM date_status GROUP BY date ORDER BY date ASC;
  
  	CREATE VIEW error100 AS SELECT date, count(*)*100 AS errors FROM date_error GROUP BY date ORDER BY date ASC;
  
  	CREATE VIEW percentage AS SELECT error100.date, (errors*1.00)/total_number AS percentage_errors FROM error100, total_entries WHERE total_entries.date=error100.date ORDER BY percentage_errors DESC;
  
 2. Execute 'python news_tool.py' in the command line.
 
 3. Enjoy!
 
## Example of the program's output

I will provide the file program_output_example.txt that is a copy of what the program will print out.

Q1. Number of article's views:

     " Candidate is jerk, alleges rival " --  338647 views
     " Bears love berries, alleges bear " --  253801 views
     " Bad things gone, say good people " --  170098 views
     
Q2. Number of authors' views:

     " Ursula La Multa " --  507594 views
     " Rudolf von Treppenwitz " --  423457 views
     " Anonymous Contributor " --  170098 views
     " Markoff Chaney " --  84557 views
     
Q3. Days where more than 1% of requests lead to errors:

     " 2016-07-17 " --  2.2626862468027260 % errors

