import requests,time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def add_servers():
    # Add 3 servers initially
    payload = {
        "n": 3,
        "hostnames": ["S1", "S2", "S3"]
    }
    response = requests.post("http://localhost:5000/add", json=payload)
    return response.json()["message"]["replicas"]

def make_requests(server_count):
    # Make 10000 requests with path as /home
    responses = []

    with ThreadPoolExecutor(max_workers=server_count) as executor:
        futures = []

        for _ in range(10000):
            future = executor.submit(make_request, "/home")
            futures.append(future)

        for future in futures:
            responses.append(future.result())

    return responses

def make_request(path):
    response = requests.get(f"http://localhost:5000{path}")
    return response.json()["message"]

def plot_bar_graph(server_responses):
    # Plot a bar graph on the number of requests handled by each server
    server_counts = {}
    for response in server_responses:
        server_id = response.split(": ")[1]
        server_counts[server_id] = server_counts.get(server_id, 0) + 1

    servers = list(server_counts.keys())
    request_counts = list(server_counts.values())

    plt.bar(servers, request_counts)
    plt.xlabel('Server ID')
    plt.ylabel('Number of Requests')
    plt.title('Number of Requests Handled by Each Server')
    plt.show()

if __name__ == "__main__":
    # Add servers initially and get the server replicas
    server_replicas = add_servers()

    time.sleep(5)

    # Make 10000 requests with path as /home
    responses = make_requests(len(server_replicas))

    # Plot the bar graph
    plot_bar_graph(responses)
