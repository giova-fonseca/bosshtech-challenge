# bosshtech-challenge

Boss Tech challenge

Create a python file that when run functions as a command line tool to allow a user to interact with the provided data. Complete as many of the following tasks as you can, but do not spend more than four hours total on the project. You will not be penalized for failing to finish any task.

Your tool should do the following:

- Create a `setup` method that will copy the `sample_data` into the `output_data` folder.
- Create a `reset` method that will reset the state of the `output_data` folder.
- Study the different "customer integrations" and come up with a normalized data model for BOSS.tech customers & companies.
- Create a `sync` method that accepts an integration argument which will update the state of the `boss-tech.json` file based on the individual integration data.
- Create an `update` method that will allow a user to update a customer's name which has been synced to the `boss-tech.json`, this update should propagate to all "customer integrations" that have been "synced".

Have Fun!

# Helper Methods

python -m toolJson --help

1. python -m toolJson setup
2. python -m toolJson reset
3. python -m toolJson sync
4. python -m toolJson updated
