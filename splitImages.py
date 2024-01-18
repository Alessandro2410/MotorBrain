from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from plotnine import *
import pandas as pd
import os
from tkinter import ttk
from tkinter import messagebox
import math

#salvo i percorsi dei file
users=pd.read_csv("/Users/ale.ino/Desktop/MotorBrain 2 copia/File csv/user.csv", sep=";")
dom_hand=pd.read_csv("/Users/ale.ino/Desktop/MotorBrain 2 copia/File csv/domHandCircle.csv")
prova_tutti_utenti=pd.read_csv("/Users/ale.ino/Desktop/MotorBrain 2 copia/File csv/provaTuttiUtenti.csv")
 
dest_folder = "/Users/ale.ino/Desktop/MotorBrain 2 copia/Plots/" #creo la cartella dove vengono salvati i grafici creati 

#determino la grandezza minima delle figure visualizzate
dim_width= 100
dim_height=100

num_plots=0

#size_value=1

#definisco la classe e creo un'instanza della classe
class ImageContainer:
    def __init__(self):
        self.plot_image = []

image_container = ImageContainer()

checkbox_state = False
#checkbox_state1=False
radio_value=1

#funzioni per abilitare le checkbox
def on_checkbox_click():
    global checkbox_state
    checkbox_state = check.get()

#def on_checkbox_click1():
#    global checkbox_state1
#    checkbox_state1 = check1.get()

#funzione per abilitare i radio button 
def on_radio_select():
    global radio_value
    radio_value = vis_var.get()


#creo una funzione che mi permette di selezionare il file escludendo quelli che non sono .csv
#se non seleziono un file il bottone di visualizzazione non viene abilitato. 
def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        file_name = filepath.split("/")[-1]
        file_name = file_name.split(".csv")[0]
        input_data = load_data(filepath)
        file_label.config(text=f"{file_name}")
        go_button.config(state=NORMAL)  #quando ho caricato il file il bottone viene abilitato 
        return input_data
    else:
        #il messaggio compare quando viene chiusa la cartella 
        messagebox.showerror("Oops!", "Selezionare un file .csv che contenga le traiettorie degli utenti")


#funzione per caricare il file selezionato
def load_data(filepath):
    global input
    input = pd.read_csv(filepath, sep=";")
    return input

#funzione che mi permette di sapere il numero totale degli utenti
def get_num_voices(users):
    
    # Converte il numero di voci(rows) in una stringa
    num_voices_str = str(users.shape[0])

    return num_voices_str

#funzione che mi permette di sapere il numero totale degli utenti. 
def get_num_voices_int(users):
    
    # Converte il numero di voci(rows) in un intero
    num_voices_int = int(users.shape[0])

    return num_voices_int

#faccio in modo che se l'utente inserisce un numero minore o uguale al del totale degli utenti il bottone di visualizzazione viene abilitato
#se vengono inseriti caratteri diversi da numeri interi il bottone rimane disabilitato        
def on_entry_key_release(event):
    current_value = entry_plots.get()
    is_valid_input = False  # Flag che serve per vedere se l'input è un intero
    
    try:
        # converto l'input in intero 
        value = int(current_value)
        
        # controllo se l'input è maggiore del totale degli utenti 
        if value > get_num_voices_int(users):
            # disabilito il bottone e il colore dei caratteri diventa grigio 
            go_button.config(state=DISABLED)
            entry_plots.config(fg='grey')
        else:
            # altrimenti il bottone viene abilitato e i caratteri diventano di colore bianco 
            go_button.config(state=NORMAL)
            entry_plots.config(fg='white')
            is_valid_input = True  # il flag diventa true 
    
    except ValueError:
        #se l'input non è un intero valido, disabilito il bottone e il colore dei caratteri lo setto a grigio 
        go_button.config(state=DISABLED)
        entry_plots.config(fg='grey')

    #resetto il colore del testo a bianco 
    if current_value == 'max' + get_num_voices(users):
        entry_plots.config(fg='white')  

    # ulteriore controllo se l'input contiene lettere e tiene il bottone disabilitato (es: se scrivo 3m il bottone rimane disabilitato )
    if not is_valid_input:
        go_button.config(state=DISABLED)
        entry_plots.config(fg='grey')

