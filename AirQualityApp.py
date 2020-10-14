"""
Author: Bianca Magyar
Date: 10/13/2020
Description: Air quality app programmed in Python, 
             utilizing Air Now API to provide city,
             quality, and category data based on 
             major US city zipcodes.
References: Codemy
"""

from tkinter import *
from PIL import ImageTk, Image
import requests
import json


#create zipcode lookup function
def ziplookup():

    try:
        #read in url for data
        api_request = requests.get("http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" 
                                   + zip.get() + "&distance=5&API_KEY=61AD62A7-9BAB-4610-9346-E677510F28D1")
        
        #used .text instead of .content bc .content made program jump to exception
        #store data from api_request into json to load and store in api variable
        #api variable contains a list with dictionaries in each index
        api = json.loads(api_request.text)
        
        #store parts of data in variables
        city = api[0]["ReportingArea"]
        quality = api[0]["AQI"]
        category = api[0]["Category"]["Name"]

        #determine air color based on category
        quality_color = ""
        if category =="Good":
            quality_color = "green"
        elif category == "Moderate":
            quality_color = "yellow"
        elif category == "Unhealthy for Sensitive Groups":
            quality_color = "orange"  
        elif category == "Unhealthy":
            quality_color = "red"
        elif category == "Very Unhealthy":
            quality_color = "purple"
        elif category == "Hazardous":
            quality_color = "maroon"  
        
        
        #set background color
        root.configure(background=quality_color)
          
        #display data in window by updating result label
        result_label.config(text=city + "\nAir Quality " + str(quality) + "\n" + category, font=("Helvetica", 15), bg=quality_color)
        zip.delete(0, END)
        
    except Exception as e:
        api = "Oops, try a different zipcode."
        default = "#ffffff" #set neutral color for error 
        root.configure(background=default)
        result_label.config(text=api, font=("Helvetica", 14), bg=default)

if __name__ == "__main__":   
    #set up window
    root = Tk()
    root.title("Air Quality App")
    root.iconbitmap("lungs.ico") 
    root.geometry("275x150")
    
    #create zipcode entry field
    zip = Entry(root)
    zip.grid(row=0, column=0, padx=2, ipadx=10, stick=W+E+N+S)
    
    #create zipcode button  
    zip_button = Button(root, text="Lookup Zipcode", command=ziplookup)
    zip_button.grid(row=0, column=1, ipadx=15, stick=W+E+N+S)
    
    #create label to display result
    result_label = Label(root)
    result_label.grid(row=1, column=0, columnspan=2, pady=20)
    
    root.mainloop()

