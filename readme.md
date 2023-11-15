# SubnetInfo Web Application

SubnetInfo is a Flask web application that allows users to perform network-related calculations, including finding information about a network, subnetting based on the required number of hosts, and subnetting based on the required number of subnets.

## Features

- **Host Information:** Find details about a network, including network address, broadcast address, available hosts, first address, and last address.

- **Subnetting by Hosts:** Calculate subnets based on the required number of hosts.

- **Subnetting by Subnets:** Calculate subnets based on the required number of subnets.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Flask

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/SubnetInfo.git
    cd SubnetInfo
    ```

3. Run the application:

    ```bash
    python app.py
    ```

    The application will be accessible at [http://localhost:5000/](http://localhost:5000/).

## Usage

1. Access the application in your web browser.

2. Fill in the required information in the provided forms.

3. Submit the forms to perform the desired network calculations.

## Project Structure

- `app.py`: Main Flask application file.
- `calculation.py`: Module containing network calculation functions.
- `forms.py`: Forms for user input.
- `templates/`: HTML templates for rendering pages.
- `static/`: Static files (CSS, JS, etc.) for the front-end.


