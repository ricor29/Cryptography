# Simple code to startup a server.

import server


# Create a UDP symmetric encryption MAC server.
symServer = server.Server(host='',
                          port=13000,
                          buff=1024)

symServer.run()
