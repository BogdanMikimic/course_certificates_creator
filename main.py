from customtkinter import CTk, \
    CTkLabel, \
    set_appearance_mode, \
    set_default_color_theme, \
    CTkTextbox, \
    CTkButton
from tkinter import filedialog, messagebox, END
from csv import reader
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import os
from threading import Thread

# ================ App colors, folder paths and, images names and sizes ================
light_text_color = '#d1906b'
lighter_bg_color = '#205c1f'
darker_bg_color = '#163b16'

help_text_color = '#b682fa'
close_text_color = '#ff083e'

disabled_color = '#595959'

created_certificates_folder_path = 'Created_certificates'
instructor_signatures_folder_path = 'Assets/Instructor_signatures'
image_assets_folder_path = 'Assets/Images_for_certificates'

background_image_name = 'bg.jpg'
background_image_with_path = f'{image_assets_folder_path}/{background_image_name}'
recommended_background_width = '585px(width)'
recommended_background_height = '833px(height)'

logo_image_name = 'logo.png'
logo_image_with_path = f'{image_assets_folder_path}/{logo_image_name}'
recommended_logo_width = '138px(width)'
recommended_logo_height = '127px(height)'

# ================ App functions ================

def clear_textbox() -> None:
    """
    Clears the text in the textbox widget
    :return: None
    """

    reporting_text_area.delete('1.0', 'end')


def write_in_textbox(text: str) -> None:
    """
    Writes (appends) text in textbox widget
    :param text: Test to be written
    :return: None
    """

    reporting_text_area.insert(END, text)


def csv_expected_content_and_order() -> list:
    """
    Serves the expected CSV headers in expected order.
    :return: list of csv headers in order
    """

    csv_headers_in_order = ['Last name',
                            'First name',
                            'Course name',
                            'Instructor name',
                            'Date of course',
                            'Course completed']
    return csv_headers_in_order


def check_csv_structure_and_file_existence(my_csv: str) -> bool:
    """
    Checks if the CSV has the right headers in the right order. Shows error message if not
    Checks if all the instructors have their signatures as png files. Shows error message if not
    Checks if the background image and logo image used to construct the certifications are there.
    Shows error message if not
    :param my_csv: the path of the CSV file
    :return: True if the headers are the right ones in the right order AND
    if all the signatures of instructors are present as png files, False otherwise
    """

    with open(my_csv, newline='') as csv_file:
        csv_reader = reader(csv_file)
        actual_headers = next(csv_reader)
        expected_headers = csv_expected_content_and_order()
        # check csv headers and order
        if actual_headers != expected_headers:
            error_message = 'The CSV file does not contain the required fields or they are not in the required order! '
            error_message += 'Check the headers in your csv to match the expected headers:'
            error_message += f'\n\n{", ".join(expected_headers)}.'
            error_message += '\n\nMake sure to check the order of the headers as well as the case of the headers and '
            error_message += 'if they match, try again.'
            messagebox.showerror('Not the right content', error_message)
            return False

        # get names of all instructors cited in the csv
        instructors_list = list()
        for line in csv_reader:
            instructors_list.append(line[3])
        # retrieve list of image files with instructor signatures
        list_of_signature_files = os.listdir(f'{instructor_signatures_folder_path}')
        # remove file extension
        signature_files_names_only_list = list()
        for inst_name in list_of_signature_files:
            signature_files_names_only_list.append(inst_name.split('.')[0])

        # check if all instructors delivering courses have a signature files, interrupt pdf creation if not
        for instructor_name in instructors_list:
            if instructor_name not in signature_files_names_only_list:
                message = f'The png file with the signature of the instructor: {instructor_name} '
                message += f'is not in the {instructor_signatures_folder_path} folder\n\n'
                message += 'The name of the png file containing the signature has to match exactly '
                message += 'the name of the instructor from the csv file, including the case'
                messagebox.showerror('Instructor signature not found', message)
                return False

        # check that the required bg.jpg exist in the "Images_for_certificates".
        # Raise error messages and interrupt pdf creation if not
        if os.path.exists(background_image_with_path) is False:
            msg_missing_bg_img = f'The required "{background_image_name}" file (which is the background image of the'
            msg_missing_bg_img += f' certification) is missing from the "{image_assets_folder_path}" folder.\n\n'
            msg_missing_bg_img += f'Make sure you have a "{background_image_name}" file in the '
            msg_missing_bg_img += f'"{image_assets_folder_path}" folder, otherwise the program will NOT work\n\n'
            msg_missing_bg_img += f'The recommended size of the image is {recommended_background_width} x '
            msg_missing_bg_img += f'{recommended_background_height}. '
            msg_missing_bg_img += f'The image must be called `{background_image_name.split(".")[0]}` and must be a '
            msg_missing_bg_img += f'`{background_image_name.split(".")[1]}` file format.'
            messagebox.showerror('File not found', msg_missing_bg_img)
            return False

        # check that the required logo.png exist in the "Images_for_certificates".
        # Raise error messages and interrupt pdf creation if not
        if os.path.exists(f'{logo_image_with_path}') is False:
            msg_missing_bg_img = f'The required "{logo_image_name}" file (which is the company logo image at the top of '
            msg_missing_bg_img += f'the certification) is missing from the "{image_assets_folder_path}" folder.\n\n'
            msg_missing_bg_img += f'Make sure you have a "{logo_image_name}" file in the "{image_assets_folder_path}" folder, '
            msg_missing_bg_img += 'otherwise the program will NOT work\n\n'
            msg_missing_bg_img += f'The recommended size of the image is {recommended_logo_width} x {recommended_logo_height}. '
            msg_missing_bg_img += f'The image file must be called `{logo_image_name.split(".")[0]}` and must be a `{logo_image_name.split(".")[1]}` file format.'
            messagebox.showerror('File not found', msg_missing_bg_img)
            return False

        # if all checks are ok, return True
        return True