def on_entry_number_release(event):
    current_value = entry_width.get()
    is_valid_input = False  # Flag che serve per vedere se l'input è un intero
    value=None

    try:
        # converto l'input in intero 
        value = int(current_value)
        
        # controllo se l'input è maggiore o uguale a 100
        if value >= 100:
            # abilito il bottone e il colore dei caratteri diventa bianco 
            go_button.config(state=NORMAL)
            entry_width.config(fg='white')
            is_valid_input = True  # il flag diventa true 
        else:
            # altrimenti disabilito il bottone e il colore dei caratteri diventa grigio
            go_button.config(state=DISABLED)
            entry_width.config(fg='grey')
    
    except ValueError:
        # se l'input non è un intero valido, disabilito il bottone e il colore dei caratteri lo setto a grigio 
        go_button.config(state=DISABLED)
        entry_width.config(fg='grey')

    # resetto il colore del testo a bianco 
    if current_value == 'max' + str(value):
        entry_width.config(fg='white')  

    # ulteriore controllo se l'input contiene lettere tengo il bottone disabilitato (es: se scrivo eee il bottone rimane disabilitato )
    if not is_valid_input:
        go_button.config(state=DISABLED)
        entry_width.config(fg='grey')

#funzione che elimina dalla cartella le immagini generate una volta chiusa l'app
def cleanup_images(dest_folder, users, num_plots, cases):

    # Converto cases in una lista se non lo è già
    if not isinstance(cases, list):
        cases = [cases]

    # Definisco i 4 modi in cui sono stati salvati i plot
    for case in cases:
        for i in range(num_plots):
            if case == 1:
                for userID_to_select in users['userID'].head(num_plots):
                    for hand in prova_tutti_utenti[prova_tutti_utenti['userID'] == userID_to_select]['hand'].unique():
                        for repetitionID in prova_tutti_utenti[(prova_tutti_utenti['userID'] == userID_to_select) & (prova_tutti_utenti['hand'] == hand)]['repetitionID'].unique():
                            image_path = f'{dest_folder}plot_user_{userID_to_select}_hand_{hand}_repetition_{repetitionID}.png'
                            if os.path.exists(image_path):
                                os.remove(image_path)
            
            elif case == 2:
                for userID_to_select in users['userID'].head(num_plots):
                    for repetitionID in dom_hand[dom_hand['userID'] == userID_to_select]['repetitionID'].unique():
                        image_path = f'{dest_folder}plot_user_{userID_to_select}_repetition_{repetitionID}.png'
                        if os.path.exists(image_path):
                            os.remove(image_path)
            
            elif case == 3:
                for userID_to_select in users['userID'].head(num_plots):
                    for hand in prova_tutti_utenti[prova_tutti_utenti['userID'] == userID_to_select]['hand'].unique():
                        image_path = f'{dest_folder}plot_user_{userID_to_select}_hand_{hand}.png'
                        if os.path.exists(image_path):
                            os.remove(image_path)
                
            elif case == 4:
                userID_to_select = users['userID'].iloc[0] if not users.empty else None
                image_path = f'{dest_folder}plot{i}.png'
                if os.path.exists(image_path):
                    os.remove(image_path)

            
# funzione che elimina le immagini alla chiusura dell'applicazione
def on_closing():
    cleanup_cases = [1,2,3,4] 
    cleanup_plots(cleanup_cases)
    window.destroy()

# funzione che elimina le immagini alla chiusura dell'applicazione 
def cleanup_plots(cases):
    for widget in frame_visualization.winfo_children():
        widget.destroy()

    for case in cases:
        cleanup_images(dest_folder, users, num_plots, case)

