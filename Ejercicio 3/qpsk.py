#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Basic QPSK starter
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class qpsk(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Basic QPSK starter", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Basic QPSK starter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "qpsk")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 4000
        self.sps = sps = 32
        self.samp_rate = samp_rate = symbol_rate*sps
        self.constellation = constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 3, 2],
        4, 1, digital.constellation.NO_NORMALIZATION).base()
        self.constellation.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self.root_raised_cosine_filter_0_0_0 = filter.interp_fir_filter_fff(
            16,
            firdes.root_raised_cosine(
                16,
                samp_rate,
                symbol_rate,
                0.25,
                (8*sps)))
        self.root_raised_cosine_filter_0_0 = filter.interp_fir_filter_fff(
            16,
            firdes.root_raised_cosine(
                16,
                samp_rate,
                symbol_rate,
                0.25,
                (8*sps)))
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_ccf(
            16,
            firdes.root_raised_cosine(
                16,
                samp_rate,
                symbol_rate,
                0.25,
                (8*sps)))
        self.qtgui_sink_x_1 = qtgui.sink_c(
            2048, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(constellation)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 32)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 0)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 10000, 2, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 10000, 2, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10000, 1, 0, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 4, 128))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.root_raised_cosine_filter_0_0_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0_0, 0), (self.blocks_float_to_complex_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qpsk")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samp_rate(self.symbol_rate*self.sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))
        self.root_raised_cosine_filter_0_0_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate(self.symbol_rate*self.sps)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))
        self.root_raised_cosine_filter_0_0_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))
        self.root_raised_cosine_filter_0_0_0.set_taps(firdes.root_raised_cosine(16, self.samp_rate, self.symbol_rate, 0.25, (8*self.sps)))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation
        self.digital_constellation_encoder_bc_0.set_constellation(self.constellation)




def main(top_block_cls=qpsk, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