def create_pdf(participant_name: str, course_name: str, date_of_course: str, instructor_name: str) -> None:
    """
    Creates a certificate pdf file for each course participant and saves it in the Created_certificates folder
    :param participant_name:
    :param course_name:
    :param date_of_course:
    :param instructor_name:
    :return: None
    """

    pdf_name_and_path = f'{created_certificates_folder_path}/{participant_name} - {course_name}.pdf'
    pdf = Canvas(pdf_name_and_path, pagesize=A4)
    pdf.setTitle('Certificate of completion')
    # images
    pdf.drawInlineImage(f'{background_image_with_path}', 0, 0)  # background pic
    pdf.drawInlineImage(f'{logo_image_with_path}', 230, 610)  # logo

    pdf.setFont('Courier-Bold', 27)
    pdf.drawCentredString(297.5, 500, 'Certificate of Completion')

    pdf.setFont('Courier', 12)
    pdf.drawCentredString(297.5, 480, 'Cocoa Bluss Ltd. hereby certifies that:')

    pdf.setFont('Courier-Bold', 24)
    pdf.drawCentredString(297.5, 410, participant_name)

    pdf.setFont('Courier', 12)
    pdf.drawCentredString(297.5, 320, 'Successfully completed the course:')

    pdf.setFont('Courier-Bold', 20)
    pdf.drawCentredString(297.5, 300, f'"{course_name}"')

    # the following text and image are aligned right
    point_of_x_alignment_to_right = 520
    pdf.setFont('Courier-Bold', 14)
    pdf.drawRightString(point_of_x_alignment_to_right, 180, f'Date of completion: {date_of_course}')
    pdf.drawRightString(point_of_x_alignment_to_right, 160, f'Instructor: Chef {instructor_name}')

    # check chef signature image size so it always align to the right no matter the width of the image
    with Image.open(f'{instructor_signatures_folder_path}/{instructor_name}.png') as img:
        image_width = img.size[0]
        pdf.drawInlineImage(img, (point_of_x_alignment_to_right - image_width), 70)

    # save pdf
    pdf.save()


def certifications_creation_handler(csv_with_path):
    """
    It iterates over the csv and calls the create_pdf() function for each participant that completed the course.
    It makes a list of the people that registered, but did not complete the course.
    It reports on the text box about the created pdfs and the pdfs that were not created
    (for people that did not complete the course)
    It is called in a separate thread
    It enables the "csv_select_and_pdf_creator_button" button widget
    :param csv_with_path: the path of the CSV file
    :return: None
    """

    with open(csv_with_path, newline='') as csv_file:
        csv_reader = reader(csv_file)
        # skip header
        next(csv_reader)
        # clear textbox text and intro text
        clear_textbox()
        write_in_textbox(f'Created PDF certificates:\n(you can find the created certificates\nin the "{created_certificates_folder_path}" folder)\n\n')
        # creating counters and not done list
        done_counter = 0
        not_done_counter = 0
        not_finished_course = list()
        for line in csv_reader:
            # check if person actually completed the course
            if line[5] == 'Yes':
                done_counter += 1
                participant_name = f'{line[0]} {line[1]}'
                course_name = line[2]
                instructor_name = line[3]
                date_of_course = line [4]
                # create the certification
                create_pdf(participant_name, course_name, date_of_course, instructor_name)
                # report about the created certification (name + the first 12 characters of the name of the course)
                write_in_textbox(f'{done_counter}. {participant_name} ({course_name[:12]+"..." if len(course_name)>=12 else course_name})\n')
            # if the person didn't complete the course, he is added to the list
            else:
                not_finished_course.append(f'{line[0]} {line[1]} ({line[2][:12]+"..." if len(line[2])>=12 else line[2]}) ')

        write_in_textbox(f'{"="*39}\nCertificates NOT created for:\n(due to not completing the course)\n\n')
        # report on people that registered for the course but did not complete it
        for student_and_course in not_finished_course:
            not_done_counter += 1
            write_in_textbox(f'{not_done_counter}. {student_and_course} \n')

        write_in_textbox(f'\nDone!\n\nThe certificates are in the\n"{created_certificates_folder_path}" folder ')

        # enable pdf creator button
        csv_select_and_pdf_creator_button.configure(text='Browse csv file',
                                                    state='normal',
                                                    fg_color=lighter_bg_color)


