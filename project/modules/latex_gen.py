from pylatex import Document, Command, NoEscape

from project.utils.path_utils import photo_cv, json_data, latex_var, pdfoutput_noext
from project.utils.data_handler import LatexVarGenerator, escape_latex

def generate_latex(generator):
    #region LATEX options
    geometry_options = {"tmargin": "1cm", 
                        "lmargin": "10cm",
                        "left": "1.25cm",
                        "right": "1.25cm",
                        "top": "1.5cm",
                        "bottom": "1.5cm",
                        "columnsep": "1.2cm"}
    document_options = ['10pt',
                    'a4paper',
                    'ragged2e',
                    'withhyper']
    column_ratio = 0.3
    photo_size = "2.8cm"
    # Doc creation
    doc = Document(geometry_options=geometry_options,
                documentclass='altacv', 
                document_options=document_options)

    doc.preamble.append(Command('usepackage', 'paracol'))

    # Conditional for ifutex
    doc.preamble.append(NoEscape(r'''
    \iftutex
        \setmainfont{Roboto Slab}
        \setsansfont{Lato}
        \renewcommand{\familydefault}{\sfdefault}
    \else
        \usepackage[rm]{roboto}
        \usepackage[defaultsans]{lato}
        \usepackage{sourcesanspro}
        \renewcommand{\familydefault}{\sfdefault}
    \fi
    '''))

    # Define colors
    doc.preamble.append(NoEscape(r'''
    \definecolor{SlateGrey}{HTML}{2E2E2E}
    \definecolor{LightGrey}{HTML}{666666}
    \definecolor{DarkPastelRed}{HTML}{450808}
    \definecolor{PastelRed}{HTML}{8F0D0D}
    \definecolor{GoldenEarth}{HTML}{E7D192}
    \colorlet{name}{black}
    \colorlet{tagline}{PastelRed}
    \colorlet{heading}{DarkPastelRed}
    \colorlet{headingrule}{GoldenEarth}
    \colorlet{subheading}{PastelRed}
    \colorlet{accent}{PastelRed}
    \colorlet{emphasis}{SlateGrey}
    \colorlet{body}{LightGrey}
    '''))

    # Renew commands
    doc.preamble.append(NoEscape(r'''
    \renewcommand{\namefont}{\Huge\rmfamily\bfseries}
    \renewcommand{\personalinfofont}{\footnotesize}
    \renewcommand{\cvsectionfont}{\LARGE\rmfamily\bfseries}
    \renewcommand{\cvsubsectionfont}{\large\bfseries}
    \renewcommand{\cvItemMarker}{{\small\textbullet}}
    \renewcommand{\cvRatingMarker}{\faCircle}
    '''))

    #endregion

    doc.append(NoEscape(r'\input{latex_var}'))  # Include generated variables

    name_value = generator.get_value('personal.name')
    doc.append(NoEscape(f'\\name{{{name_value}}}'))
    tagline_value = generator.get_value('personal.tagline')
    doc.append(NoEscape(f'\\tagline{{{tagline_value}}}'))
    doc.append(NoEscape(f'\\photoR{{{photo_size}}}{{{photo_cv}}}'))

    email_value = generator.get_value('personal.email')
    location_value = generator.get_value('personal.location')
    linkedin_value = generator.get_value('personal.linkedin')
    doc.append(NoEscape(f'''\\personalinfo{{
        \\email{{{email_value}}}
        \\location{{{location_value}}}
        \\linkedin{{{linkedin_value}}}
    }}
    \\makecvheader
    \\columnratio{{{column_ratio}}}
    \\begin{{paracol}}{{2}}
    '''))

    doc.append(NoEscape(r'\cvsection{Skills}'))
    skill_list = generator.data['skills']
    for skill in skill_list:
        skill_processed = escape_latex(skill)
        doc.append(NoEscape(f'''\\textbf{{{skill_processed}}}

    '''))


    doc.append(NoEscape(r'''
                        
    \cvsection{Trainings}'''))

    training_list = generator.data['trainings']  # Access the list of experiences
    # Loop through each experience and format it for LaTeX
    for index, training in enumerate(training_list):
        title = escape_latex(training['title'])
        school = escape_latex(training['school'])
        date = escape_latex(training['date'])
        location = escape_latex(training['location'])
        
        # Format as LaTeX command
        
        if index == len(training_list) - 1:
            doc.append(NoEscape(f'''\\textbf{{{title}}} 

    {school} {date} 

    \\textit{{{location}}}

    '''))
        else:
            doc.append(NoEscape(f'''\\textbf{{{title}}} 

    {school} {date} 

    \\textit{{{location}}}

    \divider

    '''))

    doc.append(NoEscape(r'''
    \cvsection{Languages}'''))

    language_list = generator.data['languages']  # Access the list of experiences
    for index, language_data in enumerate(language_list):
        language_v = escape_latex(language_data['language'])
        level = escape_latex(language_data['level'])
            
        if index == len(language_list) - 1:
            doc.append(NoEscape(f'''\\textbf{{{language_v}}}
    \hfill
    {level}

    '''))
        else:
            doc.append(NoEscape(f'''\\textbf{{{language_v}}} 
    \hfill
    {level}

    \divider

    '''))


    doc.append(NoEscape(r'''

    \cvsection{Hobbies}'''))

    hobby_list = generator.data['hobbies']  # Access the list of experiences
    for index, hobby in enumerate(hobby_list):
        # Format as LaTeX command
        hobby_processed = escape_latex(hobby)
        if index == 0:
            doc.append(NoEscape(f'{{\\LaTeXraggedright \\cvtag{{{hobby_processed}}}'))
        elif index == len(hobby_list) - 1:
            doc.append(NoEscape(f'\\cvtag{{{hobby_processed}}} \\par}}'))
        else:
            doc.append(NoEscape(f'\\cvtag{{{hobby_processed}}}'))

    doc.append(NoEscape(r'''
    \switchcolumn
    '''))

    doc.append(NoEscape(r'''
    \cvsection{Professionnal experiences}'''))

    experience_list = generator.data['experiences']  # Access the list of experiences
    # Loop through each experience and format it for LaTeX
    for experience in experience_list:
        title = escape_latex(experience['title'])
        company = escape_latex(experience['company'])
        date = escape_latex(experience['date'])
        location = escape_latex(experience['location'])
        
        # Format as LaTeX command
        doc.append(NoEscape(f'\\cvevent{{{title}}}{{{company}}}{{{date}}}{{{location}}}'))

        doc.append(NoEscape(r'''\begin{itemize}
    '''))
        experience_description_list = experience['description']
        for description_data in experience_description_list:
            description_data_processed = escape_latex(description_data)
            doc.append(NoEscape(f'\\item{{{description_data_processed}}}'))
        doc.append(NoEscape(r'''\end{itemize}
    {\LaTeXraggedright
    '''))
        experience_tag_list = experience['tags']
        for tag_data in experience_tag_list:
            tag_data_processed = escape_latex(tag_data)
            doc.append(NoEscape(f'\\cvtag{{{tag_data}}} '))
        doc.append(NoEscape(r'''\par}

    \divider

    '''))

    doc.append(NoEscape(r'''\end{paracol}
    '''))

    # Generate the PDF at the specified path
    doc.generate_pdf(pdfoutput_noext, clean_tex=False)

    print(f"PDF generated at: {pdfoutput_noext}")

if __name__ == "__main__":
    # Load variables from JSON
    generator = LatexVarGenerator(json_data, latex_var_name='user') # Initialize with the JSON file
    generator.generate_latex_vars(latex_var) # Generate variables.tex

    generate_latex(generator)

