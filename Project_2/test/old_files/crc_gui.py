import customtkinter as ctk
import calculations as clc

# GOOD LUCK :)
class Application():
    def __init__(self, master):
        self.padding = {'pady': 5, 'padx': 5}
        
        self.widgets = {}
        
        # # # FRAMES # # #
        self.enc_in_frame = ctk.CTkFrame(master=master)
        self.enc_in_frame.grid(**self.padding, column=0, row=0,  sticky='nsew')

        self.dec_in_frame = ctk.CTkFrame(master=master)
        self.dec_in_frame.grid(**self.padding, column=0, row=1,  sticky='nsew')

        self.enc_out_frame = ctk.CTkFrame(master=master)
        self.enc_out_frame.grid(**self.padding, column=1, row=0, sticky='nsew')

        self.dec_out_frame = ctk.CTkFrame(master=master)
        self.dec_out_frame.grid(**self.padding, column=1, row=1, sticky='nsew')

        # # # ENCODER INPUT FRAME # # #
        self.enc_frame_title = ctk.CTkLabel(master=self.enc_in_frame, text="Encoder", font=ctk.CTkFont(size=20, weight='bold'))
        self.enc_frame_title.pack(**self.padding, anchor="n")

        self.mess_in_label = ctk.CTkLabel(master=self.enc_in_frame, text="Message")
        self.mess_in_label.pack(**self.padding, anchor="center")

        self.enc_mess_entry = ctk.CTkEntry(master=self.enc_in_frame, placeholder_text="Input binary message", width=300)
        self.enc_mess_entry.pack(**self.padding, anchor="center")

        self.nk_in_label = ctk.CTkLabel(master=self.enc_in_frame, text="Code (n,k)")
        self.nk_in_label.pack(**self.padding, anchor="center")

        self.nk_entry = ctk.CTkEntry(master=self.enc_in_frame, placeholder_text="Input n,k code", width=300)
        self.nk_entry.pack(**self.padding, anchor="center")
        
        self.enc_button = ctk.CTkButton(master=self.enc_in_frame, text="ENCODE", font=ctk.CTkFont(weight="bold"), command=self.create_enc_out)
        self.enc_button.pack(**self.padding)

        # # # DECODER INPUT FRAME # # #
        self.dec_frame_title = ctk.CTkLabel(master=self.dec_in_frame, text="Decoder", font=ctk.CTkFont(size=20, weight='bold'))
        self.dec_frame_title.pack(**self.padding, anchor="n")

        self.mess_rec_label = ctk.CTkLabel(master=self.dec_in_frame, text="Message recieved")
        self.mess_rec_label.pack(**self.padding, anchor="center")

        self.dec_mess_entry = ctk.CTkEntry(master=self.dec_in_frame, placeholder_text="Input recieved binary message", width=300)
        self.dec_mess_entry.pack(**self.padding, anchor="center")

        self.poly_in_label = ctk.CTkLabel(master=self.dec_in_frame, text="Input generating polynomial")
        self.poly_in_label.pack(**self.padding, anchor="center")

        self.poly_entry = ctk.CTkEntry(master=self.dec_in_frame, placeholder_text="Input generating polynomial", width=300)
        self.poly_entry.pack(**self.padding, anchor="center")
        
        self.dec_button = ctk.CTkButton(master=self.dec_in_frame, text="DECODE", font=ctk.CTkFont(weight="bold"), command=self.do_dec_math)
        self.dec_button.pack(**self.padding)

        # # # ENCODER OUTPUT # # #
        self.enc_out_title = ctk.CTkLabel(master=self.enc_out_frame, text="Encoder Output", font=ctk.CTkFont(size=20, weight='bold'))
        self.enc_out_title.pack(**self.padding)

        # # # DECODER OUTPUT # # #
        self.dec_out_title = ctk.CTkLabel(master=self.dec_out_frame, text="Decoder Output", font=ctk.CTkFont(size=20, weight='bold'))
        self.dec_out_title.pack(**self.padding)
    
    def create_enc_out(self):
        if 'enc' in self.widgets:
            self.delete_enc_out()
        
        if self.hamming_check():
            Error_popup('Not a Hamming code!')
        
        data_in = clc.main_encode(self.enc_mess_entry.get(), self.nk_entry.get())
        
        enc_out_table = Encoder_output(master=self.enc_out_frame, daddy=self, data_in=data_in)
        self.widgets["enc"] = enc_out_table
        
    def delete_enc_out(self):
        self.widgets["enc"].destroy()
        self.widgets.pop("enc")
        
    def create_dec_out(self, data_in):
        if 'dec' in self.widgets:
            self.delete_dec_out()
            
        dec_out_table = Decoder_output(master=self.dec_out_frame, data_in=data_in)
        self.widgets["dec"] = dec_out_table
        
    def delete_dec_out(self):
        self.widgets["dec"].destroy()
        self.widgets.pop("dec")
        
    def do_dec_math(self):
        mess = self.dec_mess_entry.get()
        poly = self.poly_entry.get()
        
        data_in = [mess, poly]
        self.create_dec_out(data_in)
        
    def set_dec_data(self, mess, poly):
        self.dec_mess_entry.delete(0,len(self.dec_mess_entry.get()))
        self.dec_mess_entry.insert(0, mess)
        self.poly_entry.delete(0,len(self.poly_entry.get()))
        self.poly_entry.insert(0, poly)
        
    def hamming_check(self):
        code = self.nk_entry.get()
        code = code.split(',')
        n = int(code[0])
        k = int(code[1])
        r = n - k
        
        n_test = (2**r) - 1
        k_test = (2**r) - 1 - r
        
        if n != n_test and k != k_test:
            Error_popup('Not a Hamming code!')
            self.destroy()
            return True
        
        return False
                
