import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import sys

# python3 process_results.py ../portafolio_2021

data = pd.read_csv('notas.csv')
classes_type = ['Excelente', 'Bueno', 'Aceptable', 'Mejorable', 'Deficiente']
path_portafolio = sys.argv[1]

# agrega una columna class (excelente, bueno aceptable, mejorable y deficiente), segun la nota
def add_class(data, grade_type):
    new_data = data.copy()
    
    classes = []
    for index, row in data.iterrows():
        if row[grade_type] >= 17:
            classes.append(classes_type[0])
        if row[grade_type] >= 14 and row[grade_type] <= 16:
            classes.append(classes_type[1])
        if row[grade_type] >= 11 and row[grade_type] <= 13:
            classes.append(classes_type[2])
        if row[grade_type] >= 7 and row[grade_type] <= 10:
            classes.append(classes_type[3])
        if row[grade_type] <= 6:
            classes.append(classes_type[4])

    new_data.insert(2, "Clase", classes, True)
    return new_data

def get_groups(data):
    return data['GRUPO'].unique()


def process_grade(grade_type, data):
    column = data[grade_type]
    max_grade = column.max()
    min_grade = column.min()
    mean_grade = column.mean()

    cond_1 = data.apply(lambda x : True if x[grade_type] >= 17 else False, axis = 1)
    cond_2 = data.apply(lambda x : True if x[grade_type] >= 14 and x[grade_type] <= 16 else False, axis = 1)
    cond_3 = data.apply(lambda x : True if x[grade_type] >= 11 and x[grade_type] <= 13 else False, axis = 1)
    cond_4 = data.apply(lambda x : True if x[grade_type] >= 7 and x[grade_type] <= 10 else False, axis = 1)
    cond_5 = data.apply(lambda x : True if x[grade_type] <= 6 else False, axis = 1)

    grades_1 = len(cond_1[cond_1 == True].index)
    grades_2 = len(cond_2[cond_2 == True].index)
    grades_3 = len(cond_3[cond_3 == True].index)
    grades_4 = len(cond_4[cond_4 == True].index)
    grades_5 = len(cond_5[cond_5 == True].index)

    #grades_1 = data[data[grade] >= 14][grade].count()
    #grades_2 = data[data[grade] >= 14 and data[grade] <= 16]
    #grades_3 = data[data[grade] >= 11 and data[grade] <= 13][grade].count()
    #grades_4 = data[data[grade] >= 7 and data[grade] <= 10][grade].count()
    #grades_5 = data[data[grade] <= 6][grade].count()

    return [max_grade, min_grade, mean_grade, grades_1, grades_2, grades_3, grades_4, grades_5]

def plot_hist(grade_type, data, groups):
    plt.clf()    
    sb.set_style('white')
    sb.displot(data, x=grade_type, col="GRUPO", multiple="dodge", bins = 5)
    plt.savefig(path_portafolio + '/imgs/hist_' + grade_type + '.png', bbox_inches='tight', dpi=500)

    new_data = add_class(data, grade_type)
    plt.clf()    
    #sb.set_style('white')
    #sb.displot(data, x=grade_type, color='g', bins = [1,6,10,13,16,20], discrete=True)
    sb.countplot(x="Clase", data=new_data, palette="Set2", order=classes_type)
    plt.savefig(path_portafolio + '/imgs/hist_all_' + grade_type + '.png', bbox_inches='tight', dpi=500)
    
def build_tex(grade_type, data, results, groups):
    tex = """    
    \clearpage
    \\begin{table}[H]
    \\centering
		\\begin{tabular}{|x{\\textwidth}|}
			\hline 
            \MakeUppercase{\csuniversidad} \\\\
            \\\\
            \\begin{minipage}{.3\\textwidth}
				\includegraphics[width=\\textwidth]{../imgs/cs2}
	        \end{minipage} \\\\
        	\\\\
            \\textbf{\MakeUppercase{\csepcc}} \\\\
            \MakeUppercase{\csfacultad} \\\\
            \MakeUppercase{\csdepartamento} \\\\
			\hline 
		\end{tabular}
	\end{table}


    %\\begin{figure}				
	%			\includegraphics[width=\\textwidth]{../imgs/cs}
	%\end{figure}
    \centering
    \\textbf{INFORME DE RESULTADOS}    
    """

    tex += """    
    \\begin{table}[H]
    \\centering
		\\begin{tabular}{|p{4cm}|p{2cm}|}
			\hline 
			\\textbf{Nota máxima} & """ + str(results[0]) + """   \\\\
			\hline 
            \\textbf{Nota mínima} & """ + str(results[1]) + """   \\\\
			\hline
			\\textbf{Nota promedio} &  """ + str(round(results[2])) + """   \\\\
			\hline 
		\end{tabular}
	\end{table}	
    """

    if len(groups) == 1:
        img_width = '0.6'
    else:
        img_width = ''
    tex += """  
    \\begin{flushleft}
    En la Figura \\ref{fig:hist_""" + grade_type + """}, detallamos el histograma de frecuencias de las
    notas por grupo y en la Figura \\ref{fig:hist_all_""" + grade_type + """}, mostramos el consolidado. 
    \\end{flushleft}

    \\begin{figure}[H]	
    \centering 		
				\includegraphics[width=""" + img_width + """\\textwidth]{../imgs/hist_""" + grade_type + """.png}
                \caption{Histograma de notas.}
                \label{fig:hist_""" + grade_type + """}
	\end{figure}

    \\begin{figure}[H]	
    \\centering 		
				\includegraphics[width=0.6\\textwidth]{../imgs/hist_all_""" + grade_type + """.png}
                \caption{Histograma de notas (consolidado). Excelente (nota $\geq$ 17), Bueno (14 $\leq$ nota $\leq$ 16), Aceptable (11 $\leq$ nota $\leq$ 13), Mejorable (07 $\leq$ nota $\leq$ 10), Deficiente ( nota $\leq$ 06)}
                \label{fig:hist_all_""" + grade_type + """}
	\end{figure}
    """

    # notas

    for gr in groups:
        group = data[data['GRUPO'] == gr]
        tex += """  

        \\begin{table}[H]
        \centering
            \\caption{Notas del grupo """ + gr + """.}
            \\begin{tabular}{|c|p{10cm}|c|}
                \hline 
                \\textbf{CUI} & \\textbf{ALUMNO} & \\textbf{NOTA}  \\\\ \hline
        """    
        for index, row in group.iterrows():
            tex +=  str(row['CUI']) + " & " + row['ALUMNO'] + " & " + str(row[grade_type]) + """ \\\\ \hline 
            """
        tex += """		
            \end{tabular}
        \end{table}	
        """
    
    f = open(path_portafolio + "/texs/inf_" + grade_type + ".tex", "w")
    f.write(tex)
    f.close()

def build_all(data):
    column_grade_types = ['EP0', 'EP1', 'EC1', 'EP2', 'EC2', 'EP3', 'EC3']

    groups = get_groups(data)

    for cgrade_type in column_grade_types:
        if data[cgrade_type].isnull().values.any():
            continue

        results = process_grade(cgrade_type, data)
        plot_hist(cgrade_type, data, groups)
        build_tex(cgrade_type, data, results, groups)


if __name__ == "__main__":
    build_all(data)