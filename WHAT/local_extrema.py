# -*- coding: utf-8 -*-
"""
Copyright 2014 Jean-Sebastien Gosselin

email: jnsebgosselin@gmail.com

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

#---- STANDARD LIBRARY IMPORTS ----

from sys import argv

#---- THIRD PARTY IMPORTS ----

import numpy as np
from PySide import QtGui, QtCore

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
import matplotlib.pyplot as plt

#---- PERSONAL IMPORTS ----

import database as db

#class MainWindow(QtGui.QMainWindow):
#        
#    def __init__(self, parent=None):
#        super(MainWindow, self).__init__(parent)
#        
#        self.initUI()
#        
#        def initUI(self):
#                            
##        self.setGeometry(350, 75, 800, 750)
#        self.setWindowTitle('Master Recession Curve Estimation')
#        self.setWindowIcon(iconDB.WHAT)

class Tooltips():
    
    def __init__(self, language): #------------------------------- ENGLISH -----
        
        self.undo = 'Undo'
        self.clearall = 'Clear all extremum from the graph'
        self.home = 'Reset original view.'
        self.editPeak = ('Toggle edit mode to manually add extremums ' +
                         'to the graph')
        self.delPeak = ('Toggle edit mode to manually remove extremums ' +
                        'from the graph')
        self.pan = 'Pan axes with left mouse, zoom with right'
        self.MRCalc = 'Calculate MRC (not yet available)'
        self.find_peak = 'Automated search for local extremum'
        
        if language == 'French': #--------------------------------- FRENCH -----
            
            pass
        
class MRCalc(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(MRCalc, self).__init__(parent)

        self.initUI()
#        self.initUI_weather_normals()
        self.fig_MRC_widget.mpl_connect('button_press_event', self.onclick)
        self.fig_MRC_widget.mpl_connect('motion_notify_event', self.mouse_vguide)
        
        
#        language = 'English'
#        global labelDB
#        labelDB = LabelDataBase(language)

#        global ttipDB
#        ttipDB = db.tooltips(language)
        
    def initUI(self):
        
        iconDB = db.icons()
        StyleDB = db.styleUI()
        ttipDB = Tooltips('English')
        
    #--------------------------------------------------------- FigureCanvas ----
        
        self.setWindowTitle('Master Recession Curve Estimation')
        
        self.fig_MRC = plt.figure()        
        self.fig_MRC.set_size_inches(8.5, 5)        
        self.fig_MRC.patch.set_facecolor('white')
        self.fig_MRC_widget = FigureCanvasQTAgg(self.fig_MRC)
        
    #-------------------------------------------------------------- TOOLBAR ----
        
        self.toolbar = NavigationToolbar2QTAgg(self.fig_MRC_widget, self)
        self.toolbar.hide()
        
        self.btn_undo = QtGui.QToolButton()
        self.btn_undo.setAutoRaise(True)
        self.btn_undo.setIcon(iconDB.undo)
        self.btn_undo.setToolTip(ttipDB.undo)
        self.btn_undo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_undo.setEnabled(False)
        
        self.btn_clearPeak = QtGui.QToolButton()
        self.btn_clearPeak.setAutoRaise(True)
        self.btn_clearPeak.setIcon(iconDB.clear_search)
        self.btn_clearPeak.setToolTip(ttipDB.clearall)
        self.btn_clearPeak.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.btn_home = QtGui.QToolButton()
        self.btn_home.setAutoRaise(True)
        self.btn_home.setIcon(iconDB.home)
        self.btn_home.setToolTip(ttipDB.home)
        self.btn_home.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.btn_findPeak = QtGui.QToolButton()
        self.btn_findPeak.setAutoRaise(True)
        self.btn_findPeak.setIcon(iconDB.findPeak2)
        self.btn_findPeak.setToolTip(ttipDB.find_peak)
        self.btn_findPeak.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.btn_editPeak = QtGui.QToolButton()
        self.btn_editPeak.setAutoRaise(True)
        self.btn_editPeak.setIcon(iconDB.add_point)
        self.btn_editPeak.setToolTip(ttipDB.editPeak)
        self.btn_editPeak.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.btn_delPeak = QtGui.QToolButton()
        self.btn_delPeak.setAutoRaise(True)
        self.btn_delPeak.setIcon(iconDB.erase)
        self.btn_delPeak.setToolTip(ttipDB.delPeak)
        self.btn_delPeak.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.btn_pan = QtGui.QToolButton()
        self.btn_pan.setAutoRaise(True)
        self.btn_pan.setIcon(iconDB.pan)
        self.btn_pan.setToolTip(ttipDB.pan)
        self.btn_pan.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.btn_MRCalc = QtGui.QToolButton()
        self.btn_MRCalc.setAutoRaise(True)
        self.btn_MRCalc.setIcon(iconDB.MRCalc)
        self.btn_MRCalc.setToolTip(ttipDB.MRCalc)
        self.btn_MRCalc.setFocusPolicy(QtCore.Qt.NoFocus)
                        
        separator1 = QtGui.QFrame()
        separator1.setFrameStyle(StyleDB.VLine)
        separator2 = QtGui.QFrame()
        separator2.setFrameStyle(StyleDB.VLine)
        
        subgrid_toolbar = QtGui.QGridLayout()
        toolbar_widget = QtGui.QWidget()
        
        row = 0
        col = 0
        subgrid_toolbar.addWidget(self.btn_undo, row, col)
        col += 1
        subgrid_toolbar.addWidget(self.btn_clearPeak, row, col)                
        col += 1        
        subgrid_toolbar.addWidget(self.btn_findPeak, row, col)
        col += 1 
        subgrid_toolbar.addWidget(self.btn_editPeak, row, col)
        col += 1        
        subgrid_toolbar.addWidget(self.btn_delPeak, row, col)
        col += 1        
        subgrid_toolbar.addWidget(separator1, row, col)
        col += 1
        subgrid_toolbar.addWidget(self.btn_home, row, col)
        col += 1
        subgrid_toolbar.addWidget(self.btn_pan, row, col)
        col += 1        
        subgrid_toolbar.addWidget(separator2, row, col)
        col += 1
        subgrid_toolbar.addWidget(self.btn_MRCalc, row, col)
        
        subgrid_toolbar.setSpacing(5)
        subgrid_toolbar.setContentsMargins(0, 0, 0, 0)
        subgrid_toolbar.setColumnStretch(col+1, 500)
                
        self.btn_undo.setIconSize(StyleDB.iconSize)
        self.btn_clearPeak.setIconSize(StyleDB.iconSize)
        self.btn_home.setIconSize(StyleDB.iconSize)
        self.btn_findPeak.setIconSize(StyleDB.iconSize)
        self.btn_editPeak.setIconSize(StyleDB.iconSize)
        self.btn_delPeak.setIconSize(StyleDB.iconSize)
        self.btn_pan.setIconSize(StyleDB.iconSize)
        self.btn_MRCalc.setIconSize(StyleDB.iconSize)
        
        toolbar_widget.setLayout(subgrid_toolbar)
                
    #------------------------------------------------------------ MAIN GRID ----
        
        mainGrid = QtGui.QGridLayout()
        
        row = 0 
        mainGrid.addWidget(toolbar_widget, row, 0)
        row += 1
        mainGrid.addWidget(self.fig_MRC_widget, row, 0)
        
              
        self.setLayout(mainGrid)
        mainGrid.setContentsMargins(15, 15, 15, 15) # Left, Top, Right, Bottom 
        mainGrid.setSpacing(15)
        mainGrid.setRowStretch(1, 500)
        
        ########################### 4 TESTING ######################
        
        fwaterlvl = 'Files4testing/PO01.xls'
    
        waterLvlObj = WaterlvlData()
        waterLvlObj.load(fwaterlvl)
    
        self.water_lvl = waterLvlObj.lvl
        self.water_lvl = self.water_lvl[350:]
    
        self.time = waterLvlObj.time
        self.time = self.time[350:]
        
        self.peak_indx = np.array([]).astype(int)
        self.peak_memory = [np.array([]).astype(int)]
        
        self.plot_water_levels(self.time, self.water_lvl, self.fig_MRC)
        
    #------------------------------------------------------------ EVENTS ----
        
        #----- Toolbox -----
        
        self.btn_undo.clicked.connect(self.undo)
        self.btn_clearPeak.clicked.connect(self.clear_all_peaks)        
        self.btn_home.clicked.connect(self.home)
        self.btn_findPeak.clicked.connect(self.find_peak)
        self.btn_editPeak.clicked.connect(self.edit_peak)
        self.btn_delPeak.clicked.connect(self.delete_peak)
        self.btn_pan.clicked.connect(self.pan_graph)
        self.btn_MRCalc.clicked.connect(self.plot_MRC)
    
    def plot_MRC(self):
        
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        
        b, c, hp = mrc_calc(self.time, self.water_lvl, self.peak_indx)
        
        self.h3_ax0.set_xdata(self.time)
        self.h3_ax0.set_ydata(hp)
        
        self.fig_MRC_widget.draw()
        
        QtGui.QApplication.restoreOverrideCursor()
            
    def plot_peak(self):
        
        self.h2_ax0.set_xdata(self.time[self.peak_indx])
        self.h2_ax0.set_ydata(self.water_lvl[self.peak_indx])
        
        if len(self.peak_memory) == 1:
            self.btn_undo.setEnabled(False)
        else:
            self.btn_undo.setEnabled(True)
                                   
        self.fig_MRC_widget.draw()
    
    def find_peak(self):
        
        n_j, n_add = local_extrema(self.water_lvl, 4 * 5)
        
        # Removing first and last point if necessary to always start with a
        # maximum and end with a minimum.
        
        # WARNING: y axis is inverted. Consequently, the logic needs to be 
        #          inverted also
        
        if n_j[0] > 0:
            n_j = np.delete(n_j, 0)
            
        if n_j[-1] < 0:
            n_j = np.delete(n_j, -1)
        
        self.peak_indx = np.abs(n_j).astype(int)
        self.peak_memory.append(self.peak_indx)
        
        self.plot_peak()
        
    def edit_peak(self):
        
        if self.btn_editPeak.autoRaise(): 
            
            # Activate <edit_peak>
            self.btn_editPeak.setAutoRaise(False)            
            
            # Deactivate <pan_graph>
            # http://stackoverflow.com/questions/17711099
            self.btn_pan.setAutoRaise(True)
            if self.toolbar._active == "PAN":
                self.toolbar.pan()
                
            # Deactivate <delete_peak>
            self.btn_delPeak.setAutoRaise(True)
            
        else:

            # Deactivate <edit_peak> and hide guide line
            self.btn_editPeak.setAutoRaise(True)
            self.ly.set_xdata(-1)
            self.fig_MRC_widget.draw()
            
    def delete_peak(self):
        
        if self.btn_delPeak.autoRaise():
            
            # Activate <delete_peak>
            self.btn_delPeak.setAutoRaise(False)
            
            # Deactivate <pan_graph>
            # http://stackoverflow.com/questions/17711099
            self.btn_pan.setAutoRaise(True)
            if self.toolbar._active == "PAN":
                self.toolbar.pan()
                
            # Deactivate <edit_peak> and hide guide line
            self.btn_editPeak.setAutoRaise(True)
            self.ly.set_xdata(-1)
            self.fig_MRC_widget.draw()
            
        else:

            # Deactivate <delete_peak>
            self.btn_delPeak.setAutoRaise(True)
        
    def pan_graph(self):
                
        if self.btn_pan.autoRaise():

            # Deactivate <edit_peak> and hide guide line
            self.btn_editPeak.setAutoRaise(True)
            self.ly.set_xdata(-1)
            self.fig_MRC_widget.draw()
            
            # Deactivate <delete_peak>
            self.btn_delPeak.setAutoRaise(True)
            
            # Activate <pan_graph>
            self.btn_pan.setAutoRaise(False)
            self.toolbar.pan()
            
        else:
            self.btn_pan.setAutoRaise(True)
            self.toolbar.pan()
            
    def home(self):
        self.toolbar.home()

    def undo(self):
        
        if len(self.peak_memory) > 1:
            self.peak_indx = self.peak_memory[-2]
            del self.peak_memory[-1]
        
            self.plot_peak()
        
            print 'undo'
        else:
            pass
            
    def clear_all_peaks(self):
                            
        self.peak_indx = np.array([]).astype(int)
        self.peak_memory.append(self.peak_indx)
    
        self.plot_peak()
                
    def plot_water_levels(self, t, x, fig):
        
        fheight = fig.get_figheight()
        fwidth = fig.get_figwidth()
    
    #------------------------------------------------------ FIGURE CREATION ----
        
        left_margin  = 0.85
        right_margin = 0.25
        bottom_margin = 0.85
        top_margin = 0.25
           
        x0 = left_margin / fwidth
        y0 = bottom_margin / fheight
        w = 1 - (left_margin + right_margin) / fwidth
        h = 1 - (bottom_margin + top_margin) / fheight
                        
    #-------------------------------------------------------- AXES CREATION ----        
        
        #---- Water Level (Host) ----
        
#        self.ax0  = fig.add_axes([x0, y0, w, h], zorder=0)
        self.ax0  = fig.add_axes([x0, y0, w, h], zorder=0)
        self.ax0.patch.set_visible(False)
        
#        #---Peaks---
#        ax1 = fig.add_axes(ax0.get_position(), frameon=False, zorder=1)
#        ax1.patch.set_visible(False)
        
    #----------------------------------------------------- XTICKS FORMATING ---- 
    
#        Xmin0 = 0
#        Xmax0 = 12.001
        
        self.ax0.xaxis.set_ticks_position('bottom')
        self.ax0.tick_params(axis='x',direction='out', gridOn=True)
#        ax0.xaxis.set_ticklabels([])
#        ax0.set_xticks(np.arange(Xmin0, Xmax0))
        
#        ax0.set_xticks(np.arange(Xmin0+0.5, Xmax0+0.49, 1), minor=True)
#        ax0.tick_params(axis='x', which='minor', direction='out', gridOn=False,
#                        length=0,)
#        ax0.xaxis.set_ticklabels(month_names, minor=True)
        
#        ax1.tick_params(axis='x', which='both', bottom='off', top='off',
#                        labelbottom='off'
    #----------------------------------------------------- YTICKS FORMATING ----
        
        self.ax0.yaxis.set_ticks_position('left')
        self.ax0.tick_params(axis='y',direction='out', gridOn=True)
                
    #------------------------------------------------------- SET AXIS RANGE ---- 
       
        delta = 0.05
        Xmin0 = np.min(t) - (np.max(t) - np.min(t)) * delta
        Xmax0 = np.max(t) + (np.max(t) - np.min(t)) * delta
    
        Ymin0 = np.min(x) - (np.max(x) - np.min(x)) * delta
        Ymax0 = np.max(x) + (np.max(x) - np.min(x)) * delta
    
        self.ax0.axis([Xmin0, Xmax0, Ymin0, Ymax0])
        self.ax0.invert_yaxis()
        
    #--------------------------------------------------------------- LABELS ----
    
        self.ax0.set_ylabel('Water level (mbgs)', fontsize=14, labelpad=25,
                            verticalalignment='top', color='black')
        self.ax0.set_xlabel('Time (days)', fontsize=14, labelpad=25,
                            verticalalignment='bottom', color='black')
#    ax0.yaxis.set_label_coords(-0.09, 0.5)
#    
#    ax1.set_ylabel(u'Monthly Mean Air Temperature (°C)', color='red',
#                   fontsize=label_font_size, verticalalignment='bottom',
#                   rotation=270)
#    ax1.yaxis.set_label_coords(1.09, 0.5)

    #------------------------------------------------------------- PLOTTING ----
    
        #---- Water Levels ----
    
        h1_ax0, = self.ax0.plot(t, x, color='blue', clip_on=True, zorder=10,
                                marker='None', linestyle='-')
        
        #---- Peaks ----
                 
        self.h2_ax0, = self.ax0.plot([], [], color='red', clip_on=True, 
                                     zorder=30, marker='o', linestyle='None')
                                     
        #---- Vertical guide line under cursor ----
                                     
        self.ly = self.ax0.axvline(x=.5, ymin=0, ymax=1, color='red', zorder=40)
        
        #---- Cross Remove Peaks ----
        
        self.xcross, = self.ax0.plot(-1, 0, color='red', clip_on=True, 
                                     zorder=20, marker='x', linestyle='None',
                                     markersize = 15, markeredgewidth = 3)
                                     
        #---- Recession ----
                                     
        self.h3_ax0, = self.ax0.plot([], [], color='red', clip_on=True,
                                     zorder=15, marker='None', linestyle='--')                          
        
    #-------------------------------------------------------- UPDATE WIDGET ----

        self.fig_MRC_widget.draw()
            
    def mouse_vguide(self, event):
        # http://matplotlib.org/examples/pylab_examples/cursor_demo.html
        if not self.btn_editPeak.autoRaise():
           
            x = event.xdata
            
            # update the line positions
            self.ly.set_xdata(x)
            
            self.fig_MRC_widget.draw()
            
        elif not self.btn_delPeak.autoRaise() and len(self.peak_indx) > 0:
            
            x = event.x
            y = event.y
            
            xt = np.empty(len(self.peak_indx))
            yt = np.empty(len(self.peak_indx))
            xpeak = self.time[self.peak_indx]
            ypeak = self.water_lvl[self.peak_indx]
            
            for i in range(len(self.peak_indx)):                
                xt[i], yt[i] = self.ax0.transData.transform((xpeak[i],ypeak[i]))
           
            r = ((xt - x)**2 + (yt - y)**2)**0.5
            
            if np.min(r) < 15 :

                indx = np.where(r == np.min(r))[0][0]
                                
                self.xcross.set_xdata(xpeak[indx])
                self.xcross.set_ydata(ypeak[indx])
                
                self.fig_MRC_widget.draw()
            else:
                self.xcross.set_xdata(-1)
                
                self.fig_MRC_widget.draw()            
        else:
            pass
            
    def onclick(self, event):
        
        x = event.x
        y = event.y
 
        #---------------------------------------------------- DELETE A PEAK ---- 
        
        # www.github.com/eliben/code-for-blog/blob/master/2009/qt_mpl_bars.py

        if x != None and y != None and not self.btn_delPeak.autoRaise():
            
            if len(self.peak_indx) == 0: return
                
            xt = np.empty(len(self.peak_indx))
            yt = np.empty(len(self.peak_indx))
            xpeak = self.time[self.peak_indx]
            ypeak = self.water_lvl[self.peak_indx]
        
            for i in range(len(self.peak_indx)):                
                xt[i], yt[i] = self.ax0.transData.transform((xpeak[i],ypeak[i]))
       
            r = ((xt - x)**2 + (yt - y)**2)**0.5
        
            if np.min(r) < 15 :

                indx = np.where(r == np.min(r))[0][0]
                            
                self.xcross.set_xdata(xpeak[indx])
                self.xcross.set_ydata(ypeak[indx])
                
                self.peak_indx = np.delete(self.peak_indx, indx)
                self.peak_memory.append(self.peak_indx)
                
                xpeak = np.delete(xpeak, indx)
                ypeak = np.delete(ypeak, indx)
                
                
                self.xcross.set_xdata(-1)            
                self.plot_peak()
            else:
                pass
            
        #------------------------------------------------------- ADD A PEAK ----        

        elif x != None and y != None and not self.btn_editPeak.autoRaise():
#            print(event.xdata, event.ydata)
            
            xclic = event.xdata
        
            # http://matplotlib.org/examples/pylab_examples/cursor_demo.html
            
            x = self.time
            y = self.water_lvl
            
            indxmin = np.where(x < xclic)[0]
            indxmax = np.where(x > xclic)[0]
            if len(indxmax) == 0:
                
                self.peak_indx = np.append(self.peak_indx, len(x)-1)
                self.peak_memory.append(self.peak_indx)
                
            elif len(indxmin) == 0:
                
                self.peak_indx = np.append(self.peak_indx, 0)
                self.peak_memory.append(self.peak_indx)
                
            else:
                indxmin = indxmin[-1]
                indxmax = indxmax[0]
                
                dleft = xclic - x[indxmin]
                dright = x[indxmax] - xclic
                
                if dleft < dright:
                    
                    self.peak_indx = np.append(self.peak_indx, indxmin)
                    self.peak_memory.append(self.peak_indx)
                                        
                else:
                    
                    self.peak_indx = np.append(self.peak_indx, indxmax)
                    self.peak_memory.append(self.peak_indx)
           
            self.plot_peak()    
   
#===============================================================================
def local_extrema(x, Deltan):
    """
    Code adapted from a MATLAB script at 
    www.ictp.acad.ro/vamos/trend/local_extrema.htm
    
    LOCAL_EXTREMA Determines the local extrema of a given temporal scale.
    
    ---- OUTPUT ----
    
    n_j = The positions of the local extrema of a partition of scale Deltan
          as defined at p. 82 in the book [ATE] C. Vamos and M. Craciun,
          Automatic Trend Estimation, Springer 2012.
          The positions of the maxima are positive and those of the minima
          are negative.
    kadd = n_j(kadd) are the local extrema with time scale smaller than Deltan
           which are added to the partition such that an alternation of maxima
           and minima is obtained.    
    """
#===============================================================================

    N = len(x)
    
    ni = 0
    nf = N - 1
    
    #-------------------------------------------------------------- PLATEAU ----
    
    # Recognize the plateaus of the time series x defined in [ATE] p. 85
    # [n1[n], n2[n]] is the interval with the constant value equal with x[n]
    # if x[n] is not contained in a plateau, then n1[n] = n2[n] = n
    #
    # Example with a plateau between indices 5 and 8:
    #  x = [1, 2, 3, 4, 5, 6, 6, 6, 6, 7, 8,  9, 10, 11, 12]
    # n1 = [0, 1, 2, 3, 4, 5, 5, 5, 5, 9, 10, 11, 12, 13, 14]
    # n2 = [0, 1, 2, 3, 4, 8, 8, 8, 8, 9, 10, 11, 12, 13, 14]
   
    n1 = np.arange(N)
    n2 = np.arange(N)
                
    dx = np.diff(x)
    if np.any(dx == 0):
        print 'At least 1 plateau has been detected in the data'
        for i in range(N-1):            
            if x[i+1] == x[i]:                
                n1[i+1] = n1[i]
                n2[n1[i+1]:i+1] = i+1

    #-------------------------------------------------------- MAIN FUNCTION ----
    
    # the iterative algorithm presented in Appendix E of [ATE]
    
    nc = 0    # the time step up to which the time series has been
              # analyzed ([ATE] p. 127)
    Jest = 0  # number of local extrema of the partition of scale DeltaN 
    iadd = 0  # number of additional local extrema
    flagante = 0
    kadd = [] # order number of the additional local extrema between all the
              # local extrema
    n_j = []  # positions of the local extrema of a partition of scale Deltan
    
    while nc < nf:

        # the next extremum is searched within the interval [nc, nlim]
        
        nlim = min(nc + Deltan, nf)   
    
        #--------------------------------------------------- SEARCH FOR MIN ----
    
        xmin = np.min(x[nc:nlim+1])
        nmin = np.where(x[nc:nlim+1] == xmin)[0][0] + nc
       
        nlim1 = max(n1[nmin] - Deltan, ni)
        nlim2 = min(n2[nmin] + Deltan, nf)
        
        xminn = np.min(x[nlim1:nlim2+1])
        nminn = np.where(x[nlim1:nlim2+1] == xminn)[0][0] + nlim1
        
        # if flagmin = 1 then the minimum at nmin satisfies condition (6.1)
        if nminn == nmin:
            flagmin = 1
        else:
            flagmin = 0
            
        #--------------------------------------------------- SEARCH FOR MAX ----
            
        xmax = np.max(x[nc:nlim+1])
        nmax = np.where(x[nc:nlim+1] == xmax)[0][0] + nc   

        nlim1 = max(n1[nmax] - Deltan, ni)        
        nlim2 = min(n2[nmax] + Deltan, nf)
        
        xmaxx = np.max(x[nlim1:nlim2+1])
        nmaxx = np.where(x[nlim1:nlim2+1] == xmaxx)[0][0] + nlim1 
        
        # If flagmax = 1 then the maximum at nmax satisfies condition (6.1)
        if nmaxx == nmax: 
            flagmax = 1
        else: 
            flagmax=0
       
        #------------------------------------------------------- MIN or MAX ----

        # The extremum closest to nc is kept for analysis
        if flagmin == 1 and flagmax == 1:
            if nmin < nmax:
                flagmax = 0
            else:
                flagmin = 0

        #------------------------------------------------ ANTERIOR EXTREMUM ----
                
        if flagante == 0: # No ANTERIOR extremum
            
            if flagmax == 1:  # CURRENT extremum is a MAXIMUM

                nc = n1[nmax] + 1
                flagante = 1
                n_j = np.append(n_j, np.floor((n1[nmax] + n2[nmax]) / 2.))
                Jest += 1 
                
            elif flagmin == 1:  # CURRENT extremum is a MINIMUM

                nc = n1[nmin] + 1
                flagante = -1
                n_j = np.append(n_j, -np.floor((n1[nmin] + n2[nmin]) / 2.))
                Jest += 1

            else: # No extremum

                nc = nc + Deltan
                
        elif flagante == -1: # ANTERIOR extremum is an MINIMUM
            
            tminante = np.abs(n_j[-1])
            xminante = x[tminante]
            
            if flagmax == 1: # CURRENT extremum is a MAXIMUM                

                if xminante < xmax:

                    nc = n1[nmax] + 1
                    flagante = 1
                    n_j = np.append(n_j, np.floor((n1[nmax] + n2[nmax]) / 2.))
                    Jest += 1
                    
                else: 
                    
                    # CURRENT MAXIMUM is smaller than the ANTERIOR MINIMUM
                    # an additional maximum is added ([ATE] p. 82 and 83)
                    
                    xmaxx = np.max(x[tminante:nmax+1])
                    nmaxx = np.where(x[tminante:nmax+1] == xmaxx)[0][0]               
                    nmaxx += tminante
                    
                    nc = n1[nmaxx] + 1
                    flagante = 1
                    n_j = np.append(n_j, np.floor((n1[nmaxx] + n2[nmaxx]) / 2.))
                    Jest += 1
                    
                    kadd = np.append(kadd, Jest-1)
                    iadd += 1
                
            elif flagmin == 1: # CURRENT extremum is also a MINIMUM
                               # an additional maximum is added ([ATE] p. 82)

                nc = n1[nmin]
                flagante = 1
                
                xmax = np.max(x[tminante:nc+1])
                nmax = np.where(x[tminante:nc+1] == xmax)[0][0] + tminante                
                
                n_j = np.append(n_j, np.floor((n1[nmax] + n2[nmax]) / 2.))                               
                Jest += 1
                
                kadd = np.append(kadd, Jest-1)
                iadd += 1
                
            else:
                nc = nc + Deltan
                
        else: # ANTERIOR extremum is a MAXIMUM
            
            tmaxante = np.abs(n_j[-1])
            xmaxante = x[tmaxante]
            
            if flagmin == 1: # CURRENT extremum is a MINIMUM
                
                if xmaxante > xmin:
                    
                    nc = n1[nmin] + 1
                    flagante = -1
                    
                    n_j = np.append(n_j, -np.floor((n1[nmin] + n2[nmin]) / 2.))
                    Jest += 1
                    
                else: # CURRENT MINIMUM is larger than the ANTERIOR MAXIMUM:
                      # an additional minimum is added ([ATE] p. 82 and 83)
                    
                    xminn = np.min(x[tmaxante:nmin+1])  
                    nminn = np.where(x[tmaxante:nmin+1] == xminn)[0][0]
                    nminn += tmaxante
                    
                    nc = n1[nminn] + 1
                    flagante = -1
                    
                    n_j = np.append(n_j, -np.floor((n1[nminn] + n2[nminn]) / 2.))                
                    Jest = Jest + 1

                    kadd = np.append(kadd, Jest-1)                
                    iadd += 1
                    
            elif flagmax == 1: # CURRENT extremum is also an MAXIMUM:
                               # an additional minimum is added ([ATE] p. 82)
                nc = n1[nmax]
                flagante = -1
                
                xmin = np.min(x[tmaxante:nc+1])
                nmin = np.where(x[tmaxante:nc+1] == xmin)[0]            
                nmin += tmaxante
                
                n_j = np.append(n_j, -np.floor((n1[nmin] + n2[nmin]) / 2.))
                Jest += 1
                
                kadd = np.append(kadd, Jest-1)
                iadd += 1
                
            else:
                nc = nc + Deltan
            
#    # x(ni) is not included in the partition of scale Deltan 
#    nj1 = np.abs(n_j[0])
#    if nj1 > ni:
#        if n1[nj1] > ni: # the boundary ni is not included in the plateau
#                         # containing the first local extremum at n_j[1] and it
#                         # is added as an additional local extremum ([ATE] p. 83)
#            n_j = np.hstack((-np.sign(n_j[0]) * ni, n_j))
#            Jest += 1
#            
#            kadd = np.hstack((0, kadd + 1))
#            iadd += 1
#
#        else: # the boundary ni is included in the plateau containing
#              # the first local extremum at n_j(1) and then the first local
#              # extremum is moved at the boundary of the plateau
#            n_j[0] = np.sign(n_j[0]) * ni
   
   
#    # the same situation as before but for the other boundary nf
#    njJ = np.abs(n_j[Jest])
#    if njJ < nf:
#        if n2[njJ] < nf:
#            n_j = np.append(n_j, -np.sign(n_j[Jest]) * nf)
#            Jest += 1
#
#            kadd = np.append(kadd, Jest)
#            iadd += 1
#        else:
#            n_j[Jest] = np.sign(n_j[Jest]) * nf
   
    return n_j, kadd

def mrc_calc(t, h, ipeak):
    
    ipeak = np.sort(ipeak)
    
    maxpeak = ipeak[:-1:2]
    minpeak = ipeak[1::2]
    
    #-------------------------------------------------------- Quality Check ----
    
    dpeak = (h[maxpeak] - h[minpeak]) * -1 # WARNING: Don't forget it is mbgs
    if np.any(dpeak < 0):
        print 'There is a problem with the pair-ditribution of min-max'
        return
    if len(ipeak) == 0:
        print 'No extremum selected'
        return
    
    nsegmnt = len(minpeak)
    
    b = 0.1
    c = 0
    
    ObjFn_b = 10**6
    OPSTP_b = -0.01
    
    MODE = 0 # 0: exponential; 1: linear
    REGMOD = 1 # 0: RMSE; 1: MAE; 2: abs(ME)
   
    while abs(OPSTP_b) > 1e-5:
    
        OPSTP_c = 0.1   # Optimisation step
        ObjFn_c = 10**6  # Force divergence for first iteration
        while abs(OPSTP_c) > 1e-4:

            # RECESSION CALCULATIONS
            
            dt = np.diff(t)
            dhp = -b * (h[:-1] + h[1:] - 2*c) * dt / 2.
            
            hp = np.empty(len(h)) * np.nan
            for i in range(nsegmnt):
                hp[maxpeak[i]] = h[maxpeak[i]]
                
                for j in range(minpeak[i] - maxpeak[i]):
                    hp[maxpeak[i]+j+1] = hp[maxpeak[i]+j] + dhp[maxpeak[i]+j]
                    
            indx = np.where(~np.isnan(hp))
            
            #---- COMPUTE OBJ. FUNC. ----
            
            if REGMOD == 0:  # RMSE
                ObjFn = (np.mean((h[indx] - hp[indx])**2))**0.5
            elif REGMOD == 2: # abs(ME)
                ObjFn = np.abs(np.mean((h[indx] - hp[indx])))
            else:  # MAE
                ObjFn = np.mean(np.abs(h[indx] - hp[indx]))
            
            if ObjFn_c < ObjFn:
                OPSTP_c = -OPSTP_c / 10.
 
            ObjFn_c = np.copy(ObjFn)
            c = c + OPSTP_c
            
        if ObjFn_b < ObjFn_c:
            OPSTP_b = -OPSTP_b / 10.
        
        if b + OPSTP_b < 10**-12:
            OPSTP_b = OPSTP_b / 10.
    
        ObjFn_b = ObjFn_c
        b = b + OPSTP_b
    
    print; print 'FIN'; print
    
    print 'b =', b
    print 'c =', c
    
#    print dhp
    
    return b, c, hp
    
   
    
      
  
      #b=0.1;
      #C=-2;
      #RMSE_b=10^6;
      #OPSTP_b=-0.01;
      #MODE='exponential';
#while abs(OPSTP_b)>1e-5
#    OPSTP_C=0.1;%Optimisation step
#    RMSE_C=10^6; %Force divergence for first iteration
#    while abs(OPSTP_C)>1e-4
#        %RECESSION CALCULATIONS
#        dhp=-b*(DTWL(1:end-1)+DTWL(2:end)-2*C).*(TIME(2:end)-TIME(1:end-1))/2;
#        STOCK=[]; %initialization or reinitialization
#        for i=1:length(MINMAX)
#            hp(1)=DTWL(MINMAX(i,1));
#            for j=1:MINMAX(i,2)-MINMAX(i,1)
#                hp(j+1)=hp(j)+dhp(j+MINMAX(i,1)-1);
#            end
#            STOCK=[STOCK ; hp' DTWL(MINMAX(i,1):MINMAX(i,2),1) (MINMAX(i,1):MINMAX(i,2))'];
#            clear hp
#        end
#        RMSE=(mean(abs(STOCK(:,1)-STOCK(:,2))));
#        if RMSE_C<RMSE
#            OPSTP_C=-OPSTP_C/10;
#        end
#        RMSE_C=RMSE;
#        C=C+OPSTP_C;
#    end
#    if RMSE_b<RMSE_C
#        OPSTP_b=-OPSTP_b/10;
#    elseif b+OPSTP_b<10^-12
#        OPSTP_b=OPSTP_b/10;
#    end
#    RMSE_b=RMSE_C;
#    b=b+OPSTP_b;  
   


if __name__ == '__main__':
    
    from matplotlib import pyplot as plt
    import xlrd
    from meteo import MeteoObj
    from hydroprint import WaterlvlData, filt_data
    import database as db
    
    plt.close('all')
    
    fmeteo = 'Files4testing/AUTEUIL_2000-2013.out'
    fwaterlvl = 'Files4testing/PO16A.xls'
    
    waterLvlObj = WaterlvlData()
    waterLvlObj.load(fwaterlvl)
    
    x = waterLvlObj.lvl
    x = 100-x[:500]
    
    t = waterLvlObj.time
    t = t[:500]
    
    app = QtGui.QApplication(argv)   
    instance_1 = MRCalc()
    instance_1.show()
    app.exec_() 
    
#    # http://stackoverflow.com/questions/15721094
#    fig = plt.figure()
#    plt.plot(t, x)
#    def onclick(event):
#        if event.xdata != None and event.ydata != None:
#            print(event.xdata, event.ydata)
#            plt.plot(event.xdata, event.ydata, 'or')
#    cid = fig.canvas.mpl_connect('button_press_event', onclick)

#    plt.show()
    
    
#    # ---- Without smoothing ----
#    
#    plt.figure()
#    plt.plot(x)
#    plt.plot(x, '.')
#    
#    n_j, n_add = local_extrema(x, 4 * 2)
#    print n_j
#    
#    n_j = np.abs(n_j).astype(int)  
#    n_add = np.abs(n_add).astype(int) 
#    
#    plt.plot(n_j, x[n_j], 'or' )
#    
#    # ---- With smoothing ----
#    
#    tfilt, xfilt = filt_data(t, x, 4)
#    
#    plt.figure()
#    plt.plot(t, x)
#    plt.plot(tfilt, xfilt, 'r')
#    
#    n_j, _ = local_extrema(xfilt, 4 * 3)
#    
#    n_j = np.abs(n_j).astype(int)  
#    
#    plt.plot(tfilt[n_j], xfilt[n_j], 'or' )