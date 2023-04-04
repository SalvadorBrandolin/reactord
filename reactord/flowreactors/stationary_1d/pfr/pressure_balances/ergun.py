import numpy as np

from IPython.display import display

from sympy import symbols

from reactord.flowreactors.stationary_1d.pfr.pfr import PFR


class Ergun:
    def __init__(
        self, pressure: dict, porosity: float, particle_diameter: float
    ) -> None:
        self._inlet_pressure = pressure.get("in")
        self._outlet_pressure = pressure.get("out")
        self.porosity = porosity
        self.particle_diameter = particle_diameter

        if self._inlet_pressure and self._outlet_pressure:
            raise ValueError(
                "Pressure balance error: Only inlet or outlet border condition"
                " specification allowed for the pressure."
            )

    @property
    def irepr(self):
        display(symbols(self.__repr__()))

    def initial_profile(self, reactor: PFR):
        if self._inlet_pressure:
            return np.full(reactor.grid_size, self._inlet_pressure)
        else:
            return np.full(reactor.grid_size, self._outlet_pressure)

    def update_profile(self, reactor: PFR, variables):
        reactor.pressure_profile = variables[-1, :]

    def border_conditions(self, reactor: PFR):
        if self._inlet_pressure:
            return self._inlet_pressure, None
        else:
            return None, self._outlet_pressure

    def evaluate_balance(self, reactor: PFR):
        phi = self.porosity
        dp = self.particle_diameter

        m_rho = reactor.mix.mass_density(
            reactor.mole_fraction_profile,
            reactor.temperature_profile,
            reactor.pressure_profile,
        )
        mu = reactor.mix.mix_viscosity(
            reactor.mole_fraction_profile,
            reactor.temperature_profile,
            reactor.pressure_profile,
        )
        u = (
            np.sum(reactor.mass_profile[:, 0])
            * reactor.mix.mix_molecular_weight(
                reactor.mole_fraction_profile[:, 0]
            )
            / m_rho[0]
            / 1000
            / reactor.transversal_area
        )

        pressure_gradient = (
            -u
            / dp
            * (1 - phi)
            / phi**3
            * (150 * (1 - phi) * mu / dp + 1.75 * u * m_rho)
        )
        return pressure_gradient

    def __repr__(self):
        latex = (
            r"\frac{dP}{dz}=-\frac{G}{{\rho}D_p}\left(\frac{1-\phi}{\phi^3}"
            r"\right)\left[\frac{150(1-\phi)\mu}{D_p}+1.75G\right]"
        )
        return latex