#funzione che crea e dispone i grafici
def display_plots():

    global num_plots, dim_width, dim_height
    
    cleanup_cases = [1, 2, 3, 4]
    cleanup_plots(cleanup_cases)

    try:
        num_plots = int(entry_plots.get())
        dim_width=int(entry_width.get())
        size_value=int(entry_size.get())
        dim_height=dim_width / 1.2

    except ValueError:
        pass 

    entry_width.config(state=DISABLED) #lascio fissa la dimensione dei canvas
    # Calcolo la larghezza dello schermo
    screen_width = window.winfo_screenwidth()

    # Calcolo il numero di colonne partendo dalla larghezza dello schermo e dalle dimensioni delle figure
    num_columns = max(screen_width // dim_width, 1)
    
    # Calcolo il numero di righe basandomi sul numero di colonne specificato
    num_rows = (num_plots + num_columns - 1) // num_columns

    canvas_width = dim_width * num_columns #calcolo la dimensione del canvas

    canvas = Canvas(frame_visualization,  width=canvas_width, height=dim_height * num_rows) #creo il canvas
    canvas.grid(row=0, column=0, sticky="nsew") #il canvas si estende per tutta la grandezza della cella

    #creo una scrollbar verticale
    scrollbar = ttk.Scrollbar(frame_visualization, orient="vertical", command=canvas.yview) 
    scrollbar.grid(row=0, column=1, sticky='ns')

    canvas.configure(yscrollcommand=scrollbar.set)  #permette lo scrolling dall'alto verso il basso

    # creo un frame per contenere nel canvas i grafici
    plot_frame = Frame(canvas)
    canvas.create_window((0, 0), window=plot_frame, anchor=NW)

    #definisco come organizzare lo spazio in modo da distruibuire equamente i grafici
    plot_frame.columnconfigure(0, weight=1)
    plot_frame.rowconfigure(0, weight=1)

    #variabile per posizionare lo scrolling a partire dall'altezza totale della finestra
    total_inner_height = 0

    #Small multiples mano dominante  
    if checkbox_state and radio_value==1:

        # Creo e visualizzo i plot e li organizzo in colonna
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):
            utenteConsiderato = dom_hand[dom_hand['userID'] == userID_to_select]

            traiettoria=pd.merge(utenteConsiderato, input, how="left", on=["sessionID", "repetitionID"])

            #da tenere nel caso si volessero visualizzare le info aggiuntive quali id e mano dominante
            #first_user_id = traiettoria['userID'].iloc[0]
            #first_hand_id = traiettoria['hand'].iloc[0]  

            #creo i plot utilizzando i dati dei file
            vis=ggplot()+geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria, size=size_value)
            vis=vis+theme(axis_text_x=element_blank(),axis_text_y=element_blank(),axis_title_x=element_blank(),axis_title_y=element_blank(),axis_ticks=element_blank(),panel_background=element_blank(), panel_grid_major=element_blank(), panel_grid_minor=element_blank(), legend_position='none', plot_background=element_blank()) #per tenere la legenda togliere legend_position='none' e se si vuole modificare la grande legend_key_size=10
            vis=vis+coord_fixed() #labs(color='Ripetizione', title=f"{first_user_id, first_hand_id}") crea la legenda più associa l'id e la mano dominante al plot
            #salvo i plot in una cartella 
            vis.save(f'{dest_folder}plot{i}.png', dpi=500)

            # carico l'immagine in un oggetto PhotoImage
            img = Image.open(f'{dest_folder}plot{i}.png')
            resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS) 
            image_container.plot_image.append(ImageTk.PhotoImage(resized_image))
        
            #viene assegnato un canvas per ogni plot creato
            vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
            vis_canvas.grid(row=i // num_columns, column=i % num_columns)

            canvas_width = dim_width
            canvas_height = dim_height
            image_width, image_height = resized_image.size

            x_position = (canvas_width - image_width) // 2
            y_position = (canvas_height - image_height) // 2

            # visualizzo i plot nel canvas alla posizione assegnata
            vis_canvas.create_image(x_position, y_position, anchor=NW, image=image_container.plot_image[-1])


            # calcolo il raggio massimo che il canvas può contenere
            max_radius = min(dim_width, dim_height) / 2

            # setto un offset verticale in percentuale 
            vertical_offset_percentage = 25  

            # creo le dimensioni del cerchio
            circle_radius_outer = max_radius * 0.83  
            circle_radius_inner = circle_radius_outer * 0.78  

            circle_vertical_offset = (dim_height - circle_radius_outer * 2) * vertical_offset_percentage / 100
            circle_horizontal_offset = (dim_width - circle_radius_outer * 2) / 2

            # centro le coordinate dei cerchi con gli offset verticali e orizzontali
            circle_center_x = circle_radius_outer + circle_horizontal_offset
            circle_center_y = circle_radius_outer + circle_vertical_offset

            # cerchio esterno
            vis_canvas.create_oval(circle_center_x - circle_radius_outer,circle_center_y - circle_radius_outer,circle_center_x + circle_radius_outer,circle_center_y + circle_radius_outer,outline="white", width=1)

            # cerchio interno
            vis_canvas.create_oval(circle_center_x - circle_radius_inner,circle_center_y - circle_radius_inner,circle_center_x + circle_radius_inner,circle_center_y + circle_radius_inner,outline="white",width=1)
            
            # aggiorno l'altezza totale della finestra
            total_inner_height += vis_canvas.winfo_reqheight()
         
        #configurazione della scrollbar per il corretto posizionamento e funzionamento    
        canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))


    #visualizzazioni singole per ogni ripetizione solo con mano dominante in canvas separati  
    elif checkbox_state and radio_value==2:
    
        # Creo e visualizzo i plot e li organizzo in colonna
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):
            utenteConsiderato = dom_hand[dom_hand['userID'] == userID_to_select]

            for j, repetitionID in enumerate(utenteConsiderato['repetitionID'].unique()):
                repetition_data = utenteConsiderato[utenteConsiderato['repetitionID'] == repetitionID]

                traiettoria = pd.merge(repetition_data, input, how="left", on=["sessionID", "repetitionID"])
            
                #first_user_id = traiettoria['userID'].iloc[0]
                #first_hand_id = traiettoria['hand'].iloc[0]

                vis=ggplot()+geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria, size=size_value)+ facet_grid(".~repetitionID")+ coord_fixed()
                vis=vis+theme(axis_text_x=element_blank(),axis_text_y=element_blank(),axis_title_x=element_blank(),axis_title_y=element_blank(),axis_ticks=element_blank(),panel_background=element_blank(), strip_background_x=element_blank(),strip_text_x=element_blank(),legend_position='none', panel_grid_major=element_blank(), panel_grid_minor=element_blank() ,plot_background=element_blank()) #strip_text_x e strip_background_x tolgono le label grige e il testo dentro

                vis.save(f'{dest_folder}plot_user_{userID_to_select}_repetition_{repetitionID}.png', dpi=500)
        
                # carico l'immagine in un oggetto PhotoImage
                img = Image.open(f'{dest_folder}plot_user_{userID_to_select}_repetition_{repetitionID}.png')
                resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS) 
                image_container.plot_image.append(ImageTk.PhotoImage(resized_image))

                total_plots = len(users['userID'].head(num_plots)) * len(utenteConsiderato['repetitionID'].unique())
                total_columns = min(total_plots, num_columns)

                row_position = (i * len(utenteConsiderato['repetitionID'].unique()) + j) // total_columns
                col_position = (i * len(utenteConsiderato['repetitionID'].unique()) + j) % total_columns

                vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
                vis_canvas.grid(row=row_position, column=col_position, padx=0, pady=0)

                canvas_width = dim_width
                canvas_height = dim_height
                image_width, image_height = resized_image.size

                x_position = (canvas_width - image_width) // 2
                y_position = (canvas_height - image_height) // 2

                vis_canvas.create_image(x_position, y_position, anchor=NW, image=image_container.plot_image[-1])

                max_radius = min(dim_width, dim_height) / 2

                vertical_offset_percentage = 25  

                circle_radius_outer = max_radius * 0.83  
                circle_radius_inner = circle_radius_outer * 0.78  

                circle_vertical_offset = (dim_height - circle_radius_outer * 2) * vertical_offset_percentage / 100
                circle_horizontal_offset = (dim_width - circle_radius_outer * 2) / 2

                
                circle_center_x = circle_radius_outer + circle_horizontal_offset
                circle_center_y = circle_radius_outer + circle_vertical_offset

                vis_canvas.create_oval(circle_center_x - circle_radius_outer,circle_center_y - circle_radius_outer,circle_center_x + circle_radius_outer,circle_center_y + circle_radius_outer,outline="white", width=1)

                vis_canvas.create_oval(circle_center_x - circle_radius_inner,circle_center_y - circle_radius_inner,circle_center_x + circle_radius_inner,circle_center_y + circle_radius_inner,outline="white",width=1)

                # aggiorno l'altezza totale della finestra
                total_inner_height += vis_canvas.winfo_reqheight()

            #configurazione della scrollbar per il corretto posizionamento e funzionamento    
            canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))
    
    
    #visualizzazioni singole per ogni ripetizione con entrambe le mani  
    elif radio_value==2:
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):
            utenteConsiderato_circle = prova_tutti_utenti[prova_tutti_utenti['userID'] == userID_to_select]

            for k, hand in enumerate(utenteConsiderato_circle['hand'].unique()):
                for j, repetitionID in enumerate(utenteConsiderato_circle[utenteConsiderato_circle['hand'] == hand]['repetitionID'].unique()):
                    traiettoria_utente = pd.merge(utenteConsiderato_circle[(utenteConsiderato_circle['repetitionID'] == repetitionID) & (utenteConsiderato_circle['hand'] == hand)], input, how="left", on=["sessionID", "repetitionID"])

            
                    vis = ggplot() + geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria_utente, size=size_value) + facet_grid("hand~repetitionID") + coord_fixed()

                    vis = vis +  theme(axis_text_x=element_blank(), axis_text_y=element_blank(), axis_title_x=element_blank(), axis_title_y=element_blank(), axis_ticks=element_blank(), panel_background=element_blank(), strip_background_x=element_blank(), strip_text_x=element_blank(), strip_background_y=element_blank(), strip_text_y=element_blank(),panel_grid_major=element_blank(), panel_grid_minor=element_blank() ,plot_background=element_blank(), legend_position='none')

                    vis.save(f'{dest_folder}plot_user_{userID_to_select}_hand_{hand}_repetition_{repetitionID}.png', dpi=500)

                    
                    img = Image.open(f'{dest_folder}plot_user_{userID_to_select}_hand_{hand}_repetition_{repetitionID}.png')
                    resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS)
                    image_container.plot_image.append(ImageTk.PhotoImage(resized_image))

                    
                    total_plots = len(users['userID'].head(num_plots)) * len(utenteConsiderato_circle['hand'].unique()) * len(utenteConsiderato_circle['repetitionID'].unique())
                    total_columns = min(total_plots, num_columns)

                    row_position = (i * len(utenteConsiderato_circle['hand'].unique()) * len(utenteConsiderato_circle['repetitionID'].unique()) + k * len(utenteConsiderato_circle['repetitionID'].unique()) + j) // total_columns
                    col_position = (i * len(utenteConsiderato_circle['hand'].unique()) * len(utenteConsiderato_circle['repetitionID'].unique()) + k * len(utenteConsiderato_circle['repetitionID'].unique()) + j) % total_columns

                    
                    vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
                    vis_canvas.grid(row=row_position, column=col_position, padx=0, pady=0)

                    canvas_width = dim_width
                    canvas_height = dim_height
                    image_width, image_height = resized_image.size

                    x_position = (canvas_width - image_width) // 2
                    y_position = (canvas_height - image_height) // 2

                    
                    vis_canvas.create_image(x_position, y_position, anchor=NW, image=image_container.plot_image[-1])

                    
                    max_radius = min(dim_width, dim_height) / 2

                    
                    vertical_offset_percentage = 25  

                    
                    circle_radius_outer = max_radius * 0.83  
                    circle_radius_inner = circle_radius_outer * 0.78  

                    circle_vertical_offset = (dim_height - circle_radius_outer * 2) * vertical_offset_percentage / 100
                    circle_horizontal_offset = (dim_width - circle_radius_outer * 2) / 2

                    circle_center_x = circle_radius_outer + circle_horizontal_offset
                    circle_center_y = circle_radius_outer + circle_vertical_offset

                   
                    vis_canvas.create_oval(circle_center_x - circle_radius_outer,circle_center_y - circle_radius_outer,circle_center_x + circle_radius_outer,circle_center_y + circle_radius_outer,outline="white", width=1)

                    
                    vis_canvas.create_oval(circle_center_x - circle_radius_inner,circle_center_y - circle_radius_inner,circle_center_x + circle_radius_inner,circle_center_y + circle_radius_inner,outline="white",width=1)

                    # aggiorno l'altezza totale della finestra
                    total_inner_height += vis_canvas.winfo_reqheight()

                #configurazione della scrollbar per il corretto posizionamento e funzionamento    
                canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))

    #small multiples per entrambe le mani 
    else: 
        
        # Creo e visualizzo i plot e li organizzo in colonna
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):        
            utenteConsiderato_circle = prova_tutti_utenti[prova_tutti_utenti['userID'] == userID_to_select]

            for j, hand in enumerate(utenteConsiderato_circle['hand'].unique()):
                traiettoria_utente = pd.merge(utenteConsiderato_circle[(utenteConsiderato_circle['hand'] == hand)], input, how="left", on=["sessionID", "repetitionID"])
                
                #first_user_id = traiettoria_utente['userID'].iloc[0]
                #first_hand_id = traiettoria_utente['hand'].iloc[0]

                vis=ggplot()+coord_fixed()+geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria_utente, size=size_value)+facet_grid(".~hand")
                vis=vis+theme(axis_text_x=element_blank(),axis_text_y=element_blank(),axis_title_x=element_blank(),axis_title_y=element_blank(),axis_ticks=element_blank(),panel_background=element_blank(),strip_background_x=element_blank(), strip_text_x=element_blank(),panel_grid_major=element_blank(), panel_grid_minor=element_blank(), legend_position='none', plot_background=element_blank())

                vis.save(f'{dest_folder}plot_user_{userID_to_select}_hand_{hand}.png', dpi=500)
        
        
                # carico l'immagine in un oggetto PhotoImage
                img = Image.open(f'{dest_folder}plot_user_{userID_to_select}_hand_{hand}.png')
                resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS) 
                image_container.plot_image.append(ImageTk.PhotoImage(resized_image))

                
                total_plots = len(users['userID'].head(num_plots)) * len(utenteConsiderato_circle['hand'].unique())
                total_columns = min(total_plots, num_columns)

                
                row_position = (i * len(utenteConsiderato_circle['hand'].unique()) + j) // total_columns
                col_position = (i * len(utenteConsiderato_circle['hand'].unique()) + j) % total_columns


                #viene assegnato un canvas per ogni plot creato
                vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
                vis_canvas.grid(row=row_position, column=col_position, padx=0, pady=0)

                canvas_width = dim_width
                canvas_height = dim_height
                image_width, image_height = resized_image.size

                x_position = (canvas_width - image_width) // 2
                y_position = (canvas_height - image_height) // 2

                
                vis_canvas.create_image(x_position, y_position, anchor=NW, image=image_container.plot_image[-1])

                
                max_radius = min(dim_width, dim_height) / 2

                
                vertical_offset_percentage = 25  

                
                circle_radius_outer = max_radius * 0.83  
                circle_radius_inner = circle_radius_outer * 0.78  

                circle_vertical_offset = (dim_height - circle_radius_outer * 2) * vertical_offset_percentage / 100
                circle_horizontal_offset = (dim_width - circle_radius_outer * 2) / 2

                
                circle_center_x = circle_radius_outer + circle_horizontal_offset
                circle_center_y = circle_radius_outer + circle_vertical_offset

               
                vis_canvas.create_oval(circle_center_x - circle_radius_outer,circle_center_y - circle_radius_outer,circle_center_x + circle_radius_outer,circle_center_y + circle_radius_outer,outline="white", width=1)

                
                vis_canvas.create_oval(circle_center_x - circle_radius_inner,circle_center_y - circle_radius_inner,circle_center_x + circle_radius_inner,circle_center_y + circle_radius_inner,outline="white",width=1)


                # aggiorno l'altezza totale della finestra
                total_inner_height += vis_canvas.winfo_reqheight()

         
            #configurazione della scrollbar per il corretto posizionamento e funzionamento    
            canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))

