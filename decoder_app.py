from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture

import matplotlib.pyplot as plt



import torch
import random
from torch import nn
import numpy as np


class ConvAutoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=10, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),
            nn.Conv2d(in_channels=10, out_channels=5, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),
            nn.Conv2d(in_channels=5, out_channels=5, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),
            nn.Flatten(1)
        )

        self.decoder = nn.Sequential(
            nn.Unflatten(1, (5, 3, 3)),
            nn.UpsamplingBilinear2d(None, (3, 3)),
            nn.ConvTranspose2d(in_channels=5, out_channels=5, kernel_size=3),
            nn.ReLU(),
            nn.UpsamplingBilinear2d(None, (3, 3)),
            nn.ConvTranspose2d(in_channels=5, out_channels=10, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.UpsamplingBilinear2d(None, (3, 3)),
            nn.ConvTranspose2d(in_channels=10, out_channels=1, kernel_size=3, padding=1),
        )
    
    def forward(self, x):
        return self.decoder(self.encoder(x))





class Decoder(App):
    def on_value_change(self, instance, value):
        self.values[instance.ids["name"]] = value
        self.update()

    def update(self):
        values = torch.tensor(self.values, dtype=torch.float32).view(1, 45)
        img = np.uint8((nn.Sigmoid()(self.auto.decoder(values).squeeze()) * 255).detach().numpy())
        
        c_img = np.uint8((plt.get_cmap("ocean_r")(img)) * 255)[:, :, :3]
        
        
        self.texture.blit_buffer(c_img.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = self.texture

        

        
        
    
    def build(self):
        

        MAX = 1000
        MIN = -1000
        
        root = BoxLayout(orientation="horizontal")
        control = BoxLayout(orientation="vertical")
        slider_count = 45
        self.image = Image(size_hint=(1, 1), allow_stretch=True, keep_ratio=False)

        self.auto = ConvAutoencoder()
        self.auto.load_state_dict(torch.load("model/autoencoder_2140", weights_only=False))


        sliders = [ Slider(min=MIN, max=MAX, value=random.randint(MIN, MAX)) for _ in range(slider_count) ]
        self.values = [ 0 ] * 45
        for i, s in enumerate(sliders):
            control.add_widget(s)
            s.bind(value=self.on_value_change)
            self.values[i] = s.value
            s.ids["name"] = i
        
        self.texture = Texture.create(size=(99, 99), colorfmt="rgb")
        self.update()
        
        
        self.image.texture = self.texture

        
        
        root.add_widget(control)
        root.add_widget(self.image)
        return root

Decoder().run()
