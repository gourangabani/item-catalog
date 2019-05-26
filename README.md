# Item-Catalog Project

The Item-Catalog Web Application essentially allows an user to use basic CRUD
functionality to view, and edit catalog items (post-authentication). The
application uses Google OAuth for authentication and authorisation,
and outputs the data in JSON if required (API endpoint).

#### Requisites

The following softwares should be installed before executing the script.
Links to download the same have been are given below:

**VirtualBox:** The software that runs a virtaul setup of a linux server on a
virtual machine.
https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

**Vagrant:** The software that configures the VM and facilitates the sharing
of files between the host computer and the VM's filesystem.
https://www.vagrantup.com/downloads.html

The following data sets and vagrant environments should also be downloaded:

**vagrantfile:** The vagrant setup used to configure the server environment.
https://github.com/udacity/fullstack-nanodegree-vm

#### Running the virtual machine

In order to run the virtual machine after installation, change the current
directory using `cd` to the vagrant folder downloaded in the previous step
and then type `vagrant up`. After that, type `vagrant ssh` to log the
terminal into the virtual machine, and then change the directory again by
typing `cd /vagrant` in order to access the shared folder between the host
machine and the virtual machine. Now, scripts can be executed the way they
would be on an actual linux server.

To log out of the virtual machine, type `exit` at the shell prompt. In order
to turn the virtual machine of type `vagrant halt`.

#### Running the application

After vagrant is up and running, the application can be run by first setting up
the database, in case if it doesn't exist. This can be done by executing the
`database_setup.py` Python script, which will create a database in the root
vagrant director. This database can then be populated with sample data using
the `sample_data.py`, which when executed will populate some sample categories
and items in the catalog database. Although not necessarily, this step is
certainly recommended. After setting up the database, the Python script
`web_server.py` should be executed in order to boot the server. The application
can then be accessed via the URL: http://localhost:8000.

In order to add, edit or delete an item, the user will have to authenticate
himself/herself first, using his/her Google account. In order to access the
application's JSON API endpoint, the URL: http://localhost:8000/catalog.json
should be visited.

###### Thank You! Happy Browsing! 