# Creo la finestra principale
window = Tk()
window.title("MOTORBRAIN")
window.geometry("1280x960")


window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# creo i vari frames e li posiziono
frame_input = Frame(window, borderwidth=2, relief='solid')
frame_input.pack(side="top", fill=X, padx=2, pady=10, ipadx=20, ipady=10)

frame_visualization = Frame(window)
frame_visualization.pack(side="bottom", fill="both", expand=True, padx=0, pady=0)

frame_visualization.columnconfigure(0, weight=1)
frame_visualization.rowconfigure(0, weight=1)

#creo i widget utili per l'interazione all'interno dell'applicazione e li posiziono
file_label = Label(frame_input, text="Scegliere file csv...")
file_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

file_button = Button(frame_input, text="Browse...", command=open_file)
file_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

insert = Label(frame_input, text="Inserisci il numero di utenti (max "+get_num_voices(users)+"):")
insert.grid(row=0, column=1, columnspan=1, padx=120, pady=5, sticky="w")

entry_plots = Entry(frame_input)
entry_plots.grid(row=1, column=1, padx=120, pady=5, sticky="w")

insert_width=Label(frame_input, text="inserisci la grandezza dei plot:")
insert_width.grid(row=2, column=1, padx=120, pady=5, sticky="w")

entry_width=Entry(frame_input)
entry_width.grid(row=3, column=1, padx= 120, pady=5, sticky="w")

