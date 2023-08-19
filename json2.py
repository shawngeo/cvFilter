import PyPDF2
import json

# Open the PDF file in read binary mode
with open('actual/cv1.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Get the total number of pages in the PDF file
    num_pages = pdf_reader.getNumPages()

    # Create an empty list to store the data from each page
    data = []

    # Loop through each page in the PDF file
    for page_num in range(num_pages):
        # Get the current page object
        page = pdf_reader.getPage(page_num)

        # Extract the text from the page
        text = page.extractText()

        # Convert the text to a dictionary
        page_data = {'page_num': page_num, 'text': text}

        # Append the dictionary to the data list
        data.append(page_data)

# Convert the data list to a JSON object and write it to a file
with open('example.json', 'w') as json_file:
    json.dump(data, json_file)