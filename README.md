# URL Shortener API

The URL Shortener API is a service that allows users to create shortened versions of long URLs.

## Getting Started

To get started with the URL Shortener API, follow the instructions below.

### Prerequisites

- Python (version 3.6 or higher)
- Flask (version 2.0.1 or higher)
- Flask-RESTX (version 0.5.1 or higher)
- Other dependencies (specified in requirements.txt)

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/url-shortener-api.git
2. Navigate to the project Directory
   cd url-shortener-api
   
4.  Install Dependecies
   ```shell
    pip install -r requirements.txt
   ```
6. Setup the app
   ```shell
   export FLASK_APP=run.py
7. Start the app
   ```shell
   python run.py

### API Endpoints
  The following endpoints are available in the API:
  
<ul>
Create Shortened URL
<li>URL: POST /api/shorten-url</li>
<li>Description: Creates a shortened version of a long URL</li>
</ul>
<p>  Request Body:{
      "url": "https://example.com/long-url"
    }
</p>
<p>  
    Response
    {
      "shortUrl": "https://slt.ly/abcd123"
    }
</p>