label_vis = Label(frame_input, text="Scegli il tipo di visualizzazione:")
label_vis.grid(row=0, column=2, pady=5, sticky="w")

vis_var = IntVar(value=1)

vis_choices = [("Small multiples", 1), ("Visualizzazioni singole", 2)]

for row, (text, value) in enumerate(vis_choices, start=2):
    vis_radio = Radiobutton(frame_input, text=text, variable=vis_var, value=value, command=on_radio_select)
    vis_radio.grid(row=row-1, column=2, sticky="w")

label_check=Label(frame_input, text="Solo mano dominante")
label_check.grid(row=1, column=3, padx=80, sticky="w")

insert_size=Label(frame_input, text="inserisci lo spessore dei plot:")
insert_size.grid(row=3, column=2, pady=5, sticky="w")

entry_size=Entry(frame_input)
entry_size.grid(row=4, column=2, pady=5, sticky="w")
entry_size.insert(0, "1") #valore di dafault dello spessore

check=IntVar()

checkbox1 = Checkbutton(frame_input, variable=check, command=on_checkbox_click)
checkbox1.grid(row=1, column=3, padx=220, sticky="w")

#label_check1=Label(frame_input, text="Immagine singola per utente")
#label_check1.grid(row=2, column=3, padx=80, sticky="w")

