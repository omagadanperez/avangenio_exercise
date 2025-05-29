import os
import random
import string
import asyncio
import http.client
import logging
import argparse
import json
import time

# Set the path for logs folder to the current working directory (ensure it creates in the server folder)
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_directory, exist_ok=True)  # Create logs folder in the server directory

# Basic logging configuration
logging.basicConfig(
    filename='logs/client.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Environment-based configuration
SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))


def generate_random_string():
    """
    Generates a random string of 50-100 characters, containing
    3 to 5 non-consecutive spaces not at the beginning or end.
    """
    length = random.randint(50, 100)
    num_spaces = random.randint(3, 5)
    allowed_chars = string.ascii_letters + string.digits
    chars = [random.choice(allowed_chars) for _ in range(length)]

    possible_indices = list(range(1, length - 1))
    space_indices = set()
    while len(space_indices) < num_spaces:
        idx = random.choice(possible_indices)
        if (idx - 1 in space_indices) or (idx + 1 in space_indices):
            continue
        space_indices.add(idx)

    for idx in space_indices:
        chars[idx] = ' '

    return ''.join(chars)


def send_string_http(text):
    """
    Sends a single string to the server via HTTP POST using http.client.
    Returns the weight or None.
    """
    try:
        conn = http.client.HTTPConnection(SERVER_HOST, SERVER_PORT, timeout=10)
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({'text': text})
        conn.request('POST', '/calculate/', body, headers)
        response = conn.getresponse()
        response_body = response.read().decode()
        conn.close()

        if response.status == 200:
            data = json.loads(response_body)
            weight = data.get('weight')
            logging.info(f"Received weight: {weight} for input: {text[:30]}...")
            return weight
        else:
            logging.error(f"HTTP error {response.status} on string: {text[:30]}...")
            return None
    except Exception as e:
        logging.error(f"Exception sending string: {e}")
        return None


async def send_string_async(text, loop):
    """
    Runs the blocking send_string_http in an executor to keep async.
    """
    return await loop.run_in_executor(None, send_string_http, text)


async def send_strings_from_file(input_path, output_path):
    """
    Reads strings from input file, sends them asynchronously to server,
    writes the results to output file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    loop = asyncio.get_running_loop()
    tasks = []

    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line:
                tasks.append(send_string_async(line, loop))

        results = await asyncio.gather(*tasks)
        for weight in results:
            if weight is not None:
                outfile.write(f"{weight}\n")


def generate_file(num_strings=1000000, file_path="data/chains.txt"):
    """
    Generates a file with the specified number of valid chains.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        for _ in range(num_strings):
            file.write(generate_random_string() + '\n')


async def main_from_web(num_strings, output_file, response_file):
    start_time = time.time()

    logging.info(f"Generating {num_strings} chains...")
    generate_file(num_strings, output_file)

    logging.info(f"Sending chains to server and writing responses to {response_file}...")
    await send_strings_from_file(output_file, response_file)

    elapsed = time.time() - start_time
    logging.info(f"Process completed in {elapsed:.2f} seconds.")


def main():
    parser = argparse.ArgumentParser(description="Client that generates and sends chains to a server.")
    parser.add_argument('--num_strings', type=int, default=None,
                        help="Number of chains to generate (default: 1,000,000)")
    args = parser.parse_args()

    if args.num_strings is None:
        try:
            num_strings = int(input("Enter number of chains to generate (default 1000000): ") or 1000000)
        except ValueError:
            print("Invalid input, using default 1000000")
            num_strings = 1000000
    else:
        num_strings = args.num_strings

    output_file = "data/chains.txt"
    response_file = "data/responses.txt"

    asyncio.run(main_from_web(num_strings, output_file, response_file))


if __name__ == "__main__":
    main()
