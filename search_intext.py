#this code is part of the Final Degree Project in UNIR by Gonzalo Castro

#This module provides regular expression matching operations similar to those found in Perl.
import re


def Search_GDPR(plan_text,regular_expressions):#search GDPR regular expressions in plain text
  results = []
   
  for name,expression_regular in regular_expressions:
    coincidences = re.findall(expression_regular, plan_text)#returns matches found in plain text
    
    if coincidences:#if not empty
      results.append((name, coincidences))
      
  return results


def Search_Pattern(text,pattern):#search pattern in plain text. If we find a match it is already positive
  expression_regular = re.compile(pattern)
  results = expression_regular.search(text)
  if results:
    return True
  
  return False

      
if __name__ == "__main__":
 Search_Pattern()
 Search_GDPR()
 