import os

from dotenv import load_dotenv

load_dotenv()

_from = os.getenv('FROM')
to = os.getenv('TO')
adults = os.getenv('ADULTS')
kids = os.getenv('KIDS')
babies = os.getenv('BABIES')
going_date = os.getenv('GOING_DATE')
return_date = os.getenv('RETURN_DATE')
_class = os.getenv('CLASS')

url = 'https://123milhas.com/v2/busca?de='+_from+'&para='+to+'&adultos='+adults+'&criancas='+kids+'&bebes='+babies+'&ida='+going_date+'&volta='+return_date+ \
      '&classe='+_class