#check1=IntVar()

#checkbox2 = Checkbutton(frame_input, variable=check1, command=on_checkbox_click1)
#checkbox2.grid(row=2, column=3, padx=260, sticky="w")

#creo il bottone finale disabilitato inizialmente. Lo collego alla funzione display_plots per fare in modo che una volta cliccato mi mostri i grafici
go_button = Button(frame_input, text="Visualizza", command=display_plots, state=DISABLED)
go_button.grid(row=1, column=3, padx=360 ,sticky="w")

entry_plots.bind("<KeyRelease>", on_entry_key_release) #metodo per associare un evento alla funzione on_entry_release
entry_width.bind('<KeyRelease>', on_entry_number_release)


window.protocol("WM_DELETE_WINDOW", on_closing) #quando si chiude la finestra di visualizzazione vengono eliminate le immagini dalla cartella 

window.mainloop()


'''
#visualizzazioni singole per ogni utente solo con mano dominante in un unico canvas --- fare 3 cerchi 
    elif checkbox_state1 and checkbox_state and radio_value==2:
        
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):
            utenteConsiderato = dom_hand[dom_hand['userID'] == userID_to_select]
            traiettoria=pd.merge(utenteConsiderato, input, how="left", on=["sessionID", "repetitionID"])

            vis=ggplot()+geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria)+ facet_grid(".~repetitionID")+ coord_fixed()
            vis=vis+theme(axis_text_x=element_blank(),axis_text_y=element_blank(),axis_title_x=element_blank(),axis_title_y=element_blank(),axis_ticks=element_blank(),panel_background=element_blank(), strip_background_x=element_blank(),strip_text_x=element_blank(),legend_position='none') #strip_text_x e strip_background_x tolgono le label grige e il testo dentro
    

            vis.save(f'{dest_folder}plot_{i}.png', dpi=300)
            
            # carico l'immagine in un oggetto PhotoImage
            img = Image.open(f'{dest_folder}plot_{i}.png')
            resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS) 
            image_container.plot_image.append(ImageTk.PhotoImage(resized_image))
            
            #viene assegnato un canvas per ogni plot creato
            vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
            vis_canvas.grid(row=i // num_columns, column=i % num_columns, padx=0, pady=0)


            # visualizzo il plot nel canvas assegnato
            vis_canvas.create_image(0, 0, anchor=NW, image=image_container.plot_image[-1])


            # aggiorno l'altezza totale della finestra
            total_inner_height += vis_canvas.winfo_reqheight()

        canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))
    
    #small multiples per entrambe le mani in un unico canvas --- fare 3 cerchi
    elif checkbox_state1:
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):        
            utenteConsiderato_circle = prova_tutti_utenti[prova_tutti_utenti['userID'] == userID_to_select] 

            traiettoria_utente=pd.merge(utenteConsiderato_circle, input, how="left", on=["sessionID", "repetitionID"])

            vis=ggplot()+coord_fixed()+geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria_utente)+facet_grid(".~hand")
            vis=vis+theme(axis_text_x=element_blank(),axis_text_y=element_blank(),axis_title_x=element_blank(),axis_title_y=element_blank(),axis_ticks=element_blank(),panel_background=element_blank(),strip_background_x=element_blank(), strip_text_x=element_blank(), legend_position='none')

            vis.save(f'{dest_folder}plot_{i}.png', dpi=500)

            # carico l'immagine in un oggetto PhotoImage
            img = Image.open(f'{dest_folder}plot_{i}.png')
            resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS) 
            image_container.plot_image.append(ImageTk.PhotoImage(resized_image))
            
            #viene assegnato un canvas per ogni plot creato
            vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
            vis_canvas.grid(row=i // num_columns, column=i % num_columns, padx=0, pady=0)


            # visualizzo il plot nel canvas assegnato
            vis_canvas.create_image(0, 0, anchor=NW, image=image_container.plot_image[-1])

            circle_radius_outer = min(dim_width, dim_height) * 0.44 # Adjust the proportion as needed
            circle_radius_inner = circle_radius_outer * 0.75 # Adjust the proportion as needed

            # Center coordinates of the circles
            circle_center_x = dim_width / 2
            circle_center_y = dim_height / 2

            # Outer circle
            vis_canvas.create_oval(circle_center_x - circle_radius_outer,circle_center_y - circle_radius_outer,circle_center_x + circle_radius_outer,circle_center_y + circle_radius_outer,outline="black", width=1)

            # Inner circle
            vis_canvas.create_oval(circle_center_x - circle_radius_inner,circle_center_y - circle_radius_inner,circle_center_x + circle_radius_inner,circle_center_y + circle_radius_inner,outline="black",width=1)

            # aggiorno l'altezza totale della finestra
            total_inner_height += vis_canvas.winfo_reqheight()
        
        canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))

    #visualizzazioni singole per ogni ripetizione con entrambe le mani in un unico canvas --- fare 3 cerchi 
    elif checkbox_state1 and radio_value==2:
        for i, userID_to_select in enumerate(users['userID'].head(num_plots)):
            utenteConsiderato_circle = prova_tutti_utenti[prova_tutti_utenti['userID'] == userID_to_select]

            traiettoria_utente=pd.merge(utenteConsiderato_circle, input, how="left", on=["sessionID", "repetitionID"])

            vis=ggplot()+geom_point(aes(x='xR', y='yR', color='factor(repetitionID)'), traiettoria_utente)+ facet_grid("hand~repetitionID")+ coord_fixed()
            vis=vis+theme(axis_text_x=element_blank(),axis_text_y=element_blank(),axis_title_x=element_blank(),axis_title_y=element_blank(),axis_ticks=element_blank(),panel_background=element_blank(),strip_background_x=element_blank(),strip_text_x=element_blank(),strip_background_y=element_blank(),strip_text_y=element_blank() ,legend_position='none') #strip_background_y=element_blank(),strip_text_y=element_blank() per togliere anche le label e il testo dentro sull'asse y

           
            vis.save(f'{dest_folder}plot_{i}.png', dpi=500)

            # carico l'immagine in un oggetto PhotoImage
            img = Image.open(f'{dest_folder}plot_{i}.png')
            resized_image = img.resize((dim_width, math.floor(dim_height)), Image.LANCZOS) 
            image_container.plot_image.append(ImageTk.PhotoImage(resized_image))
            
            #viene assegnato un canvas per ogni plot creato
            vis_canvas = Canvas(plot_frame, width=dim_width, height=dim_height)
            vis_canvas.grid(row=i // num_columns, column=i % num_columns, padx=0, pady=0)


            # visualizzo il plot nel canvas assegnato
            vis_canvas.create_image(0, 0, anchor=NW, image=image_container.plot_image[-1])

            # aggiorno l'altezza totale della finestra
            total_inner_height += vis_canvas.winfo_reqheight()

        canvas.configure(scrollregion=(0, 0, dim_width * num_columns, total_inner_height))
'''
#le parti sotto commento fanno riferimento ai casi in cui si vuole visualizzare i plot di un utente in un'unica immagine ma non c'è il cerchio sotto