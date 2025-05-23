# Task Manager
Task tracker project from https://roadmap.sh/projects/task-tracker

## Usage
Clone or download the repository and access the ``task-manager`` file with your CLI

Upon entrance, type ``python taskmanager.py`` or ``py taskmanager.py`` to run the application with python

Have Fun ^^

## Commands
Task Manager is comprised of the following commands:
* ``help``
* ``add``
* ``update``
* ``mark-in-progress``
* ``mark-done``
* ``list``
* ``delete``
* ``exit``

Each of these commands should be prefixed by ``tm``, the **T**ask **M**anager command prefix.

*e.g.* ``tm add "Bake a cake"``

## JSON
This program uses a single JSON file to store information. If you have any problems with this file, make sure to have it on the ``task_storage`` folder, that its name is ``tasks.json`` and its inner content is a single empty javascript object ``{}``