class Encoder_output():
    def __init__(self, master, daddy, data_in):
        self.data = data_in
        self.daddy = daddy
        #self.lines = []
        
        self.radio_var = ctk.IntVar()
        
        self.main_frame = ctk.CTkFrame(master=master)
        self.main_frame.pack(pady=10, padx=10, fill='x', expand=True)
        
        self.main_frame.columnconfigure(index=0, weight=10)
        self.main_frame.columnconfigure(index=1, weight=10)
        self.main_frame.columnconfigure(index=2, weight=1)
        
        self.main_frame.rowconfigure(index=0, weight=1)
        
        self.gen_pol_title = ctk.CTkLabel(master=self.main_frame, text='Gen. polynomial', font=ctk.CTkFont(weight='bold'))
        self.gen_pol_title.grid(column=0, row=0, sticky="w")
        
        self.enc_mess_title = ctk.CTkLabel(master=self.main_frame, text='Encoded message', font=ctk.CTkFont(weight='bold'))
        self.enc_mess_title.grid(column=1, row=0, sticky="w")
        
        self.button_title = ctk.CTkLabel(master=self.main_frame, text='Use', font=ctk.CTkFont(weight='bold'))
        self.button_title.grid(column=2, row=0, sticky='w')
        
        self.create_lines()
        
        self.export = ctk.CTkButton(master=self.main_frame, text="Use in decoder", command=lambda: daddy.set_dec_data(mess=self.data[self.radio_var.get()][0], poly=self.data[self.radio_var.get()][1]))
        self.export.grid(column=0, row=len(self.data)+1, columnspan=3, sticky='nsew')
        
    
    def create_lines(self):
        for i in range(len(self.data)):
            #temp_lines = []
            
            self.main_frame.rowconfigure(index=i+1, weight=1)
            
            temp_poly = ctk.CTkLabel(master=self.main_frame, text=f"{self.data[i][1]}")
            temp_poly.grid(column=0, row=i+1, sticky="w")
            #temp_lines.append(temp_poly)
            
            temp_mess = ctk.CTkLabel(master=self.main_frame, text=f"{self.data[i][0]}")
            temp_mess.grid(column=1, row=i+1, sticky='w')
            #temp_lines.append(temp_mess)
            
            temp_radio = ctk.CTkRadioButton(master=self.main_frame, text='', variable=self.radio_var, value=i)
            temp_radio.grid(column=2, row=i+1)
            #temp_lines.append(temp_lines)
            
            #self.lines.append(temp_lines)
    
    def destroy(self):
        self.main_frame.destroy()
        
