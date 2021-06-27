def s(endpoint):
  try: 
      x = endpoint
  except KeyError:
      x = 'undefined'
  return x