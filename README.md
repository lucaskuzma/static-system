# Static System

A dead simple site generator, relying on the file system for organization, since we already tend to organize our files.

An exercise in revealing the many inadequacies of the Finder.


## Install Dependencies

Outside of getting a recent Python version, this is pretty optional now.

	pipenv install
	pipenv shell

## Generate

	python generate.py


## Local Server

It may be convenient to fire up a local server.

	 npm install -g light-server 
	 light-server -s out

## Push to Host as Static Site

Surge? Netlify? Anything simpler? Can a CDN be fed directly?
