import tarfile
files = tarfile.open('train_xml.tar.gz')
files = files.extractall()

def process_xml(filename):
  from xml.etree import ElementTree as ET
  tree = ET.parse(f'train_xml/{filename}')
  root = tree.getroot()
  # find all sections and mentions
  sections = []
  sections2 = []
  mentions = []
  for child in root.iter():
    if child.tag == "Section":
      sections.append(child.text)
      sections2.append(child.attrib)
    elif child.tag == "Mention":
      mentions.append(child.attrib)
  train_data = []
  counter = 0
  for x in sections:
    id = sections2[counter]["id"]
    counter += 1
    lst = []
    lst.append(x)
    dictionary = {}
    value = []
    mentions2 = []
    for x1 in mentions:
      if x1["section"] == id:
        mentions2.append(x1)
    for x2 in mentions2:
      if "," not in x2["start"]:
        start = int(x2["start"])
        end = start + int(x2["len"])
        tup = (start, end, x2["type"])
        # check if the start and end is equal to the str value
        if x[start:end] == x2["str"]:
          value.append(tup)
    dictionary["entities"] = value
    lst.append(dictionary)
    train_data.append(lst)
  return train_data

import os
path = 'train_xml'
train_data = []
for f in os.listdir(path):
  res = process_xml(f)
  train_data = train_data + res
