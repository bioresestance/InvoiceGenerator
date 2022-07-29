# Invoice Generator

Simple python script to generate a PDF invoice for my business. There is no GUI, all commands are done in the command line. I currently only do billing of engineering hours, so the tool will only work on being a number of engineering consulting hours to a client.

# How to use

1. First clone the repository from Github using `git clone {url}`.
2. Pip install the required packages for the project. 
3. run the script in a command line. Got to the next section for options to pass.


# Script Arguments

You can run the script with the following options:

| Name | Short Option | Long Option| Description |
|------|--------------|------------|-------------|
|Client| -c | --client   | Name of the client to bill |
|Hours| -h | --hours   | Number of hours to bill the client at |
|Start Date| -s   | --start   | Date to start the billing from |
|End Date| -e | --end   | Last date to bill the client from |


# Script Options

The script will use a yaml file to store the configuration settings. By default, this file is called `config.yml`.


# Credits
This project is based on the tutorial at [stackabuse](https://stackabuse.com/creating-pdf-invoices-in-python-with-borb/).
