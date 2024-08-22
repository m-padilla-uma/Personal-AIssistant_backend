import os
import time
import openai
from openai import OpenAI, RateLimitError

# Get OPEN_AI_API_KEY:
# print(os.environ.get("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
# Exponential backoff parameters
max_retries = 5  # maximum number of retries
retry_delay = 1  # initial delay in seconds

# Function to handle the API request with retry logic
def fetch_response_with_backoff():
    global retry_delay
    retries = 0
    while retries < max_retries:
        try:
            # Make the API request
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say this is a test"}],
                stream=True,
            )

            # Process the stream
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
            break  # Exit the loop if successful

        except RateLimitError:
            # If we hit the rate limit, wait and retry
            retries += 1
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponentially increase the delay

        except Exception as e:
            # Handle other OpenAI errors
            print(f"OpenAI API error: {e}")
            break

# Call the function to fetch the response
fetch_response_with_backoff()