def make_certifications() -> None:
    """
    Opens filedialog to allow user to select the csv that contains the certification data
    Calls the functions that check the files and the csv
    Disables the browse button
    Calls the function that creates the pdfs in a new thread
    :return: None
    """

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        if check_csv_structure_and_file_existence(file_path):
            # disable browse button
            csv_select_and_pdf_creator_button.configure(text='Please wait',
                                                        state='disabled',
                                                        fg_color=disabled_color)

            # start a thread to create the pdfs without blocking the main application
            Thread(target=certifications_creation_handler, args=(file_path,)).start()


def help_message() -> None:
    """
    Pops up a message box that informs the user about how to use the UI
    """
    message = 'How to use the app:\n\n'
    message += '1. Press the "Browse files" button, navigate to your .csv file containing the course participants.\n\n'
    message += '2. Selecting the csv file will trigger an automatic check to find if it contains the expected headers '
    message += 'in the expected order, and if all the instructors have files with their signatures. '
    message += 'If any of the checks fail, you will be notified.\n\n'

    message += '3. If the tests pass, the pdf certifications will be automatically created and put in the '
    message += f'"{created_certificates_folder_path}" folder. The text box on the screen will notify you what certifications were'
    message += 'created and when it is done\n\n'

    message += 'Changing certification background and logo and adding instructor signatures:\n\n'
    message += 'To change the image of the logo (used in the certificate), '
    message += f'replace the existing "{logo_image_name}" file in the "{image_assets_folder_path}" folder with another '
    message += f'file named "{logo_image_name}". '
    message += f'The recommended size is {recommended_logo_width} x {recommended_logo_height}.\n\n'
    message += 'To change the image of the background (used as the pdf certificate background), '
    message += f'replace the existing "{background_image_name}" file in the "{image_assets_folder_path}" folder with another file '
    message += f'named "{background_image_name}". '
    message += f'The recommended size is {recommended_background_width} x {recommended_background_height}. \n\n'
    message += f'You can add or delete images with instructors signatures to/from "{instructor_signatures_folder_path}" '
    message += 'folder. The added file needs to be a png, and the name of the file has to match exactly the name of '
    message += 'the instructor as presented in the csv. The recommended height of the image 70px'

    messagebox.showinfo('Help', message)

# ================ User interface configuration ================
# set the color theme (customtkinter built-in)
set_appearance_mode('Dark')
set_default_color_theme('blue')

widget_width = 300

# create and configure the window
window = CTk()
window.geometry('400x350')
# create a name for the window
window.title('Certifications creator')

# title label
title_label = CTkLabel(window,
                       text='Certifications creator',
                       font=('Helvetica', 16, 'bold'),
                       text_color=light_text_color)
title_label.pack(pady=10)

# reporting text area
reporting_text_area = CTkTextbox(window,
                                 height=150,
                                 width=widget_width,
                                 text_color=light_text_color)
reporting_text_area.pack(pady=10)
greeting_text = '''Hello!

To get started, press the "Browse csv file" 
button below. Search for your csv, select it,
click "open", and the app will create the 
certifications pdfs files.'''
write_in_textbox(greeting_text)

# file selection and pdf create button
csv_select_and_pdf_creator_button = CTkButton(window,
                                              text='Browse csv file',
                                              command=make_certifications,
                                              text_color=light_text_color,
                                              fg_color=lighter_bg_color,
                                              hover_color=darker_bg_color,
                                              width=widget_width)
csv_select_and_pdf_creator_button.pack(pady=5)

# help button
help_button = CTkButton(window,
                        text='Help',
                        command=help_message,
                        width=20,
                        text_color=help_text_color,
                        fg_color=darker_bg_color,
                        hover_color=lighter_bg_color)
help_button.place(x=350, y=10)

# close button
close_button = CTkButton(window,
                         text='Close',
                         command=window.destroy,
                         text_color=close_text_color,
                         fg_color=darker_bg_color,
                         hover_color=lighter_bg_color,
                         width=widget_width)
close_button.pack(pady=5)

window.mainloop()
