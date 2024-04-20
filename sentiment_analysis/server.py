#Script to connect the bot server to the web interface
import asyncio
import json
import threading
import time
import websockets
import socket
import openai
import myAnimeListAPI as mala
from logistic_inference import compute_positivity
from infer import init_search
from emotions import load_emotions

clients = {}
client_id = 0

# Secret key for OpenAI API
openai.api_key = "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"


def getRatings(animeid):
    url = "https://api.myanimelist.net/v2/anime/{animeid}?fields=rating"
    return mala.makeRequest(url)["rating"]

#Assynchronous function that receives a JSON Message and acts uppon its contents
#Different types:
#   -query: User query. Contains the name of an Anime or Series the bot should generate data for. The response will be a JSON containing that data 
async def process_message(message):
        #print(message)
        msg = json.loads(message)

        match msg["type"]:
            case "query":
 
                data = init_search(msg["text"])
                #rating = getRatings(msg["id"])
                response = {
                    "type": "message",
                    "text": data,
                    'positivity': 0,
                    'all': load_emotions("emotion.json", "one-piece")
                    #"rating": rating
                }
                
                #print(response)
                return response
            
            case _:
                print("Something is wrong")


async def refrase_query(query):
    prompt = "take this review and rephrase in a clearer way but keep the essence and structure: \n\n"
    #
    #Rephrase only the grammar of the following query. Just write the refrased query and if you don't understand don't say nothing:
    print("Refrasing query: " + query)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt + query}
        ]
    )
    improved_query = completion.choices[0].message.content

    #print("Improved query: " + improved_query)
    if improved_query != None and len(improved_query) > 0:
        return improved_query
    
    # if chat gpt is offline, just return the original query
    return query



# Handles communication between sockets
async def handler(websocket):
    global client_id
    global clients

    local_client_id = client_id

    # store user connection in an array 
    clients[client_id] = websocket
    
    client_id += 1

    # for each subsquent message received, process it
    async for message in websocket:
        response = await process_message(message)
        if (response != None and len(response) > 0): 
            response["text"] = await refrase_query(response["text"])
            response["positivity"] = compute_positivity(response["text"].split("."))
            await websocket.send(json.dumps(response))

#Assync function to send a message to all selected sockets
# ids -> array of ids (can be single)
# message -> msg to be sent
async def send_to_users(ids, message, all=False):
    global clients

    if (all == True):
        broadcast_connections = []
        for k,v in clients.items():
            broadcast_connections.append(v)

        websockets.broadcast(broadcast_connections, message)
        return

    users_connections = []
    for id in ids:
        users_connections.append(clients[id])
    
    websockets.broadcast(users_connections, message)


async def main():
    ip = socket.gethostbyname(socket.gethostname())
    print("Serving websocket server at " + ip + ":8080")
    socket_to_share = open("../interface-shift/src/socket_to_share.txt", "w")
    socket_to_share .write(ip+":8080")
    socket_to_share.close()
    # f = open("socket_to_share.txt", "r")
    # print(f.read())
    # f.close()
    async with websockets.serve(handler, ip, 8080):
        await asyncio.Future()  # run forever


asyncio.run(main())