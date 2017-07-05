# -*- coding: utf-8 -*-
"""
Copyright 2014-2017 Jean-Sebastien Gosselin
email: jean-sebastien.gosselin@ete.inrs.ca

This file is part of WHAT (Well Hydrograph Analysis Toolbox).

WHAT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

# Standard library imports:
# from datetime import datetime

from os import getcwd

# Third party imports:
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import xlrd

import matplotlib as mpl


class LabelDataBase():
    def __init__(self, language):
        self.lag = u'Time Lag (days)'
        self.A = 'Cumulative Response Function'
        self.title = ('Well %s from %s to %s')

        if language == 'French':
            self.lag = u'Lag temporel (h)'
            self.A = u'Réponse barométrique cumulative'
            self.title = u'Réponse barométrique pour le puits %s du %s au %s'


# =============================================================================


class BRFFigure(mpl.figure.Figure):
    def __init__(self):
        super(BRFFigure, self).__init__()

        # -------------------------------------------------- FIG CREATION -----

        fig_width = 8
        fig_height = 5

        self.set_size_inches(fig_width, fig_height)
        self.patch.set_facecolor('white')

        left_margin = 0.8
        right_margin = 0.25
        bottom_margin = 0.75
        top_margin = 0.25

        # ---------------------------------------------------------- AXES -----

        ax = self.add_axes([left_margin/fig_width, bottom_margin/fig_height,
                            1 - (left_margin + right_margin)/fig_width,
                            1 - (bottom_margin + top_margin)/fig_height],
                           zorder=1)
        ax.set_visible(False)

        # ---- ticks ----

        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', which='major', direction='out',
                       gridOn=True)

        # ---- axis ----

        lbd = LabelDataBase('English')
        ax.set_xlabel(lbd.lag, fontsize=14, labelpad=8)
        ax.set_ylabel(lbd.A, fontsize=14)

        # ---- artists ----

        self.line, = ax.plot([], [], ls='-', color='blue', linewidth=1.5,
                             zorder=20, clip_on=True)

        self.markers, = ax.plot([], [], color='0.1', mec='0.1', marker='.',
                                ls='None', ms=5, zorder=30, mew=1,
                                clip_on=False)

        self.errbar, = ax.plot([], [])

        offset = mpl.transforms.ScaledTranslation(
                0, -5/72, self.dpi_scale_trans)

        self.title = ax.text(0.5, 1, '', ha='center', va='top', fontsize=14,
                             transform=ax.transAxes+offset)

    # =========================================================================

    def empty_BRF(self):
        ax = self.axes[0]
        ax.set_visible(False)

    def plot_BRF(self, lag, A, err, date0, date1, well, msize=0,
                 draw_line=True, ylim=[None, None]):

        ax = self.axes[0]
        ax.set_visible(True)

        lbd = LabelDataBase('English')
        lag_max = np.max(lag)

        # --------------------------------------------------------- TICKS -----

        TCKPOS = np.arange(0, max(lag_max+1, 10), 1)
        ax.set_xticks(TCKPOS)

        TCKPOS = np.arange(-10, 10, 0.2)
        ax.set_yticks(TCKPOS)

        # ---------------------------------------------------------- AXIS -----

        if ylim[0] is None:
            if len(err) > 0:
                ymin = min(np.floor(np.min(A-err)/0.2)*0.2, 0)
            else:
                ymin = min(np.floor(np.min(A)/0.2)*0.2, 0)
        else:
            ymin = ylim[0]

        if ylim[1] is None:
            if len(err) > 0:
                ymax = max(np.ceil(np.max(A+err)/0.2)*0.2, 1)
            else:
                ymax = max(np.ceil(np.max(A)/0.2)*0.2, 1)
        else:
            ymax = ylim[1]

        ymin += -10**-12
        ymax += 10**-12

        ax.axis([0, lag_max, ymin, ymax])

        # ---------------------------------------------------------- PLOT -----

        self.line.set_xdata(lag)
        self.line.set_ydata(A)
        self.line.set_visible(draw_line)

        self.markers.set_xdata(lag)
        self.markers.set_ydata(A)
        self.markers.set_markersize(msize)

        self.errbar.remove()
        if len(err) > 0:
            self.errbar = ax.fill_between(lag, A+err, A-err, edgecolor='0.65',
                                          color='0.75', clip_on=True)
        else:
            self.errbar, = ax.plot([], [])
#
        self.title.set_text(lbd.title % (well, date0, date1))


def plot_BRF(lag, A, err, date0, date1, well, msize=0, draw_line=True,
             ylim=[None, None]):

    label_data_base = LabelDataBase('English')
    lag_max = np.max(lag)

    # ------------------------------------------------------ FIG CREATION -----

    fig_width = 8
    fig_height = 5

    fig1 = plt.figure(figsize=(fig_width, fig_height))
    fig1.patch.set_facecolor('white')

    left_margin = 0.8
    right_margin = 0.25
    bottom_margin = 0.75
    top_margin = 0.25

    # -------------------------------------------------------------- AXES -----

    ax1 = fig1.add_axes([left_margin/fig_width, bottom_margin/fig_height,
                        1 - (left_margin + right_margin)/fig_width,
                        1 - (bottom_margin + top_margin)/fig_height], zorder=1)

    # ------------------------------------------------------------- TICKS -----

    TCKPOS = np.arange(0, max(lag_max+1, 10), 1)
    ax1.set_xticks(TCKPOS)

    # TCKPOS = np.arange(0, lag_max, 0.25)
    # ax1.set_xticks(TCKPOS, minor=True)

    ax1.xaxis.set_ticks_position('bottom')

    TCKPOS = np.arange(-5, 5, 0.2)
    ax1.set_yticks(TCKPOS)

    # TCKPOS = np.arange(0, 1.1, 0.025)
    # ax1.set_yticks(TCKPOS, minor=True)

    ax1.yaxis.set_ticks_position('left')

    ax1.tick_params(axis='both', which='major', direction='out', gridOn=True)
    # ax1.tick_params(axis='both', which='minor', direction='out',gridOn=False)

    # -------------------------------------------------------------- AXIS -----

    if ylim[0] is None:
        if len(err) > 0:
            ymin = min(np.floor(np.min(A-err)/0.2)*0.2, 0)
        else:
            ymin = min(np.floor(np.min(A)/0.2)*0.2, 0)
    else:
        ymin = ylim[0]

    if ylim[1] is None:
        if len(err) > 0:
            ymax = max(np.ceil(np.max(A+err)/0.2)*0.2, 1)
        else:
            ymax = max(np.ceil(np.max(A)/0.2)*0.2, 1)
    else:
        ymax = ylim[1]

    ymin += -10**-12
    ymax += 10**-12

    ax1.axis([0, lag_max, ymin, ymax])

    # ------------------------------------------------------------- LABEL -----

    ax1.set_xlabel(label_data_base.lag, fontsize=14, labelpad=8)
    ax1.set_ylabel(label_data_base.A, fontsize=14)

    # -------------------------------------------------------------- PLOT -----

    if draw_line is True:
        ax1.plot(lag, A, ls='-', color='blue', linewidth=1.5, zorder=20,
                 clip_on=True)

    if len(err) > 0:
        ax1.fill_between(lag, A+err, A-err, edgecolor='0.65', color='0.75',
                         clip_on=True)

    ax1.plot(lag, A, color='0.1', mec='0.1', marker='.', ls='None',
             ms=msize, zorder=30, mew=1, clip_on=False)

    # ---- title ----

    offset = mpl.transforms.ScaledTranslation(0, -5/72, fig1.dpi_scale_trans)
    ax1.text(0.5, 1,
             label_data_base.title % (well, date0, date1),
             ha='center', va='top', fontsize=14,
             transform=ax1.transAxes+offset)

    #    if len(err):
    #        erb = ax1.errorbar(lag, A, yerr=err, color='red',
    #                           ms=0, mec='blue', fmt='.', ecolor='0.5',
    #                           zorder=10, clip_on=True)
    #
    #        # http://stackoverflow.com/questions/2842123
    #        for b in erb[1]:
    #            b.set_clip_on(True)
    #        for b in erb[2]:
    #            b.set_clip_on(True)




if __name__ == '__main__':
    pass
