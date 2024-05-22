import random
import hashlib
from datetime import datetime



def generar_id_scan():
  """
  Genera un ID único basado en la fecha y hora actual.
  Formato del ID: YYYYMMDDHHmmssSSSSS
  Retorno:
    str: ID único generado.
  """
  # Obtiene la fecha y hora actual
  fecha_hora_actual = datetime.now()

  # Formateo de la fecha y hora
  anio = str(fecha_hora_actual.year).zfill(4)
  mes = str(fecha_hora_actual.month).zfill(2)
  dia = str(fecha_hora_actual.day).zfill(2)
  hora = str(fecha_hora_actual.hour).zfill(2)
  minuto = str(fecha_hora_actual.minute).zfill(2)
  segundo = str(fecha_hora_actual.second).zfill(2)
  milisegundo = str(fecha_hora_actual.microsecond)[:5]
  num_random = random.randint(10**18, 10**19 - 1) #19 digitos enteros
  # Concatenación para formar el ID único
  id_scan_inter = f"{anio}{mes}{dia}{hora}{minuto}{segundo}{milisegundo}"
  id_scan = hashlib.sha256(
        ( str(id_scan_inter) + str(num_random)).encode()
    ).hexdigest()
  

  return id_scan  


if __name__ == "__main__":
    
 generar_id_scan()

