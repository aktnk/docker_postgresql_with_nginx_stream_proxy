from dotenv import load_dotenv
import os

load_dotenv()

DB_USER=os.getenv('POSTGRES_USER')
DB_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DB_DATABASE=os.getenv('POSTGRES_DB')
DB_HOST=os.getenv('HOST')

if __name__=="__main__":
    print(f"{DB_USER},{DB_PASSWORD},{DB_DATABASE},{DB_HOST}")