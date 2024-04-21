# Course certificates creator 

**This is a desktop app that constructs pdf certificates for course participants, 
based on specific data extracted from a csv file.**

*This is a mockup app based on a real app.
The purpose of the app is to allow non-technical people to generate pdf 
certification automatically for course participants, directly from a csv file.*

*All participant names, course names, instructor names, instructor signatures, 
company logo and company name are fictitious. Some app functionality was also 
altered.*


## I. App purpose:
* The current app was constructed (and compiled into an executable file) to automate 
manual certification creation, speeding up the process considerably. 
* It presupposes no technical knowledge from the
user, apart from basic computer utilisation skills. 

## II. Using the app (as a user)
Normal usage:
* Read the instruction in the text area
* Click the "Browse csv file" button, navigate to your CSV file and press "Open"
* Wait for the app to finish creating the certifications
* Read report of prepared PDFs
* Created pdfs can be found in the "Created_certificates" folder

Errors and help:
* An error will pop up if the uploaded CSV has unexpected headers or if they are
in the wrong order.
* An error will pop up if not all signatures of the instructors are in the folder
* An error will pop up if the background image or logo image are missing from the folder
* A help button pops up an info message informing about how to use the app,
including how to change the images and add signatures

Changing the images and adding signatures:
* The user can change the image of the logo (used in the construction of the certificate pdf file)
by replacing the existing logo.png file in the "Assets/Images_for_certificates" folder with another file 
named logo.png. The recommended size is 138px(width) x 127px(height). 
* The user can change the image of the background (used as the pdf certificate background)
by replacing the existing bg.jpg file in the "Assets/Images_for_certificates" folder with another file 
named bg.jpg. The recommended size is 585px(width) x 833px(height). 
* The user can add or delete images with instructors signatures to/from "Assets/Instructor_signatures"
folder. The added file needs to be a png, and the name of the file has to match exactly the name of the 
instructor as presented in the csv. The recommended height of the image 70px. 


## III. Using the app (the code)
* Install the dependencies from dependencies.txt
* Run main.py
* There is a sample csv (Participants.csv) located in the folder "Course participants.csv"

## IV. Author
[BogdanMikimic](https://github.com/BogdanMikimic)

