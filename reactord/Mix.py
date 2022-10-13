import numpy as np
from abc import ABCMeta, abstractmethod
from scipy.integrate import quad
from substance import Substance


class Abstract_Mix(metaclass = ABCMeta):
    """Mixture object abstract class.

        Parameters
        ----------
        substance_list : ndarray or list[Substance objects]
            list or array of Substance objects."""

    @abstractmethod
    def __init__(self):
        pass        

    @abstractmethod
    def concentrations(self):
        """Concentrations of the mixtures substances at the given moles 
        of each compound, temperature and pressure.
        
        Parameters:
        moles: ndarray or list [float]
            moles of each substance
        temperature: float
            Temperature [K]
        pressure: float
           Total Pressure [Pa]
                
        Returns
        -------
        ndarray [float]
            ndarray that contains the concentrations of the mixture's 
            substances [mol/m^3]
        """
        pass

    @abstractmethod
    def volume(self):
        """Method that returns the volume of the mixture.

        Parameters
        ----------
        moles: ndarray or list [float]
            moles of each substance
        temperature: float
            Temperature [K]
        pressure: float
           Total Pressure [Pa]

        Returns
        -------
        float
            volume of the mixture [m^3]
        """
        pass

    @abstractmethod
    def mix_heat_capacity(self):
        """Method that returns the heat capacity of the mixture.

        Parameters
        ----------
        moles: ndarray or list [float]
            moles of each substance
        temperature: float
            Temperature [K]
        pressure: float
           Total Pressure [Pa]

        Returns
        -------
        float
            heat capacity of the mixture [j/mol/K)] 
        """      
        pass
    
    @abstractmethod
    def pure_heat_capacities_integral(self):
        pass

# Other methods (Inhereted but not implemented in subclasses)
    def mol_fracations(self, moles):
        """method that calculates the molar fractions of the mixture

        Parameters
        ----------
        moles: ndarray or list [float]
            moles of each substance

        Returns
        -------
        ndarray
            array that contains the molar fractions of mixture's 
            substances
        """
        total_moles = np.sum(moles, axis=0)
        zi = np.divide(moles, total_moles)
        return zi

    def partial_pressures(self, moles, temperature, pressure):
        """method that calculates the partial pressures of the mixture

        Parameters
        ----------
        moles: ndarray or list [float]
            moles of each substance
        temperature: float
            Temperature [K]
        pressure: float
           Total Pressure [Pa]

        Returns
        -------
        ndarray
            array that contains the partial pressures of mixture's 
            substances
        """
        zi = self.mol_fracations(moles)
        partial_pressures= np.multiply(zi, pressure)
        return partial_pressures

    def partial_P_2_conc (self, partial_pressures, temperature):
        R= 8.31446261815324 # J/mol.K
        self.partial_pressures= np.array(partial_pressures)
        conc= self.partial_pressures /(R*temperature) # mol/m^3
        return conc

    def __len__(self):
        return len(self.substances)
    
    def __str__ (self):
        string=(f"The mixture contains the following" 
                f" {len(self.substances)} components:\n")
        for i,substance in enumerate (self.substances):
            string = string + substance.name.capitalize() + "\n"     
        return string

class Liquid_Mix(Abstract_Mix):

    def __init__(self, substance_list):
        self.substances = substance_list
        self.formation_enthalpies = [
                substance.formation_enthalpy for substance in self.substances
            ]
        
    def concentrations(self, moles, temperature, pressure):
        zi = self.mol_fracations(moles)      
        molar_volumes = np.array(
        [substance.volume_liquid(temperature, pressure) 
        for substance in self.substances]
        )                        

        total_molar_vol = np.dot(zi,molar_volumes)
        concentrations = np.divide(zi, total_molar_vol) #moles/m^3     
        return concentrations

    def volume(self, moles, temperature, pressure):  
        pure_volumes = np.array(
            [substance.volume_liquid(temperature, pressure) 
            for substance in self.substances]
        )
        return np.dot(pure_volumes, moles)        

    def mix_heat_capacity(self, moles, temperature, pressure):
        zi = self.mol_fracations(moles)
        pure_cp = np.array(
            [substance.heat_capacity_liquid(temperature) 
            for substance in self.substances]
        )
        mix_cp = np.dot(zi, pure_cp)
        return mix_cp
    
    def pure_heat_capacities_integral(
        self, 
        temperature: float, 
        *args
    ) -> list[float]:
        """Correction of the standard enthalpies of formation from 298.15 K and
       to 'temperature'. The pure substances heat_capacity_liquid are used.

        Parameters
        ----------
        temperature : float
            Temperature of correction [K].

        Returns
        -------
        ndarray
            Corrected enthalpy of formation of each pure substance in the 
            mixture [J/mol]. 
        """
        
        ref_temperature = 298.15
        correction_enthalpies = np.array([])

        for substance in self.substances:
            cp_dt_integral = self.mix.heat_capacity_liquid_dt_integral(
                ref_temperature, temperature
            )
            correction_enthalpies = np.append(
                (correction_enthalpies, 
                
                )
            )
        
        return correction_enthalpies

class IdealGas_Mix(Abstract_Mix):

    def __init__(self, substance_list : list[Substance]):
        self.substances = substance_list
        self.formation_enthalpies = [
                substance.formation_enthalpy_ig for substance in self.substances
            ]

    def concentrations(self, moles, temperature, pressure):
        zi = self.mol_fracations(moles)      
        
        molar_volumes = np.array(
            [substance.volume_gas(temperature, pressure) 
            for substance in self.substances]
        )

        total_molar_vol = np.dot(zi,molar_volumes)
        concentrations = np.divide(zi, total_molar_vol) #moles/m^3     
        return concentrations

    def volume(self, moles, temperature, pressure):
        pure_volumes = np.array(
            [substance.volume_gas(temperature, pressure) 
            for substance in self.substances]
        )
        return np.dot(pure_volumes, moles) 

    def mix_heat_capacity(self, moles, temperature, pressure):
        zi = self.mol_fracations(moles)
        pure_cp = np.array([
                            substance.heat_capacity_gas(temperature) 
                            for substance in self.substances]
        )
        mix_cp = np.dot(zi, pure_cp)
        return mix_cp

    def pure_heat_capacities_integral(self, temperature:float, *args):
        """Correction of the standard enthalpies of formation from 298.15 K and
        1 bar to 'temperature'.The pure substances heat_capacity_gas are used.

        Parameters
        ----------
        temperature : float
            Temperature of correction [K].

        Returns
        -------
        ndarray
            Corrected enthalpy of formation of each pure substance in the 
            mixture [J/mol].  
        """
        
        ref_temperature = 298.15
        correction_enthalpies = np.array([])

        for substance in self.substances:
            integral, err = quad(
                substance.heat_capacity_gas, ref_temperature, temperature
            )
            correction_enthalpies = np.append(
                (correction_enthalpies, integral)
            )
        
        return correction_enthalpies + self.formation_enthalpies