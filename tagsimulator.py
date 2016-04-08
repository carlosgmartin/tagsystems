import random

# Returns the production to be appended to the queue
def get_prod(word):
  if word == (0, 0):
    return (1, 1, 1)
  if word == (0, 1):
    return (0, 1)
  if word == (1, 0):
    return (1, 1)
  if word == (1, 1):
    return (0,)

# Creates a queue with a random configuration of specified length
def create_queue(length):
  return tuple(random.choice([0, 1]) for n in range(length))

# Updates the queue by deleting two symbols from the front and
# appending a corresponding production to the back
def update(queue):
  return queue[2:] + get_prod(queue[:2])

# Update the queue until all original symbols have been deleted
def update_epoch(queue):
  for n in range(int(len(queue)/2)):
    queue = update(queue)
  return queue

epochs = 10
queue = create_queue(10000)

for epoch in range(epochs):
  print('Epoch ' + str(epoch))
  print('Length: ' + str(len(queue)))
  print('Density of a symbols: ' + str(queue.count(0)/len(queue)))
  print('Density of b symbols: ' + str(queue.count(1)/len(queue)))
  print('')
  queue = update_epoch(queue)