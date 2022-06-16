import xml.etree.ElementTree as ET

# import data by reading from file 'sample.xml'
tree  = ET.parse('sample.xml')

# returns the root element of the XML file
root = tree.getroot()

print(root)
# print will return this statement:
# <Element 'data' at 0x00000165AC3393B0>


# As an Element, data has a tag and a dictionary of attributes
print(root.tag)  # prints: data


# It also has child nodes, which can be accessed by index since they are nested
# The .attrib method wll return a dict of attributes for the element
# Here the first element is <person id = "100" > and it only has one attribute: id
print(root[0].attrib) # prints {'id': '100'}

#since child nodes are nested, we can iterate over them to print their info
for child in root[1]:  #this will iterate over all child elements of the first element
    print(child.tag ,child.text)  #.text will return the value for a certain tag (for ex: tag is firstName, will return John)
# prints:
# firstName John
# lastName Doe
# age 25
# registered Yes

# We can also use 2d index to access specific tag of an element
# this looks at the first[0] 'person' element and the second[1] element tag 'lastName'
print(root[0][1].text) #prints: Doe

# To look for specific tags in the XML file, we can iterate using .find and .findall methods
# .find() returns the first matching element, or none
# .findall() returns a list with all matching elements
for x in root:
    age = x.find('age').text  # prints: 25   32
    names = x.findall('age')  # prints: [<Element 'age' at 0x000001AD4BAA45E0>]
    print(age,names)

