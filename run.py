# Author: Sakthi Santhosh
# Created on: 16/10/2023
from dotenv import load_dotenv

from app import create_app

def run():
    load_dotenv()

    app_handle = create_app(config="development")

    app_handle.run(debug=True, host="0.0.0.0")

if __name__ == "__main__":
    run()