class Decoder_output():
    def __init__(self, master, data_in):
        self.data = data_in
        
        # self.widgets = []
        
        self.title_padding = {"padx":5, "pady":0}
        self.text_padding = {"padx":20, "pady":0}
        
        self.main_frame = ctk.CTkFrame(master=master)
        self.main_frame.pack(pady=10, padx=10, fill='x', expand=True)
        
        self.input_check()
        
    def clear_offsprings(self):
        for child in self.main_frame.winfo_children():
            child.destroy()
         
    def destroy(self):
        self.main_frame.destroy()
        
    def error_out(self, err_pos):
        self.dec_mess_title = ctk.CTkLabel(master=self.main_frame, text='Recieved message:' ,font=ctk.CTkFont(weight='bold'))
        self.dec_mess_title.pack(**self.title_padding, anchor="w")
        
        self.dec_mess = ctk.CTkLabel(master=self.main_frame, text=f'{self.data[0]}')
        self.dec_mess.pack(**self.text_padding, anchor="w")
        
        self.dec_mess_title = ctk.CTkLabel(master=self.main_frame, text='Recieved message as a polynomial:' ,font=ctk.CTkFont(weight='bold'))
        self.dec_mess_title.pack(**self.title_padding, anchor="w")
        
        self.dec_mess = ctk.CTkLabel(master=self.main_frame, text=f'{clc.format_message_to_x(self.data[0])}')
        self.dec_mess.pack(**self.text_padding, anchor="w")
        
        self.syndrome_title = ctk.CTkLabel(master=self.main_frame, text='Error detection:' ,font=ctk.CTkFont(weight='bold'))
        self.syndrome_title.pack(**self.title_padding, anchor="w")
        
        self.syndrome_text = ctk.CTkLabel(master=self.main_frame, text=f'Error detected on position x^{err_pos}!')
        self.syndrome_text.pack(**self.text_padding, anchor="w")
        
        # self.error_location_title = ctk.CTkLabel(master=self.main_frame, text='Error location:' ,font=ctk.CTkFont(weight='bold'))
        # self.error_location_title.pack(**self.title_padding, anchor="w")
        
        # self.error_location = ctk.CTkLabel(master=self.main_frame, text='Erorr location here')
        # self.error_location.pack(**self.text_padding, anchor="w")
        
        self.repaired_mess_title = ctk.CTkLabel(master=self.main_frame, text='Repaired message:' ,font=ctk.CTkFont(weight='bold'))
        self.repaired_mess_title.pack(**self.title_padding, anchor="w")
        
        self.repaired_mess = ctk.CTkLabel(master=self.main_frame, text=f'{clc.repair_message(self.data[0], err_pos)}')
        self.repaired_mess.pack(**self.text_padding, anchor="w")
        
        self.dec_mess_title = ctk.CTkLabel(master=self.main_frame, text='Repaired message as a polynomial:' ,font=ctk.CTkFont(weight='bold'))
        self.dec_mess_title.pack(**self.title_padding, anchor="w")
        
        self.dec_mess = ctk.CTkLabel(master=self.main_frame, text=f'{clc.format_message_to_x(clc.repair_message(self.data[0], err_pos))}')
        self.dec_mess.pack(**self.text_padding, anchor="w")
        
    def no_issues_out(self):
        self.dec_mess_title = ctk.CTkLabel(master=self.main_frame, text='Recieved message:' ,font=ctk.CTkFont(weight='bold'))
        self.dec_mess_title.pack(**self.title_padding, anchor="w")
        
        self.dec_mess = ctk.CTkLabel(master=self.main_frame, text=f'{self.data[0]}')
        self.dec_mess.pack(**self.text_padding, anchor="w")
        
        self.dec_mess_title = ctk.CTkLabel(master=self.main_frame, text='Recieved message as a polynomial:' ,font=ctk.CTkFont(weight='bold'))
        self.dec_mess_title.pack(**self.title_padding, anchor="w")
        
        self.dec_mess = ctk.CTkLabel(master=self.main_frame, text=f'{clc.format_message_to_x(self.data[0])}')
        self.dec_mess.pack(**self.text_padding, anchor="w")
        
        self.syndrome_title = ctk.CTkLabel(master=self.main_frame, text='Errors:' ,font=ctk.CTkFont(weight='bold'))
        self.syndrome_title.pack(**self.title_padding, anchor="w")
        
        self.syndrome_text = ctk.CTkLabel(master=self.main_frame, text='No errors')
        self.syndrome_text.pack(**self.text_padding, anchor="w")
    
    def input_check(self):
        
        if self.data == ['','']:
            self.main_frame.destroy()
            Error_popup("Empty input!")
        
        check = clc.crc_check(self.data[0], self.data[1])
        
        if check == None:
            self.create_no_problem()
        else:
            self.create_problem(check)

        
        
    
    def create_no_problem(self):
        self.clear_offsprings()
        
        self.no_issues_out()
        
    def create_problem(self, err_pos):
        self.clear_offsprings()
        
        self.error_out(err_pos)

class Error_popup():
    def __init__(self, error_text):
        self.error_text = error_text
        self.root = self.set_root()
        
        self.err_label = ctk.CTkLabel(master=self.root, text=self.error_text, font=ctk.CTkFont(weight='bold', size=16))
        self.err_label.pack()
        
        self.ok_button = ctk.CTkButton(master=self.root, text="OK", command=lambda: self.root.destroy())
        self.ok_button.pack()
        
        self.root.mainloop()
        
        
    def set_root(self):
        root = ctk.CTk()
        # root.geometry("1200x530")
        size = {'width': 200, 'height': 75}
        root.minsize(**size)
        root.maxsize(**size)
        root.resizable(0,0)
        
        root.columnconfigure(index=0, weight=1)
        root.columnconfigure(index=1, weight=5)
        root.rowconfigure(index=0, weight=1)
        root.rowconfigure(index=1, weight=1)
        
        return root
        

def set_root():
    root = ctk.CTk()
    root.geometry("1200x625")
    root.minsize(width=300, height=625)
    
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=5)
    root.rowconfigure(index=0, weight=1)
    root.rowconfigure(index=1, weight=1)
    
    return root

def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("dark-blue")

    root = set_root()
        
    app=Application(root)
    
    root.mainloop()
 
# if __name__ == "__main__":
#     main()