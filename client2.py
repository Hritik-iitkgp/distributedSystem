import requests,time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def add_servers(N):
    # Add 3 servers initially
    payload = {
        "n": N,
        "hostnames": []
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

def calculate_average_load(responses, server_replicas):
    server_counts = {}
    for response in responses:
        server_id = response.split(": ")[1]
        server_counts[server_id] = server_counts.get(server_id, 0) + 1

    average_loads = [server_counts.get(server_id, 0) / len(responses) * 100 for server_id in server_replicas]
    return average_loads

def plot_line_chart(server_counts, average_loads_list):
    for i, average_loads in enumerate(average_loads_list):
        plt.plot(server_counts[i], average_loads, marker='o', label=f'N={server_counts[i]}')

    plt.xlabel('Number of Servers (N)')
    plt.ylabel('Average Load (%)')
    plt.title('Average Load of Servers for Different Number of Servers')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    avg_list=[]
    # Add servers initially and get the server replicas
    
    server_replicas = add_servers(2)

    time.sleep(1)

    # Make 10000 requests with path as /home
    responses = make_requests(len(server_replicas))

    # Plot the bar graph
    #plot_bar_graph(responses)
    avg_loads=calculate_average_load(responses,server_replicas)
    plot_line_chart(server_replicas,avg_loads)
    avg_list.append(avg_loads)

    server_replicas = add_servers(1)

    time.sleep(1)

    # Make 10000 requests with path as /home
    responses = make_requests(len(server_replicas))

    # Plot the bar graph
    avg_loads=calculate_average_load(responses,server_replicas)
    plot_line_chart(server_replicas,avg_loads)
    avg_list.append(avg_loads)

    server_replicas = add_servers(1)

    time.sleep(1)

    # Make 10000 requests with path as /home
    responses = make_requests(len(server_replicas))

    # Plot the bar graph
    avg_loads=calculate_average_load(responses,server_replicas)
    plot_line_chart(server_replicas,avg_loads)
    avg_list.append(avg_loads)
    server_replicas = add_servers(1)

    time.sleep(1)

    # Make 10000 requests with path as /home
    responses = make_requests(len(server_replicas))

    # Plot the bar graph
    avg_loads=calculate_average_load(responses,server_replicas)
    plot_line_chart(server_replicas,avg_loads)
    avg_list.append(avg_loads)
    server_replicas = add_servers(1)

    time.sleep(1)

    # Make 10000 requests with path as /home
    responses = make_requests(len(server_replicas))

    # Plot the bar graph
    avg_loads=calculate_average_load(responses,server_replicas)
    plot_line_chart(server_replicas,avg_loads)
    avg_list.append(avg_loads)

   
    
