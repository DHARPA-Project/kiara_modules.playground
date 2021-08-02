import re

# get publication ref from file name
def get_ref(file):
  ref_match = re.findall(r'(\w+\d+)_\d{4}-\d{2}-\d{2}_',file)
  return ref_match[0]

# get date from file name
def get_date(file):
  date_match = re.findall(r'_(\d{4}-\d{2}-\d{2})_',file)
  return date_match[0]

# get year from file name
def get_year(file):
  year_match = re.findall(r'_(\d{4})-\d{2}-\d{2}_',file)
  return year_match[0]

# get month from file name
def get_month(file):
  month_match = re.findall(r'_\d{4}-(\d{2})-\d{2}_',file)
  return month_match[0]

# get day from file name
def get_day(file):
  month_match = re.findall(r'_\d{4}-\d{2}-(\d{2})_',file)
  return month_match[0]

# add publication names
def get_pub_name(pub_number):
    if (pub_number == 'sn85066408'):
        return 'L\'Italia'
    elif (pub_number == '2012271201'):
        return 'Cronaca Sovversiva'
    elif (pub_number == 'sn84020351'):
        return 'La Sentinella'
    elif (pub_number == 'sn85054967'):
        return 'Il Patriota'
    elif (pub_number == 'sn84037024'):
        return 'La Ragione'
    elif (pub_number == 'sn84037025'):
        return 'La Rassegna'
    elif (pub_number == 'sn85055164'):
        return 'La Libera Parola'
    elif (pub_number == 'sn86092310'):
        return 'La Sentinella del West'
    elif (pub_number == 'sn92051386'):
        return 'La Tribuna del Connecticut'
    elif (pub_number == 'sn93053873'):
        return 'L\'Indipendente'
         
