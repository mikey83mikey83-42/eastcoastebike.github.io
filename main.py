from square import Square
from square.core.api_error import ApiError
import os

# Initialize the Square client
# It's best practice to use environment variables for your token
client = Square(
    token=os.environ.get('SQUARE_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN'),
    environment='production'  # Change to 'production' when you're ready to go live
)

def main():
    try:
        # Example: List locations to verify the connection
        response = client.locations.list_locations()
        
        # The new SDK allows direct iteration over the response
        for location in response:
            print(f"Connected to: {location.name} ({location.id})")
            
    except ApiError as e:
        print("Square API Error:")
        for error in e.errors:
            print(f"  - {error.category}: {error.detail}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
    
