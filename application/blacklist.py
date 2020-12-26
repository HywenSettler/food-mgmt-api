'''
A storage engine to save revoked tokens. In production if
speed is the primary concern, redis is a good bet. If data
persistence is more important for you, postgres is another
great option. In this example, we will be using an in memory
store, just to show you how this might work.

For this example, we are just checking if the tokens jti
(unique identifier) is in the blacklist set.
'''

BLACKLIST = set()
