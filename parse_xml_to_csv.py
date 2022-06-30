import csv
from xml.etree import ElementTree


# CREATE EMPTY CSV FILE
file_location = 'cited_products.csv'
csvfile = open(file_location, 'w', newline='', encoding='utf-8')
csvfile_writer = csv.writer(csvfile, delimiter='|')

# MANUALLY ADD THE HEADER TO CSV FILE
xml_header_tags = ['entry_number', 'Main_Product_Name', 'Chemical_Name']

csvfile_writer.writerow(xml_header_tags)

# PARSE XML
xml_file = 'cited_products.xml'
xml = ElementTree.parse(xml_file)
root = xml.getroot()

for child in root:
    # print("TAG: "+str(child.tag)+" ATTRIBUTE: " +str(child.attrib) +' TEXT: '+ str(child.text))
    # CREATE ROW WITH PREDEFINED NULL FIELDS (to avoid index out of bounds error)
    row = ['null'] * 3

    # APPEND DATA TO ROW AT SPECIFIC INDEX
    row[0] = child.attrib['entry_number']

    # Nested tags
    chemical_name = ''
    main_product_name = ''

    for nested_child in child:
        if 'Chemical_Name' in nested_child.tag:
            chemical_name = chemical_name + nested_child.text + ', '
            header_index = xml_header_tags.index(nested_child.tag)
            row[header_index] = chemical_name

        elif 'Main_Product_Name' in nested_child.tag:
            main_product_name = main_product_name + nested_child.text + ', '
            header_index = xml_header_tags.index(nested_child.tag)
            row[header_index] = main_product_name

    # ADD A NEW ROW TO CSV FILE
    csvfile_writer.writerow(row)
csvfile.close()

# Print the xml tags
elemList = []
for elem in xml.iter():
    elemList.append(elem.tag)

# Removing duplicated by converting to set and back to list
elemList = list(set(elemList))

# Just printing out the result
print(f"XML TAGS: {elemList}")
# ['Cited_Product', 'Cited_Products', 'Chemical_Name', 'Main_Product_Name']
