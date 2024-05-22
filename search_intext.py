import re

#search regular expressions in plain text
def Search_GDPR(texto_plano,expresiones_regulares):
  resultados = []
  print (f"EXPREG son:,{expresiones_regulares}")
 
  for nombre,expresion_regular in expresiones_regulares:
    coincidencias = re.findall(expresion_regular, texto_plano)
    print ("Encontrados: ",coincidencias)
    if coincidencias:
      resultados.append((nombre, coincidencias)) #FALTA METER EL ID DE FICHERO
      
  print ("Resultados", resultados)
  return resultados

#search pattern in plain text
def Search_Pattern(texto,patron):
  expresion_regular = re.compile(patron)
  resultado = expresion_regular.search(texto)
  if resultado:
    return True
  
  return False

      
if __name__ == "__main__":
 Search_Pattern()
 Search_GDPR()
 