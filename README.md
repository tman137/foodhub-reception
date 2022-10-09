# Software for the reception of Foodhub Munich

The [Foodhub](https://foodhub-muenchen.de/) in Munich is a supermarket owned and operated by it's members. 
At the reception desk members can scan their membership card and this software will query our odoo system to give a feedback whether the member is allowed to shop or not.

### Prerequisites
The software is written in python3. The following libraries are used:
* [python-statemachine](https://pypi.org/project/python-statemachine/)
* [pygame](https://www.pygame.org/news)

The font Barlow has to be installed

### Deployment
* At the reception desk a raspberry pi with a display was put in place, which upon boot starts up the software &rarr; Plug and Play
* The raspberry pi needs to be connected to the internet via Ethernet, to the Barcode scanner via USB and the pi as well as the screen need to be powered via USB 3.0 and Micro USB, respectively
* All resources (sounds, background, etc) are placed within this repository
* The font "Barlow" has to be installed
* The program can be started manually with `python3 src/reception.py <odoo_url> <odoo_database> <odoo_email> <odoo_password>`

### Software description
* The software runs in an infinite loop and querys, whether input from the barcode scanner was received
* As soon as a complete barcode was received, a query via xmlrpc to the specified Odoo instance is conducted.
* Depending on the shopping status of the member a green or red animation is shown and a sound is played, indicating whether the member is allowed to shop or not.
* If the member is not allowed to shop, the membership status will be shown as well
* Afterwards the software will wait for another barcode

### Setup script
* Flash a standard raspbian image on your sd card 
* enable ssh in raspbian
* copy the initialize_pi.sh script to your raspberry
* ssh to your raspberry and run ./initialize_pi.sh <odoo_url> <odoo_database> <odoo_email> <odoo_password>

### TODOs 
* Throw an exception if barlow is not installed
