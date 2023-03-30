import numpy as np

from reactord.kinetics import Kinetics
from reactord.mix.abstract_mix import AbstractMix

from scipy.integrate import solve_bvp

import pandas as pd


class PFR:
    def __init__(
        self,
        mix: AbstractMix,
        kinetics: Kinetics,
        reactor_length: float,
        transversal_area: float,
        grid_size: int,
        mass_balance,
        energy_balance,
        pressure_balance,
    ) -> None:
        # =====================================================================
        # Core PFR information
        # =====================================================================
        self.mix = mix
        self.kinetics = kinetics
        self.reactor_length = reactor_length
        self.transversal_area = transversal_area
        self._initial_grid_size = grid_size
        self.grid_size = grid_size

        # =====================================================================
        # Balances
        # =====================================================================
        self.mass_balance = mass_balance
        self.energy_balance = energy_balance
        self.pressure_balance = pressure_balance

        # =====================================================================
        # Variables grids and profiles
        # =====================================================================
        self.z = np.array([])
        self.mass_profile = np.array([])
        self.mole_fraction_profile = np.array([])
        self.temperature_profile = np.array([])
        self.refrigerant_temperature_profile = np.array([])
        self.pressure_profile = np.array([])
        self.r_rates_profile = np.array([])

    def initial_profile_builder(self):
        self.z = np.linspace(0, self.reactor_length, self.grid_size)
        self.mass_profile = self.mass_balance.initial_profile(self)
        (
            self.temperature_profile,
            self.refrigerant_temperature_profile,
        ) = self.energy_balance.initial_profile(self)
        self.pressure_profile = self.pressure_balance.initial_profile(self)

        self.initial_variables_profile = np.vstack(
            (
                self.mass_profile,
                self.temperature_profile,
                self.refrigerant_temperature_profile,
                self.pressure_profile,
            )
        )
    
    def border_conditions_builder(self):
        self.mass_bc = self.mass_balance.border_conditions(self)
        self.temperature_bc = self.energy_balance.border_conditions(self)
        self.pressure_bc = self.pressure_balance.border_conditions(self)

        self.inlet_conditions = np.append(
            self.mass_bc[0], self.temperature_bc[0]
        )
        self.inlet_conditions = np.append(
            self.inlet_conditions, self.pressure_bc[0]
        )

        self.outlet_conditions = np.append(
            self.mass_bc[1], self.temperature_bc[1]
        )
        self.outlet_conditions = np.append(
            self.outlet_conditions, self.pressure_bc[1]
        )

        self._in_index = np.argwhere(
            np.not_equal(self.inlet_conditions, None)
        ).ravel()
        self._out_index = np.argwhere(
            np.not_equal(self.outlet_conditions, None)
        ).ravel()

    def border_conditions(self, ya, yb):
        bc = np.array([])

        for idx in self._in_index:
            bc = np.append(bc, ya[idx] - self.inlet_conditions[idx])

        for idx in self._out_index:
            bc = np.append(bc, yb[idx] - self.outlet_conditions[idx])

        return bc

    def evaluate_balances(self, z, variables):
        n = len(self.mix)
        self.z = z
        self.grid_size = len(z)
        self.mass_profile = variables[0:n, :]
        self.temperature_profile = variables[-3, :]
        self.refrigerant_temperature_profile = variables[-2, :]
        self.pressure_profile = variables[-1, :]

        self.mole_fraction_profile = self.mix.mole_fractions(
            self.mass_profile
        )

        self.r_rates_profile = self.kinetics.kinetic_eval(
            self.mole_fraction_profile,
            self.temperature_profile,
            self.pressure_profile,
        )

        mass_gradient = self.mass_balance.evaluate_balance(self)
        temperature_gradient = self.energy_balance.evaluate_balance(self)
        pressure_gradient = self.pressure_balance.evaluate_balance(self)

        gradients = np.vstack(
            (mass_gradient, temperature_gradient, pressure_gradient)
        )

        return gradients

    def simulate(self, tol=1e-3, max_nodes=1000, verbose=0, bc_tol=None):
        self.grid_size = self._initial_grid_size
        self.initial_profile_builder()
        self.border_conditions_builder()
        
        self.simulation = solve_bvp(
            fun=self.evaluate_balances,
            bc=self.border_conditions,
            x=self.z,
            y=self.initial_variables_profile,
            tol=tol,
            max_nodes=max_nodes,
            verbose=verbose,
            bc_tol=bc_tol,
        )
        
        result = np.vstack((self.simulation.x, self.simulation.y))
        z = np.array(["z"])
        names = self.mix.names
        last = np.array(["temperature", "refrigerant_temperature", "pressure"])
        
        columns = np.append(z, names)
        columns = np.append(columns, last)
        
        self._sim_df = pd.DataFrame(
            result.T,
            columns=columns,
            index=None
        )

    @property
    def sim_df(self):
        return self._sim_df
    
    @property
    def irepr(self):
        print("Mass balance:")
        self.mass_balance.irepr
        print("Reactor and refrigerant energy balances:")
        self.energy_balance.irepr
        print("Pressure balance:")
        self.pressure_balance.irepr

    def __repr__(self):
        latex = (
            f"{self.mass_balance.__repr__()}\n"
            f"{self.energy_balance.__repr__()[0]}\n"
            f"{self.energy_balance.__repr__()[1]}\n"
            f"{self.pressure_balance.__repr__()}\n"
        )
        return latex