'''
Created on 12 Dec 2017
This module contains the class IsaAtmosphere which computes the atmospheric 
values at a iven altitude. 
@author: ng6a38a
'''
import numpy as np

class IsaAtmosphere:
    
    def __init__(self, altitude):
        '''
        The class IsaAtmosphere computes the values of pressure, temperature, 
        density, speed of sound at a given altitude in meters.
        '''
        self.altitude = altitude         #[m]
        self.R = 287                     #[J/kg K]
        self.gamma = 4/3
        self.g = 9.81                    #[m/s2]
        self.TEMPERATURE_sl = 288.15     #[K]
        self.PRESSURE_sl = 101325        #[Pa]
        self.DENSITY_sl = 1.225          #[kg/m3]
        self.a = -0.0065                 #[K/m]
        
        if self.altitude > 11000:
            print('Out of Troposphere')
            
    def sea_level_values(self):
        """
        Gives back the value at sea level.
        """
        return self.TEMPERATURE_sl, self.PRESSURE_sl, self.DENSITY_sl
        
    def compute_temperature(self):
        """
        Compute the temperature in the troposphere.
        """
        temperature = self.TEMPERATURE_sl + self.a * self.altitude
        #print(temperature)
        return temperature
    
    def compute_pressure(self):
        """
        Compute the pressure in the troposphere.
        """        
        pressure = self.PRESSURE_sl * (self.compute_temperature() / \
                   self.TEMPERATURE_sl)**(-self.g / (self.R * self.a))
        return pressure
     
    def compute_density(self):
        """
        Compute the density in the troposphere.
        """        
        density = self.compute_pressure() / (self.R * self.compute_temperature())
        return density
    
    def compute_sound_speed(self):
        sound_speed = np.sqrt(self.gamma * self.R * self.compute_temperature())
        return sound_speed
        
             
        