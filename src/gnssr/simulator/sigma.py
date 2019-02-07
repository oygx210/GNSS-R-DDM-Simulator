#!/usr/bin/env python

import numpy as np

from gnssr.simulator.jacobian.planar import *
from gnssr.simulator.antenna.tds_antenna import *
from gnssr.simulator.rcs.sea_rcs import *

def sigma(delay, doppler, sim_config):
    """
    Accounts for the surface geometry, the antenna patterns, and the bistatic 
    radar cross section of each cell. Assigns a weighting factor to each 
    delay-Doppler cell of the scene. 

    Implements equation 10:
        J. F. Marchan-Hernandez, A. Camps, N. Rodriguez-Alvarez, E. Valencia, X.  
        Bosch-Lluis, and I. Ramos-Perez, “An Efficient Algorithm to the 
        Simulation of Delay–Doppler Maps of Reflected Global Navigation 
        Satellite System Signals,” IEEE Transactions on Geoscience and Remote 
        Sensing, vol. 47, no.  8, pp. 2733–2740, Aug. 2009.  

    Args:
        delay (numpy.ndarray with size(1,)): Delay increment.
        doppler (numpy.ndarray with size(1,)): Doppler increment
        sim_config: Instance of simulation_configuration class.

    Returns:
        numpy.ndarray with  size(1,).
    """
    r_t = sim_config.r_t
    r_r = sim_config.r_r
    v_t = sim_config.v_t
    v_r = sim_config.v_r
    elevation = sim_config.elevation
    f_carrier = sim_config.f_carrier
    h_r = sim_config.h_r
    transmitting_power = sim_config.transmitting_power
    coherent_integration_time = sim_config.coherent_integration_time

    x_1 = x_delay_doppler_1(delay, doppler, sim_config).real
    y_1 = y_delay_doppler_1(delay, doppler, sim_config).real
    r_1 = np.array([x_1,y_1,0])

    x_2 = x_delay_doppler_2(delay, doppler, sim_config).real
    y_2 = y_delay_doppler_2(delay, doppler, sim_config).real
    r_2 = np.array([x_2,y_2,0])

    return transmitting_power*coherent_integration_time**2/(4*np.pi) * ( \
                radar_cross_section(r_1, sim_config)/( \
                    np.linalg.norm(r_1-r_t)**2* \
                    np.linalg.norm(r_r-r_1)**2 \
                ) * \
                delay_doppler_jacobian_1(delay, doppler, sim_config) * \
                receiver_antenna_gain(r_1, sim_config) * \
                transmitting_antenna_gain(r_1, sim_config) \
                + 
                radar_cross_section(r_2, sim_config)/( \
                    np.linalg.norm(r_2-r_t)**2* \
                    np.linalg.norm(r_r-r_2)**2 \
                ) * \
                delay_doppler_jacobian_2(delay, doppler, sim_config) * \
                receiver_antenna_gain(r_2, sim_config) * \
                transmitting_antenna_gain(r_2, sim_config) \
            )