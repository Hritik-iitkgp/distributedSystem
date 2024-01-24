from flask import Flask, jsonify,request
import os,subprocess,random,requests,time
from consistent_hashing import ConsistentHashMap 

N=0

my_unq_cnt=1

req_id=0

consistent_hash_map = ConsistentHashMap(M=512, N=0, K=9)

replicas=[]
app = Flask(__name__)
@app.route('/rep', methods=['GET'])
def get_replicas():
    global N
    response = {
        "message": {
            "N": N,
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200


@app.route('/add', methods=['POST'])
def add_replicas():
    global my_unq_cnt
    global N
    global consistent_hash_map
    data = request.get_json()
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    print(n)
    print(hostnames)

    if len(hostnames) > n:
        response = {
            "message": "<Error> Length of hostname list is more than newly added instances",
            "status": "failure"
        }
        return jsonify(response), 400

    # # Update consistent hash map and replicas list
    for i in range(n): 
        if i < len(hostnames):
            replica_name = hostnames[i]
        else:
            replica_name = f"My_unique_name{my_unq_cnt}"
            my_unq_cnt+=1
        #consistent_hash.add_server(replica_name)
        command =  f"docker run --name {replica_name} --env SERVER_ID={replica_name} --network net1 -d firstbuild"
        result = subprocess.run(command,shell=True,text=True)
        consistent_hash_map.add_server_instance(replica_name)
        N+=1
        replicas.append(replica_name)
    

    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200


@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    global consistent_hash_map
    global N
    data = request.get_json()
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])

    if len(hostnames) > n:
        response = {
            "message": "<Error> Length of hostname list is more than removable instances",
            "status": "failure"
        }
        return jsonify(response), 400

    # Update replicas list
    for i in range(n):
        if i < len(hostnames):
            replica_name = hostnames[i]
            command=f"docker rm -f {replica_name}"
            subprocess.run(command,shell=True,text=True)
            consistent_hash_map.remove_server_instance(replica_name)
            N-=1
            replicas.remove(replica_name)
        else:
            # Randomly choose a replica to remove
            removed_replica = random.choice(replicas)
            command=f"docker rm -f {removed_replica}"
            subprocess.run(command,shell=True,text=True)
            consistent_hash_map.remove_server_instance(removed_replica)
            N-=1
            replicas.remove(removed_replica)

    #update_hash_slots()

    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/<path>', methods=['GET'])
def route_request(path):
    global req_id
    global my_unq_cnt
    global consistent_hash_map
    if path.startswith("/"):
        path = path[1:]  # Remove leading slash

    # Check if the path is specifically registered
    if path == 'home' or path == 'heartbeat':
        req_id+=1
        alloted_server=consistent_hash_map.map_request_to_server(req_id)
        #print(alloted_server)

        try:
            response=requests.get(f"http://{alloted_server}:5000/{path}")
            print(response.status_code)
            if response.status_code== 200:
                json_response = response.json()
                return jsonify(json_response),200
                
            else:
                return f"{path}Error{alloted_server}",404
                
        except:
            consistent_hash_map.remove_server_instance(alloted_server)
            replicas.remove(alloted_server)
            replica_name=f"My_unique_name{my_unq_cnt}"
            my_unq_cnt+=1
            command =  f"docker run --name {replica_name} --env SERVER_ID={replica_name} --network net1 -d firstbuild"
            result = subprocess.run(command,shell=True,text=True)
            time.sleep(2)
            consistent_hash_map.add_server_instance(replica_name)
            replicas.append(replica_name)

            response=requests.get(f"http://{replica_name}:5000/{path}")
            json_response = response.json()
            return jsonify(json_response),200
            

        
            







        
        
    else:
        # Treat as a custom path and forward to the appropriate server replica
        response = jsonify({"message": "Request for unknown custom path", "status": "failure"})
        return response, 404  


if __name__ == '__main__':
    # N=0
    # my_unq_cnt=0
    


    app.run(host='0.0.0.0', port=5000,debug=True)