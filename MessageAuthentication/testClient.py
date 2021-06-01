# Simple code to startup a client.

import client


# Create a UDP symmetric encryption MAC server.
symClient = client.Client(host='127.0.0.1',
                          port=13000)

symClient.run()
