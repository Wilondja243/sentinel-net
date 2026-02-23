
import customtkinter as ctk

class Button(ctk.CTkButton):
    def __init__(
        self,
        master,
        text,
        border="#282C2E",
    **kwargs):
        
        super().__init__(
            master=master, 
            text=text,
            corner_radius=50,
            border_width=1,
            border_color=border,
            **kwargs
        )
