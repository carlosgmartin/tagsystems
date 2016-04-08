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

# Returns the production distribution from the word distribution
def get_prod_probs(word_probs, get_prod):
  prod_probs = {}
  for word in word_probs:
    prod = get_prod(word)
    if prod not in prod_probs: prod_probs[prod] = 0
    prod_probs[prod] += word_probs[word]
  return prod_probs

# Normalizes a distribution into a probability distribution
def normalize(probs):
  total = sum(probs.values())
  for event in probs:
    probs[event] /= total
  return probs

# Returns the word distribution from the production distribution
def get_word_probs(prod_probs):
  word_probs = {}
  for prod in prod_probs:
    if len(prod) == 0: continue
    for pos in range(len(prod) - 1):
      word = prod[pos:pos + 2]
      if word not in word_probs: word_probs[word] = 0
      word_probs[word] += prod_probs[prod]
    # Consider every production that could follow the current one
    for prod2 in prod_probs:
      if len(prod2) == 0: continue
      word = (prod[-1], prod2[0])
      if word not in word_probs: word_probs[word] = 0
      word_probs[word] += prod_probs[prod] * prod_probs[prod2]
  return normalize(word_probs)

# Returns the expected density of symbols on the queue
def get_densities(word_probs):
  densities = {}
  for word in word_probs:
    for symbol in word:
      if symbol not in densities: densities[symbol] = 0
      densities[symbol] += word_probs[word]
  return normalize(densities)
      
def get_growth(word_probs, get_prod):
  expected_length = 0
  for word in word_probs:
    expected_length += len(get_prod(word)) * word_probs[word]
  return expected_length - 2

initial_word_probs = {}
initial_word_probs[(0, 0)] = .25
initial_word_probs[(0, 1)] = .25
initial_word_probs[(1, 0)] = .25
initial_word_probs[(1, 1)] = .25

word_probs = {}
prod_probs = {}

word_probs[0] = initial_word_probs
epochs = 10

for epoch in range(epochs):
  prod_probs[epoch + 1] = get_prod_probs(word_probs[epoch], get_prod)
  word_probs[epoch + 1] = get_word_probs(prod_probs[epoch + 1])

length = 10000
for epoch in range(epochs):
  print('Epoch ' + str(epoch))
  densities = get_densities(word_probs[epoch])
  growth = get_growth(word_probs[epoch], get_prod)
  print('Length: ' + str(length))
  print('Density of a symbols: ' + str(densities[0]))
  print('Density of b symbols: ' + str(densities[1]))
  print('')
  length *= (1 + growth/2)