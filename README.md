# Toucher-Redis
- Explorer Redis avec les methodes FIFO et LIFO 

- Explore Redis with FIFO and LIFO methods

- Изучите Redis с помощью методов FIFO и LIFO

### Pour Afficher les Taches enregistrees dans db 1 (check in db 1)
1) redis-cli
2) SELECT 1
3) KEYS *

### Commandes utilisees (Commands used):
 1) LLEN key:
- Returns the length of the list stored at key. If key does not exist, it is interpreted as an empty list and 0 is returned. 
An error is returned when the value stored at key is not a list.

 2) RPOP key :
- Removes and returns the first elements of the list stored at key.

 3) SET key :
- Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type. 
- Any previous time to live associated with the key is discarded on successful SET operation.

 4) RPUSH key :
- Insert all the specified values at the tail of the list stored at key. 
- If key does not exist, it is created as empty list before performing the push operation. 
- When key holds a value that is not a list, an error is returned.

 5) LPOP key :
- Removes and returns the first elements of the list stored at key.