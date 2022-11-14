from abc import ABCMeta, abstractmethod

from _collections_abc import Callable

from reactord import Kinetics
from reactord.mix import AbstractMix


class ReactorBase(metaclass=ABCMeta):
    """Abstract class interface for each reactor in ReactorD."""

    # ==================================================================
    # Common parameters for all reactors.
    # ==================================================================

    _kinetics: Kinetics = None
    _mix: AbstractMix = None
    _list_of_reactions: list[Callable] = []
    _stoichiometry: list = []
    _kinetic_argument: str = ""

    @property
    def kinetics(self):
        """Kinetics class instantiation

        Returns
        -------
        Kinetics
            Kinetics class instantiation.
        """
        return self._kinetics

    @kinetics.setter
    def kinetics(self, new_kinetics):
        """Method to asign a new instantiation of the reactor kinetics.
        Validates that the asigned object is acctualy a Kinetics
        instantiation.

        Parameters
        ----------
        new_kinetics : Kinetics
            Kinetics class instantiation.

        Raises
        ------
        ValueError
            The assigned value is not a Kinetics instantiation object.
        """
        if isinstance(new_kinetics, Kinetics):
            self._kinetics = new_kinetics
        else:
            raise ValueError(
                "The assigned value to the reactor's kinetics "
                " attribute must be a Kinetics instance object."
            )

    @property
    def mix(self):
        """Mixture object that is stored only on the Kinetics object to 
        prevent multiple mixture objects on the same reactor.

        Returns
        -------
        AbstractMix
            Mixture object.
        """
        return self._kinetics.mix

    @mix.setter
    def mix(self, new_mix):
        """Method to assign a new mixture object to the reactor. The 
        method replaces the mixture inside the kinetic object.

        Parameters
        ----------
        new_mix : AbastractMix
            Mixture object.
        """
        self._kinetics.mix = new_mix

    @property
    def list_of_reactions(self):
        """List that contains the functions to eval each reaction.

        Explain more: # TODO

        Returns
        -------
        _type_
            _description_
        """
        return self._kinetics.list_of_reactions

    @list_of_reactions.setter
    def list_of_reactions(self, new_list_of_reactions):
        self._kinetics.list_of_reactions = new_list_of_reactions

    @property
    def stoichiometry(self):
        return self._kinetics.stoichiometry

    @stoichiometry.setter
    def stoichiometry(self, new_stoichiometry):
        self._kinetics.stoichiometry = new_stoichiometry

    @property
    def kinetic_argument(self):
        return self._kinetics.stoichiometry

    @kinetic_argument.setter
    def kinetic_argument(self, new_kinetics_argument):
        self._kinetics.kinetic_argument = new_kinetics_argument

    # ==================================================================
    # Abastract methods
    # Settings for mass, energy and pressure balance.
    # ==================================================================

    @abstractmethod
    def set_mass_balance_data(self):
        """Method that recieves and instantiates the neccesary
        parameters to solve the mass balance in the reactor's bulk
        phase as attributes of the reactor. The method returns None.

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def set_energy_balance_data(self):
        """Method that recieves and instantiates the neccesary
        parameters to solve the energy balance in the reactor's bulk
        phase as attributes of the reactor. The method returns None.

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def set_pressure_balance_data(self):
        """Method that recieves and instantiates the neccesary
        parameters to solve the pressure balance in the reactor's bulk
        phase as attributes of the reactor. The method returns None.

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    # ==================================================================
    # Solvers aditional data needed - general used methods
    # ==================================================================

    @abstractmethod
    def _grid_builder(self) -> None:
        """Method to build the grid of independent variables.
        Recieves lower and upper boundaries for each independent
        variable and also the number of discretization intervals
        for each defined range.

        Example:

        A discontinuous tank reactor solved from time 0 s to 3600 s,
        using 10 second as time step, should recieve something like:

        time_span = [0, 3600]
        time_step = 10

        The return of the method should seems like:

        return numpy.linspace(time_span[0], time_span[1], time_step)

        More explanation needed: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def _border_condition_builder(self) -> None:
        """Constructs the border conditions for the differential
        equations that represents the bulk phase behaviour. The format
        of the method's output correponds with the reactor's algebra.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def _initial_guess_builder(self) -> None:
        """Constructs the initial guess for the differential equation
        solver that represents the bulk phase behaviour.

        The format
        of the method's output correponds with the reactor's algebra.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    # ==================================================================
    # Balances
    # ==================================================================

    @abstractmethod
    def _mass_balance(self) -> None:
        """Method that evals and returns the evaluated reactor's bulk
        mass balances. The format of the method's returns corresponds
        to the specific solver needs.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def _reactor_energy_balance(self) -> None:
        """Method that evals and returns the evaluated reactor's bulk
        energy balance. The format of the method's returns corresponds
        to the specific solver needs.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def _pressure_balance(self) -> None:
        """Method that evals and returns the evaluated reactor's bulk
        pressure balance. The format of the method's returns corresponds
        to the specific solver needs.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def _refrigerant_energy_balance(self) -> None:
        """Method that evals and returns the evaluated refrigerant
        energy balance. The format of the method's returns corresponds
        to the specific solver needs.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    @abstractmethod
    def simulate(self) -> None:
        """Simulates the reactor given the mass_balance_data,
        energy_balance_data, pressure_balance_data.

        Explain the output: # TODO

        Raises
        ------
        NotImplementedError
            Abstract method not implemented.
        """
        raise NotImplementedError("Abstract method not implemented.")

    # ==================================================================
    # Validators:
    #   Normal validation routines
    # ==================================================================

    def _fluxes_list_validator(self, in_flux_list, out_flux_list):
        """_summary_

        Parameters
        ----------
        in_flux_list : _type_
            _description_
        out_flux_list : _type_
            _description_
        """
