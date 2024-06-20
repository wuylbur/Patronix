#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

#This module implements pseudo-random number generators for various distributions.
import random

#This module implements a common interface to many different secure hash and message digest algorithms.
import hashlib

from datetime import datetime



def generate_id_scan():
  """
  Generates a unique ID based on the current date and time. ID format: YYYYMMDDHHmmssSSSSS
  """
  # Gets the current date and time
  current_date_time = datetime.now()

  # Date and time formatting
  year = str(current_date_time.year).zfill(4)
  month = str(current_date_time.month).zfill(2)
  day = str(current_date_time.day).zfill(2)
  hour = str(current_date_time.hour).zfill(2)
  minute = str(current_date_time.minute).zfill(2)
  second = str(current_date_time.second).zfill(2)
  microsecond = str(current_date_time.microsecond)[:5]
  num_random = random.randint(10**18, 10**19 - 1) #19 integers
  
  
  # Concatenation to form the unique ID
  id_scan_inter = f"{year}{month}{day}{hour}{minute}{second}{microsecond}"
  
  id_scan = hashlib.sha256(
        ( str(id_scan_inter) + str(num_random)).encode()
    ).hexdigest()
  

  return id_scan  


if __name__ == "__main__":
    
 generate_id_scan()

