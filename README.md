## mozio-api-challenge
### Problem
**Prompt:**

As Mozio expands internationally, we have a growing problem that many transportation suppliers would like their API to be integrated into Mozio platform, to allow them to sell their transfers.

Integrating many APIs from scratch and selling their content in a unified approach is not a simple task and Mozio built its own Transfers Framework to facilitate that. Nevertheless, we still need to check the supplier's API documentation, communicate with them and integrate their code into our framework.

To assess your API knowledge, we would like you to implement Mozio API to handle the core methods that we have available. You can see the API working (under the hood, inspecting the requests made on the Network tab) on our testing website.

**Requirement:**

* Read Mozio API Integration guide.
* Implement Python methods to do search, booking (reservation), and cancellation.
* Perform one booking with the following search parameters, cancel it, and share its confirmation number:
```json
{
  "start_address": "44 Tehama Street, San Francisco, CA, USA",
  "end_address": "SFO",
  "mode": "one_way",
  "pickup_datetime": "2023-12-01 15:30",
  "num_passengers": 2,
  "currency": "USD",
  "campaign": "{your full name}"
}
```
* For the reservation, select the provider with the name "Dummy External Provider" and pick the cheapest available vehicle.
* Create a GitHub account (if you don't have one), push all your code, and share the link with us.
* Considerations - API Integration:

* API KEY to use: 6bd1e15ab9e94bb190074b4209e6b6f9
* Mozio API endpoints that should be implemented:
*   `POST /v2/search/`
*   `GET /v2/search/{search_id}/poll/`
*   `POST /v2/reservations/`
*   `GET /v2/reservations/{search_id}/poll/`
*   `DELETE /v2/reservations/{confirmation_number}`
* No need to provide any payment information for the booking flow.
* Note: Please refer to the Mozio API Integration guide for detailed information on the API and its usage.

### Solution

#### Instalation
Firstly you must download and install Python 3.10.6 on your machine according to your operating system. The download link is as follows:

[Python 3.10.6](https://www.python.org/downloads/release/python-3106/).

#### Virtual Environment for Python 3.10.6

Subsequently, the venv package for Python 3.10.6 must be installed (For guidance refer to the link [venv](https://docs.python.org/3/library/venv.html)). For example for Debian-based distributions:

`sudo apt install python3.10-venv`

The virtual environment should be created using venv `python3.10 -m venv /path/to/new/virtual/environment`. For example:

`python3.10 -m venv myvenv`

Then the virtual environment should be set up using venv `source /path/to/directory`. For example:

`source myvenv/bin/activate`

#### Installing the requiriments of the application

Run the command `pip install -r requirements.txt`.

#### Running the application
Run the `main.py` to use the application.

#### Testing
To run the tests use the following command with :
`python3 -m pytest -v tests/`